from logging import fatal
import discord
from discord import channel
from discord import embeds
from discord.embeds import Embed
import asyncio
from discord.ext import commands
import aiohttp 
import datetime
import time
import re
from discord import Webhook, RequestsWebhookAdapter, File
from discord.ext.commands import cooldown, BucketType
import sys
import os
from dotenv import load_dotenv
import youtube_dl
import random
from discord import Member
from discord.ext.commands import has_permissions, MissingPermissions
from urllib import parse, request
from discord.ext.commands.bot import Bot
from discord.ext.commands.converter import EmojiConverter
from discord.ext.commands.core import command
from discord.utils import get
from discord import TextChannel
from youtube_dl import YoutubeDL
import json
import contextlib
import io
import datetime, time
import psutil

from discord.ext.commands.errors import CheckAnyFailure
load_dotenv()
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "**This command is on cooldown!**, try again in {:.2f}s".format(error.retry_after)
        await ctx.send(msg)

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")

@bot.command()
async def stats(ctx):
    embed = discord.Embed(title="Bot Statistics", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Servers:", value="2", inline=True)
    embed.add_field(name="Users:", value=ctx.guild.member_count, inline=True)
    embed.add_field(name="Channels:", value=len(ctx.guild.channels) + 4, inline=True)
    embed.add_field(name="Prefix:", value="`!`", inline=True)
    embed.add_field(name="CPU Usage:", value=f'{int(psutil.cpu_percent())}%', inline=True)
    embed.add_field(name="Memory Usage:", value=f'{int(psutil.virtual_memory().percent)}%', inline=True)
    embed.add_field(name="Available Memory:", value=f'{int(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)}%', inline=True)
    await ctx.send(embed=embed)

@bot.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title="Unusual Friends", description="Hi this is Unsual Friends bot developed for this discord server! Here's the list of available commands:", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Maths Commands:", value="`add`, `sub`, `multi`, `divide`, `square`", inline=False)
    embed.add_field(name="Browser:", value="`youtube`", inline=False)
    embed.add_field(name="Miscellaneous:", value="`spam`", inline=False)
    embed.add_field(name="Admin only Commands:", value="`kick`, `nick`, `say`", inline=False)
    embed.add_field(name="Bot Utility Commands:", value="`ping`, `stats`", inline=False)
    embed.set_footer(text="My prefix is ! | Type !help command for a breif info of that command")
    
    await ctx.send(embed=embed)

#CALCULATOR
@bot.command(aliases=['sum', "addition"]) 
async def add(ctx,a:float, b:float): 
    await ctx.send(f"{a} + {b} = {a+b}") #Adds A and B

@bot.command(aliases=["subtract", "minus"]) 
async def sub(ctx,a:float,b:float): 
    await ctx.send(f"{a} - {b} = {a-b}") #Subtracts A and B

@bot.command(aliases=["multiply"]) 
async def multi(ctx,a:float,b:float): 
    await ctx.send(f"{a} * {b} = {a*b}") #Multplies A and B

@bot.command() 
async def divide(ctx,a:float,b:float): 
    await ctx.send(f"{a} / {b} = {a/b}") #Divides A and B

@bot.command()
async def square(ctx,a:float):
    await ctx.send(f"{a*a}") #Multilies A by itself

#BROWSER COMMANDS
@bot.command(aliases=["Youtube", "yt", "Yt", "youtubesearch"])
async def youtube(ctx, *, search):
    query_string = parse.urlencode({'search_query': search})
    html_content = request.urlopen('http://www.youtube.com/results?' + query_string)
    search_content= html_content.read().decode()
    search_results = re.findall(r'\/watch\?v=\w+', search_content)
    #print(search_results)
    await ctx.send("Here's what I found" ' ' 'https://www.youtube.com' + search_results[0])

@bot.command()
async def define(ctx, word):
   async with aiohttp.ClientSession() as session:
      request = await session.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}')
      definejson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title=definejson['word'],description=definejson['meanings'] ,color=ctx.author.color)
   embed.add_field(name="Definition:", value=definejson['definition'], inline=False)
   embed.add_field(name="Example:", value=definejson['example'], inline=False)
   await ctx.send(embed=embed)

#ADMIN ONLY
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member):
    await member.kick()
    await ctx.send(f"**{member.name}** has been kicked by **{ctx.author.name}**!")

@bot.command(pass_context=True, aliases=['sn', 'Nick', 'Sn', 'Setnick', 'setnick', "nickname"])
@commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'<:tick:919194526558584864> **Nickname was changed for {member.mention}.**')


#MISC
@bot.command()
@commands.cooldown(1,30,commands.BucketType.guild)
async def spam(ctx, amount : int, *, message=None):
    if ctx.channel.id == 917866202968236052 or ctx.channel.permissions_for(ctx.author).administrator:
        limit = 15
    if amount > limit:
        await ctx.send(f"<:_:919194636906561548> **The amount provided `{amount}` is too big! It needs to be less then 15.**")
        return
    else:
        for _ in range(amount): 
            await ctx.send(message)

@bot.command()
async def eval(ctx, *, code):
    str_obj = io.StringIO() #Retrieves a stream of data
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'```{str_obj.getvalue()}```')

@bot.command()
async def meme(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/meme')
      memejson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Meme",description=memejson['caption'] ,color=ctx.author.color)
   embed.set_image(url=memejson['image'])
   await ctx.send(embed=embed)

@bot.command()
async def joke(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/joke')
      jokejson = await request.json() # Convert it to a JSON dictionary
   await ctx.send(jokejson['joke'])


#ANIMALS
@bot.command()
async def dog(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Doggo!", color=discord.Color.purple())
   embed.set_image(url=dogjson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def dogfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/dog')
        factjson = await request.json()
    embed = discord.Embed(title="Dog Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

@bot.command()
async def fox(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/fox')
      foxjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Fox!", color=discord.Color.purple())
   embed.set_image(url=foxjson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def whale(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/whale')
      whalejson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Whale!", color=discord.Color.purple())
   embed.set_image(url=whalejson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def cat(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      catjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Kitty!", color=discord.Color.purple())
   embed.set_image(url=catjson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def koala(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/koala')
      koalajson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Koala!", color=discord.Color.purple())
   embed.set_image(url=koalajson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def racoon(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/racoon')
      racoonjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Racoon!", color=discord.Color.purple())
   embed.set_image(url=racoonjson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def kangaroo(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/kangaroo')
      kangaroojson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Kangaroo!", color=discord.Color.purple())
   embed.set_image(url=kangaroojson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def birb(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/birb')
      birbjson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Birb!", color=discord.Color.purple())
   embed.set_image(url=birbjson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def panda(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/panda')
      pandajson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Panda!", color=discord.Color.purple())
   embed.set_image(url=pandajson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def redpanda(ctx):
   async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/red_panda')
      red_pandajson = await request.json() # Convert it to a JSON dictionary
   embed = discord.Embed(title="Red Panda!", color=discord.Color.purple())
   embed.set_image(url=red_pandajson['link'])
   await ctx.send(embed=embed)

@bot.command()
async def catfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/cat')
        factjson = await request.json()
    embed = discord.Embed(title="Cat Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

@bot.command()
async def foxfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/fox')
        factjson = await request.json()
    embed = discord.Embed(title="Fox Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

@bot.command()
async def racoonfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/racoon')
        factjson = await request.json()
    embed = discord.Embed(title="Racoon Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

@bot.command()
async def kangaroofact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/kangaroo')
        factjson = await request.json()
    embed = discord.Embed(title="Kangaroo Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

@bot.command()
async def pandafact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/panda')
        factjson = await request.json()
    embed = discord.Embed(title="Panda Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

@bot.command()
async def koalafact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/koala')
        factjson = await request.json()
    embed = discord.Embed(title="Koala Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

@bot.command()
async def whalefact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/whale')
        factjson = await request.json()
    embed = discord.Embed(title="Whale Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

@bot.command()
async def birbfact(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/facts/birb')
        factjson = await request.json()
    embed = discord.Embed(title="Birb Fact",description=factjson['fact'] , color=ctx.author.color)
    await ctx.send(embed=embed)

#ANIME
@bot.command()
async def animequote(ctx):
    async with aiohttp.ClientSession() as session:
        request = await session.get('https://some-random-api.ml/animu/quote')
        quotejson = await request.json()
    embed = discord.Embed(title="Anime quote",description=quotejson['sentence'] , color=ctx.author.color)
    embed.set_author(name=quotejson['anime'])
    embed.set_footer(text=quotejson['character'])
    await ctx.send(embed=embed)


@bot.command()
async def say(ctx, *, message):
    channel = bot.get_channel(853143136620904518)
    await channel.send(message)

#WELCOME
@bot.event
async def on_member_join(member):
    welcomechannel = await bot.fetch_channel(908296505876688958)
    await welcomechannel.send(f"Hello {member.mention} :wave:\nWelcome to Unusual Friends ❤\n\n- <#809297410979397663> - read the server rules\n- <#850694848323256360> - pick up roles\n- <#900106358823739442> - verify yourself\n- <#908002039907373108> - check out all the channels")


#HELP SUB-COMMANDS
@help.command()
async def add(ctx):
    embed = discord.Embed(title="Add", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value="Adds 2 numbers. Numbers can be integers & decimals as well.", inline=False)
    embed.add_field(name="Usage: ", value="!add *number1* *number2*", inline=False)
    embed.add_field(name="Aliases:", value="`sum`, `add`, `addition`", inline=False)
    embed.add_field(name="Examples:", value="!add 25 68\n !add 25 0.38\n !add 0.25 0\n !add 0.25 0.38", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def sub(ctx):
    embed = discord.Embed(title="Subtract", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value="Subtracts 2 numbers. Numbers can be integers & decimals as well.", inline=False)
    embed.add_field(name="Usage: ", value="!sub *number1* *number2*", inline=False)
    embed.add_field(name="Aliases:", value="`sub`, `subtract`, `minus`", inline=False)
    embed.add_field(name="Examples:", value="!sub 25 68\n !sub 25 0.38\n !sub 0.25 0\n !sub 0.25 0.38", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def multi(ctx):
    embed = discord.Embed(title="Multiply", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value="Multiplies 2 numbers. Numbers can be integers & decimals as well.", inline=False)
    embed.add_field(name="Usage: ", value="!multi *number1* *number2*", inline=False)
    embed.add_field(name="Aliases:", value="`multiply`, `multi`", inline=False)
    embed.add_field(name="Examples:", value="!multi 25 68\n !multi 25 0.38\n !multi 0.25 0\n !multi 0.25 0.38", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def divide(ctx):
    embed = discord.Embed(title="Divide", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value="Divides 2 numbers. Numbers can be integers & decimals as well.", inline=False)
    embed.add_field(name="Usage: ", value="!divide *number1* *number2*", inline=False)
    embed.add_field(name="Aliases:", value="`divide`", inline=False)
    embed.add_field(name="Examples:", value="!divide 25 68\n !divide 25 0.38\n !divide 0.25 0\n !divide 0.25 0.38", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def square(ctx):
    embed = discord.Embed(title="Square", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value="Calculates square of a number.", inline=False)
    embed.add_field(name="Usage: ", value="!square *number*", inline=False)
    embed.add_field(name="Aliases:", value="`square`", inline=False)
    embed.add_field(name="Examples:", value="!square 25\n !square 0.5", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def youtube(ctx):
    embed = discord.Embed(title="YouTube", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value="Searches on YouTube for the provided query!", inline=False)
    embed.add_field(name="Usage:", value="!youtube *query*", inline=False)
    embed.add_field(name="Aliases:", value="`youtube`, `yt`, `youtubesearch`", inline=False)
    embed.add_field(name="Examples:", value="!youtube Rickroll video HD quality", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def nick(ctx):
    embed = discord.Embed(title="Nick", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value='Changes nickname of the user\n **Note:** Use "quotes" if nickname contains 2 or more words.', inline=False)
    embed.add_field(name="Usgae:", value='!nick *@user* *"new nick"*\n !nick *@user* *new_nick*', inline=False)
    embed.add_field(name="Aliases", value="`nick`, `sn`, `setnick`", inline=False)
    embed.add_field(name="Examples:", value='!nick <@560838833680154624> "Cheap Monke"\n !sn <@727526184161902614> Monke\n !setnick <@787149777103486986> "Pro Monke ji"\n !nick <@764497721389350963> "Strange Monke"', inline=False)
    await ctx.send(embed=embed)

@help.command()
async def spam(ctx):
    embed = discord.Embed(title="Spam", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value="Spams the argument for given number of times. Only **15** messages can be spammed at once.\n **Note:** This command has a guild cooldown of **30 seconds**", inline=False)
    embed.add_field(name="Usage:", value="!spam *number* *sentence*", inline=False)
    embed.add_field(name="Aliases", value="`spam`", inline=False)
    embed.add_field(name="Examples:", value="!spam 10 Leave humanity return to Monke\n !spam 5 <:monkelife:853888327471333386> <:monkelife:853888327471333386> <:monkelife:853888327471333386>\n !spam 15 Noice", inline=False)
    await ctx.send(embed=embed)

@help.command()
async def ping(ctx):
    embed = discord.Embed(title="Ping", color = ctx.author.color)
    embed.set_author(name= "Unusual Friends#3075", icon_url="https://images-ext-1.discordapp.net/external/0k2KhTElwr7ki38RUYVAAsCKjwPZ5wP32DFQpt37k2M/%3Fsize%3D2048/https/cdn.discordapp.com/avatars/835206086570803211/d7c4dbb2521c985489e973aea0cb5a2e.png?width=473&height=473")
    embed.add_field(name="Description:", value="Shows bot latency.", inline=False)
    embed.add_field(name="Usage:", value="!ping", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def restart(ctx):
    if ctx.message.author.id == 787149777103486986:   
        await ctx.send("**Rebooting** <a:malloading:922167995961335808>")
        os.system("clear")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.send("<:_:919194636906561548> **Only bot dev. can use this command!**")
    

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you all procrastinate"))
    print('Bot is ready.')

bot.run(os.getenv("TOKEN"))