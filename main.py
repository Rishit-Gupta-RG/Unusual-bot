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
from urllib.parse import quote_plus
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



bot = commands.Bot(command_prefix="!", test_guilds=[764549036090720267])

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

@bot.user_command(name="Avatar")  # optional
async def avatar(inter: disnake.ApplicationCommandInteraction, user: disnake.User):
    emb = disnake.Embed(title=f"{user}'s avatar")
    emb.set_image(url=user.display_avatar.url)
    await inter.response.send_message(embed=emb)

@bot.message_command(name="Reverse")  # optional
async def reverse(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    # Let's reverse it and send back
    await inter.response.send_message(message.content[::-1])

class Google(disnake.ui.View):
    def __init__(self, query: str):
        super().__init__()
        # we need to quote the query string to make a valid url. Discord will raise an error if it isn't valid.
        query = quote_plus(query)
        url = f"https://www.google.com/search?q={query}"

        # Link buttons cannot be made with the decorator
        # Therefore we have to manually create one.
        # We add the quoted url to the button, and add the button to the view.
        self.add_item(disnake.ui.Button(label="Click Here", url=url))
async def google(ctx: commands.Context, *, query: str):
    """Returns a google link for a query"""
    await ctx.send(f"Google Result for: `{query}`", view=Google(query))

@bot.event
async def on_ready():
    print('Bot is ready')

bot.run(os.getenv("TOKEN"))