import discord
import logging
from discord.utils import get
from discord.ext.commands import Bot, Greedy
from discord.ext import commands
from itertools import cycle
import time
import typing
import random
import asyncio
import os
import ast
import json
from youtube_dl import YoutubeDL
                                   

bot = commands.Bot(command_prefix="prefix")

bot.remove_command("help")
bot.load_extension("cogs.hehe")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.music")









@bot.event
async def on_message(message):




    if message.content.startswith('gay'):
        msg =await message.channel.send('no u')
        await msg.edit(content = "no ur mom")
        await msg.edit(content = "no ur dad")
        await msg.edit(content = "uve seen nothing")
        await msg.edit(content = "nvm pretend like its nothing")
        await msg.edit(content = "ok bai")
        await msg.delete()

    await bot.process_commands(message)






 
@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping =  round(ping_ * 1000)
    await ctx.send(f"my ping is {ping}ms")

@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')
    print(f'Successfully logged in and booted...!')


















@bot.command()
async def team(ctx):
    await ctx.send("team plz")

@bot.command()
async def nothing(ctx):
    msg = await ctx.send("u gay dont waste my time >:c")
    await msg.edit(content = "u fking gay why bully me ;(")
    await msg.edit(content = "plox leave me alone palis")
    await msg.edit(content = "leave me alone and i will give u my phone number c:")
    await msg.edit(content = "jk no one gonna have my number even ma owner wont ;p")
    await msg.delete()


@bot.command() 
async def vote(ctx):
    emoji='👍', '👎'
    for e in emoji:
        await ctx.message.add_reaction(e)





@bot.command()
async def wtf(ctx):
    await ctx.send("https://1.bp.blogspot.com/-8o693FmtIUo/W4qw1dQjshI/AAAAAAAACC8/CY_uwkvWG8U-JtWiWrZWPhPLyCbtywxVACLcBGAs/s320/FB_IMG_15351295134003148.jpg")




@bot.command()
async def avatar(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    roles = [role for role in member.roles]

    embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)

    embed.set_author(name=f"{member}'s avatar:")
    embed.set_image(url=member.avatar_url)

    await ctx.send(embed=embed)





@bot.command()
async def music_help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.green()
    ) 

    embed.set_author(name="music help :", icon_url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.add_field(name="-->join", value="joins ur music channel", inline=True)
    embed.add_field(name="-->leave", value="leaves ur music channel", inline=True)
    embed.add_field(name="-->play {something}", value="plays music", inline=True)
    embed.add_field(name="-->pause", value="pauses the music thats playing", inline=True)
    embed.add_field(name="-->resume", value="continues playing the music after paused", inline=True)
    embed.add_field(name="-->queue", value="shows the queue", inline=True) 
    embed.add_field(name="-->current", value="shows the currently playing music", inline=True)
    embed.add_field(name="-->skip", value="skips the music thats currently playing", inline=True)
    await author.send(embed=embed)
    await ctx.send("successfuly sent to ur dm")
    emoji='👍'
    for e in emoji:
        await ctx.message.add_reaction(e)



@bot.command()
async def api_help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.green()
    ) 

    embed.set_author(name="api help :", icon_url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.add_field(name="-->dog", value="shows a dog gif :3", inline=True)
    embed.add_field(name="-->cat", value="shows a cat gif :3", inline=True)
    embed.add_field(name="-->meme", value="shows a meme", inline=True)
    embed.add_field(name="-->shiba", value="shows a doge pic uwu", inline=True)
    embed.add_field(name="-->dogfact", value="shows a dog fact :p", inline=True)
    embed.add_field(name="-->catfact", value="shows a cat fact :p", inline=True) 
    embed.add_field(name="-->pikachu", value="shows a pikachu pic uwu", inline=True)
    await author.send(embed=embed)
    await ctx.send("successfuly sent to ur dm")
    emoji='👍'
    for e in emoji:
        await ctx.message.add_reaction(e)





@bot.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.green()
    ) 

    embed.set_author(name="help :", icon_url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.add_field(name="-->help moderator", value="shows every command that u need perms to use (e!help_moderator to view)", inline=True)
    embed.add_field(name="-->help fun", value="shows fun commands (e!help_fun to view)", inline=True)
    embed.add_field(name="-->help api", value="shows api commands (e!help_api to view)", inline=True)
    embed.add_field(name="-->help info", value="shows command to check someone's info (e!help_info to view)", inline=True)
    await author.send(embed=embed)
    await ctx.send("successfuly sent to ur dm")
    emoji='👍'
    for e in emoji:
        await ctx.message.add_reaction(e)

@bot.command()
async def help_fun(ctx):
    author = ctx.message.author
    embed = discord.Embed(
        colour = discord.Colour.green()
    )  

    embed.set_author(name="fun help :", icon_url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.set_image(url="https://cdn.discordapp.com/attachments/525781033241673729/545991739865956389/2019-02-15_09_35_52-Window.png")
    embed.add_field(name="-->team", value="team with the bot (do i have to say what it does?)", inline=True)
    embed.add_field(name="-->nothing", value="theres tottaly nothing in here", inline=True)
    embed.add_field(name="-->meme", value="shows a meme", inline=True)
    embed.add_field(name="-->gay", value="says how gay u are", inline=True)
    embed.add_field(name="-->kill", value="kills someone :p", inline=True)
    embed.add_field(name="-->respect", value="press f to pay respect", inline=True)
    embed.add_field(name="-->slots", value="gamble m8 (iconomy gonna work on it soon >:o)", inline=True)
    embed.add_field(name="-->flip coin", value="heads or tails :p", inline=True)
    embed.add_field(name="-->8ball {something}", value="ask it a certain question and it will give an answer (yes or no questions)", inline=True)
    await author.send(embed=embed)
    await ctx.send("successfuly sent to ur dm")
    emoji='👍'
    for e in emoji:
        await ctx.message.add_reaction(e)




async def play_():
        await bot.wait_until_ready()
        while not bot.is_closed():
            a = 0
            for i in bot.guilds:
                for u in i.members:
                    if u.bot == False:
                        a = a + 1

            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="with everyone"))
            await asyncio.sleep(5)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name="to everyone's secrets"))
            await asyncio.sleep(5)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="ur mom"))
            await asyncio.sleep(5)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} taking a shower"))
            await asyncio.sleep(5)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"everyone's mom having sex"))
            


bot.loop.create_task(play_())
with open(r'C:\Users\golde\OneDrive\Bureau\goldenbot\data\config.json') as f:
    r = json.load(f)
bot.run("token")
f.close()
