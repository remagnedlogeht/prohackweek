import discord
import random
from discord.ext import commands
import logging
import traceback
from datetime import datetime
import asyncio
import os
import aiohttp
from discord import opus
from asyncio import sleep
import datetime
import json


class Fun(commands.Cog):
        def __init__(self, bot):
                self.bot = bot

        @commands.command()
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def kill(self, ctx, member: discord.Member=None):
            if member is None:
                await ctx.send(':gun: | **You died! Tag a user to kill him/her!**')
            if member is ctx.me:
                return await ctx.send('nope.')
            if member is ctx.author:
                return await ctx.send(':gun: | **You died! Tag a user to kill him/her!**')
            if member is not None:
                await ctx.send(random.choice([f':gun: | **{ctx.author.mention} wanted to kill {member.mention} just as he stumbled and struck his head with a stone**', f':gun: | **{member.mention} died from a murderer**', f':gun: | **{member.mention} gave too much rage to Clash Royale until he fainted and died**', f':gun: | **{member.mention} was pushed by {ctx.author.mention} from the 5th floor and died**', f':gun: **{member.mention}, The pregnancy of the table just fell asleep and caught fire**', f':gun: | **{member.mention} was shot by {ctx.author.mention}**', f':gun: **After a hard attempt to kill him {member.mention} , {ctx.author.mention} was arrested**']))

        @commands.command(name='8ball')
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def lball(self, ctx, question = None):
               if question is None:
                       return await ctx.send('<:RaluvyQuestion:489805105764499467> | **Please put a question!**')
               if question is not None:
                       await ctx.send(random.choice(['● It is certain.', '● It is decidedly so.', '● Without a doubt.', '● Yes - definitely.', '● You may rely on it', '● As I see it, yes.', '● Most likely.', '● Outlook good.', '● Yes.', '● Signs point to yes.', '● Reply hazy, try again', '● Ask again later.', '● Better not tell you now.', '● Cannot predict now.', '● Concentrate and ask again.', '● Don`t count on it.', '● My reply is no.', '● My sources say no', '● Outlook not so good.', '● Very doubtful.' ]))

        @commands.command()
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def respect(self, ctx):
            em = discord.Embed(title="", description="", color=discord.Colour.blue())
            em.set_author(name="")
            em.add_field(name=f"{ctx.author.name}", value='Press :regional_indicator_f: to pay respect', inline=True)
            msg = await ctx.send(embed=em)
            await msg.add_reaction('\N{regional indicator symbol letter f}')

        @commands.command(aliases=['slot'])
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def slots(self, ctx):
              t = await ctx.send('Spinning...')
              await asyncio.sleep(1)
              a = (random.choice(['------------------\n:soccer: : :tangerine: : :chocolate_bar:\n:potato: : :chocolate_bar: : :watermelon:<\n:tangerine: : :soccer: : :seven:\n------------------\n\n**You Lose! :(**', '------------------\n:soccer: : :tangerine: : :seven:\n:chocolate_bar: : :chocolate_bar: : :chocolate_bar:<\n:soccer: : :watermelon: : :seven:\n------------------\n\n**You Win! :D**', '------------------\n:chocolate_bar: : :soccer: : :potato:\n:seven: : :seven: : :seven:<\n:soccer: : :chocolate_bar: : :watermelon:\n------------------\n\n**You Win! :D**', '------------------\n:chocolate_bar: : :potato: : :soccer:\n:potato: : :tangerine: : :seven:<\n:soccer: : :chocolate_bar: : :tangerine:\n------------------\n\n**You Lose! :(**']))
              await t.edit(content=a)

        @commands.command(aliases=['howgay'])
        @commands.cooldown(1, 3, commands.BucketType.user)
        async def gay(self, ctx, member: discord.Member=None):
             a = random.randint(0, 101)
             if member is None:
                    member = (ctx.author)
             embed = discord.Embed(color=0xe67e22)
             embed.add_field(name=f"Is {member.name} gay?", value=f"**{a}%** gay! :gay_pride_flag:", inline=False)
             await ctx.send(embed=embed)


        @commands.command(aliases=['flipcoins'])
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def flipcoin(self, ctx):
            a = (ctx.author.mention)
            msg = await ctx.send('Flipping...')
            await asyncio.sleep(1.5)
            await msg.edit(content=random.choice([f"{a}, **Heads!**", f"{a}, **Tails!**"]))

def setup(bot):
        bot.add_cog(Fun(bot))