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


class API(commands.Cog):
        def __init__(self, bot):
                self.bot = bot




        @commands.command(aliases=['shibainu'])
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def shiba(self, ctx):
                async with aiohttp.ClientSession() as cs:
                        async with cs.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=false') as r:
                                res = await r.json()
                                embed = discord.Embed(color=0x000000)
                                embed.title = "Awww, a doge!"
                                embed.set_image(url=str(res).strip("[']"))
                                embed.set_footer(text=f"{self.bot.user.name}")
                                embed.timestamp = datetime.datetime.utcnow()
                                await ctx.send(embed=embed)




        @commands.command(aliases=['woof'])
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def dog(self, ctx):
                async with aiohttp.ClientSession() as cs:
                        async with cs.get("http://random.dog/woof.json") as r:
                                res = await r.json()
                                embed = discord.Embed(color=0x000000)
                                embed.title = '\U0001f436 Woof!'
                                embed.set_image(url=res['url'])
                                embed.set_footer(text=f"{self.bot.user.name}")
                                embed.timestamp = datetime.datetime.utcnow()
                                await ctx.send(embed=embed)



        @commands.command(aliases=['meow'])
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def cat(self, ctx):
                async with aiohttp.ClientSession() as cs:
                        async with cs.get('https://some-random-api.ml/img/cat') as r:
                                res = await r.json()
                                embed = discord.Embed(color=0x000000)
                                embed.title = "\U0001f431 Meoww...!"
                                embed.set_image(url=res['link'])
                                embed.set_footer(text=f"{self.bot.user.name}")
                                embed.timestamp = datetime.datetime.utcnow()
                                await ctx.send(embed=embed)

        
        @commands.command()
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def meme(self, ctx):
                async with aiohttp.ClientSession() as cs:
                        async with cs.get("https://some-random-api.ml/meme") as r:
                                res = await r.json()
                                embed = discord.Embed(color=discord.Colour.red())
                                embed.title = res['caption']
                                embed.set_image(url=res['image'])
                                embed.set_footer(text=f"{self.bot.user.name}")
                                embed.timestamp = datetime.datetime.utcnow()
                                await ctx.send(embed=embed)
                                


                                                        
        @commands.command(aliases=['pika'])
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def pikachu(self, ctx):
                async with aiohttp.ClientSession() as cs:
                        async with cs.get("https://some-random-api.ml/pikachuimg") as r:
                                res = await r.json()
                                embed = discord.Embed(color=discord.Colour.red())
                                embed.title = 'Pika!'
                                embed.set_image(url=res['link'])
                                embed.set_footer(text=f"{self.bot.user.name}")
                                embed.timestamp = datetime.datetime.utcnow()
                                await ctx.send(embed=embed)
                                
        @commands.command(aliases=['catfact'])
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def catfacts(self, ctx):
                async with aiohttp.ClientSession() as cs:
                        async with cs.get("https://some-random-api.ml/facts/cat") as r:
                                res = await r.json()
                                await ctx.send(f":cat: **Did you know?**\n{res['fact']}")
                                               
        @commands.command(aliases=['dogfact'])
        @commands.cooldown(1, 5, commands.BucketType.user)
        async def dogfacts(self, ctx):
                async with aiohttp.ClientSession() as cs:
                        async with cs.get("https://some-random-api.ml/facts/dog") as r:
                                res = await r.json()
                                await ctx.send(f":dog: **Did you know?**\n{res['fact']}")







def setup(bot):
        bot.add_cog(API(bot))