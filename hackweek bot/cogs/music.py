import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
import random
import logging
import os
from discord import opus
from asyncio import sleep
import ffmpeg


ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            data = data['entries'][0]

        await ctx.send(f'Added **{data["title"]}** to the Queue.')

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer(commands.Cog):
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300): 
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                if self in self._cog.players.values():
                    return self.destroy(self._guild)
                return

            if not isinstance(source, YTDLSource):
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f':hammer_pick: | There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            self.np = await self._channel.send(f'Now Playing: **{source.title}** Requested by: **{source.requester}**')
            await self.next.wait()

            source.cleanup()
            self.current = None

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:  
            for entry in self.players[guild.id].queue._queue:
                if isinstance(entry, YTDLSource): 
                    entry.cleanup()
            self.players[guild.id].queue._queue.clear()
        except KeyError:
            pass                        
                       
        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('**This command can not be used in Private Messages.**')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            embed = discord.Embed(title="Error:", description="Error connecting to Voice Channel. Please make sure you are in a voice channel")
            await ctx.send(embed=embed)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player
                
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='connect', aliases=['join', "summon", "Join", "JOIN", "Summon", "SUMMON", "Connect", "CONNECT"])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f':x: | Connecting to channel: <{channel}> timed out.')

        await ctx.send(f'Successfully Connected to: **{channel}**', delete_after=15)

                 
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='play', aliases=['sing', 'Sing', 'Play', 'PLAY', 'SING', "p", "P"])
    async def play_(self, ctx, *, search: str):
     

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)
                 
        if ctx.message.author.voice is None:
            return await ctx.send('Join a voice channel first')

        player = self.get_player(ctx)

        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)
 

                 

                 
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='pause', aliases=["Pause", "PAUSE"])
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
        elif vc.is_paused():
            return
                 
        if ctx.message.author.voice is None:
            return await ctx.send('Join a voice channel first')
                 
        vc.pause()
        await ctx.send(f'**{ctx.author}**: Paused the song!')

                 
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='resume', aliases=["continue", "start", "Continue", "CONTINUE", "Start", "START", "Resume", "RESUME"])
    async def resume_(self, ctx):
        """Resume the currently paused song."""               
        vc = ctx.voice_client

        if ctx.message.author.voice is None:
            return await ctx.send('Join a voice channel first')
                 
        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)                 
        elif not vc.is_paused():
            return
     
                 
        vc.resume()
        await ctx.send(f':play_pause: | **{ctx.author}**: Resumed the song!')      
                 
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='skip', aliases=["next", "Next", "NEXT", "Skip", "SKIP", "s", "S"])
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)
                 
        if ctx.message.author.voice is None:
            return await ctx.send('Join a voice channel first')
                 
        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f':track_next: Skipped the song!')
                 
                 
                 
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='queue', aliases=['q', 'playlist', "queueinfo", "Q", "Playlist", "PLAYLIST", "Queueinfo", "QUEUEINFO"])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)
                 
        if ctx.message.author.voice is None:
            return await ctx.send('Join a voice channel first')

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')


                 
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = '\n'.join(f'**{_["title"]}**' for _ in upcoming)
        embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt, color=0xE9A72F)

        await ctx.send(embed=embed)
               
               

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing', 'Np', 'NP', 'Current', 'CURRENT', 'Currentsong', 'CURRENTSONG', 'Playing', 'PLAYING'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently playing anything!')


        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        player.np = await ctx.send(f'Now Playing: **{vc.source.title}**\nRequested by **{vc.source.requester}**')
               
               

    @commands.command(name='volume', aliases=['vol', 'Vol', 'VOL', 'Volume', 'VOLUME'])
    @commands.is_owner()
    async def change_volume(self, ctx, *, vol: float):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!', delete_after=20)


        if not 1 < vol < 101:
            return await ctx.send('Please enter a value between 1 and 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'**{ctx.author}**: Set the volume to **{vol}%**')
               
               
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name='stop', aliases=["leave", "Leave", "LEAVE", "Stop", "STOP"])
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!', delete_after=20)

        await self.cleanup(ctx.guild)

def setup(bot):
    bot.add_cog(Music(bot))

