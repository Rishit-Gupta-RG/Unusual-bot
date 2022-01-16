from cProfile import label
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
from disnake.ext.commands import cooldown, BucketType
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
from datetime import datetime

intents = disnake.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix="!", test_guilds=[764549036090720267], intents=intents)

@bot.command(name="ping", description="Shows bot latency.")
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "**This command is on cooldown!**, try again in {:.2f}s".format(error.retry_after)
        await ctx.send(msg)

@bot.slash_command(name="Timeout", description="Timeout a user.")
@disnake.ext.commands.has_permissions(manage_nicknames=True)
async def timeout(ctx, member: disnake.Member,time, *, reason=None) -> None:
    time_convert = {'s' : 1 , 'm' : 60 , 'h' : 3600 , 'd' : 86400}
    timeout_time = float(time[0:len(time)-1]) * time_convert[time[-1]]
    await member.timeout(duration=timeout_time, reason=reason)
    await ctx.send(f"{member.mention} has been timed out by {ctx.author.mention} for {time}.\n **Reason -** {reason}")

@bot.slash_command(name="Remove-Time-Out", description="Removes a user from timeout")
@disnake.ext.commands.has_permissions(manage_nicknames=True)
async def rto(ctx, member: disnake.Member, reason=None) -> None:
    await member.timeout(duration=None)
    await ctx.send(f"Timeout for {member.mention} has been removed by {ctx.author.mention}.\n**Reason -** {reason}")


@bot.slash_command()
async def test(ctx):
    await ctx.send("Monke")

@bot.user_command(name="Avatar")  # optional
async def avatar(inter: disnake.ApplicationCommandInteraction, user: disnake.User):
    emb = disnake.Embed(title=f"{user}'s avatar", color=inter.author.color)
    emb.set_image(url=user.display_avatar.url)
    await inter.response.send_message(embed=emb)

@bot.user_command(name="Info")
async def info(inter: disnake.ApplicationCommandInteraction, member: disnake.User):
    embed=disnake.Embed(title="User Information",colour=inter.author.color)
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="Name", value=member.name)
    embed.add_field(name="Nickname", value=member.nick)
    embed.add_field(name="ID", value=member.id)
    embed.add_field(name="Account Created",value=member.created_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))
    embed.add_field(name="Joined",value=member.joined_at.strftime("%a %#d %B %Y, %I:%M %p UTC"))
    members = sorted(inter.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Status", value=member.status)
    await inter.response.send_message(embed=embed)

@bot.command()
@commands.cooldown(1,35,commands.BucketType.guild)
async def spam(ctx, Amount : int, *, Message=None):
    if ctx.channel.id == 917866202968236052 or ctx.channel.permissions_for(ctx.author).administrator:
        limit = 25
    if Amount > limit:
        await ctx.send(f":negative_squared_cross_mark: **The amount provided `{Amount}` is too big! It needs to be less then {limit}.**")
        return
    else:
        for _ in range(Amount): 
            await ctx.send(Message)

@bot.message_command(name="Reverse")  # optional
async def reverse(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    # Let's reverse it and send back
    await inter.response.send_message(message.content[::-1])


@bot.command(name="Google", description="Provides a google redirect button for the provided query.")
async def google(ctx: commands.Context, *, query: str):
    button = disnake.ui.Button
    view = disnake.ui.View()
    query = quote_plus(query)
    url = f"https://www.google.com/search?q={query}"
    view.add_item(button(label="Click here", url=url))
    await ctx.send(f"Google Result for: `{query}`", view=view)

@bot.listen('on_command_error')
async def error_handler(ctx, error):
    raise error

@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.streaming, name="The Monke Game", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    print('Bot is ready')

bot.run(os.getenv("TOKEN"))