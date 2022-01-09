from logging import fatal
from typing import Union
import disnake
from disnake import channel
from disnake import embeds
from disnake.embeds import Embed
import asyncio
from disnake.ext import commands
import aiohttp 
import datetime
from datetime import timedelta
import time
import re
import sys
import os
from dotenv import load_dotenv
load_dotenv()
import youtube_dl
import random
from disnake import Member
from disnake.ext.commands import has_permissions, MissingPermissions
from urllib import parse, request
from disnake.ext.commands.bot import Bot
from disnake.ext.commands.converter import EmojiConverter
from disnake.ext.commands.core import command
from disnake.utils import get
from disnake import TextChannel
from youtube_dl import YoutubeDL
import json
import contextlib
import io
import datetime, time
import psutil
from datetime import timedelta



bot = commands.Bot(command_prefix="!")

@bot.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")

@bot.command()
@disnake.ext.commands.has_permissions(manage_nicknames=True)
async def timeout(ctx, member: disnake.Member,time, *, reason=None) -> None:
    time_convert = {'s' : 1 , 'm' : 60 , 'h' : 3600 , 'd' : 86400}
    timeout_time = float(time[0:len(time)-1]) * time_convert[time[-1]]
    await member.timeout(duration=timeout_time, reason=reason)
    await ctx.send(f"{member.mention} has been timed out by {ctx.author.mention} for {time}.\n **Reason -** {reason}")

@bot.slash_command()
async def test(inter):
    await inter.response.send_message("Monke")

@bot.event
async def on_ready():
    print('Bot is ready')

bot.run(os.getenv("TOKEN"))