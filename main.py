from logging import fatal
import disnake
from disnake import channel
from disnake import embeds
from disnake.embeds import Embed
import asyncio
from disnake.ext import commands
import aiohttp 
import datetime
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
async def timeout(ctx, member: disnake.Member, time: float = None, *, reason=None) -> None:
    await member.timeout(duration=time, reason=reason)
    await ctx.send(f"{member.mention} has been timed out for {time} seconds, With the reason of {reason}")


@bot.event
async def on_ready():
    print('Bot is ready')

bot.run(os.getenv("TOKEN"))