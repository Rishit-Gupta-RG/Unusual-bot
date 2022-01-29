from ast import alias
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
import traceback
import textwrap
import importlib
import subprocess
import copy
from collections import Counter
import inspect
from typing import Union, Optional
from contextlib import redirect_stdout

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

@bot.command(name="evaluate", aliases=["e", "eval"], description="Runs a python script.")
async def evaluate(ctx, *, code):
    str_obj = io.StringIO()
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'```{str_obj.getvalue()}```')

@bot.command(name="Timeout", description="Timeout a user.")
@disnake.ext.commands.has_permissions(manage_nicknames=True)
async def timeout(ctx, member: disnake.Member,time, *, reason=None) -> None:
    time_convert = {'s' : 1 , 'm' : 60 , 'h' : 3600 , 'd' : 86400}
    timeout_time = float(time[0:len(time)-1]) * time_convert[time[-1]]
    await member.timeout(duration=timeout_time, reason=reason)
    await ctx.send(f"{member.mention} has been timed out by {ctx.author.mention} for {time}.\n **Reason -** {reason}")

@bot.command(name="Remove-Time-Out", description="Removes a user from timeout")
@disnake.ext.commands.has_permissions(manage_nicknames=True)
async def rto(ctx, member: disnake.Member, reason=None) -> None:
    await member.timeout(duration=None)
    await ctx.send(f"Timeout for {member.mention} has been removed by {ctx.author.mention}.\n**Reason -** {reason}")


@bot.slash_command(description="Monke")
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
        else:
            await ctx.send(f"Finished spamming the content {Amount} times: ```{Message}```- Requested by {ctx.author.mention}")

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

class TicTacToeButton(disnake.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=disnake.ButtonStyle.secondary, label="\u200b", row=y)
        self.x = x
        self.y = y

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: disnake.MessageInteraction):
        assert self.view is not None
        view: TicTacToe = self.view
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = disnake.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
            content = "It is now O's turn"
        else:
            self.style = disnake.ButtonStyle.success
            self.label = "O"
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            content = "It is now X's turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = "X won!"
            elif winner == view.O:
                content = "O won!"
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


# This is our actual board View
class TicTacToe(disnake.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: TicTacToeButton
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    # This method checks for the board winner -- it is used by the TicTacToeButton
    def check_board_winner(self):
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # If we're here, we need to check if a tie was made
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


@bot.command()
async def tic(ctx: commands.Context):
    if ctx.message.author.id == 787149777103486986:
        """Starts a tic-tac-toe game with yourself."""
        await ctx.send("Tic Tac Toe: X goes first", view=TicTacToe())
    else:
        await ctx.send("❌ This command is under development, Only bot dev. can use it")

@bot.listen('on_command_error')
async def error_handler(ctx, error):
    raise error

@bot.command()
async def reboot(ctx):
    if ctx.message.author.id == 787149777103486986:   
        await ctx.send("**Rebooting** <a:malloading:922167995961335808>")
        os.system("clear")
        os.execv(sys.executable, ['python'] + sys.argv)
    else:
        await ctx.send("<:_:919194636906561548> **Only bot dev. can use this command!**")

@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.streaming, name="The Monke Game", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    print('Bot is ready')

bot.run(os.getenv("TOKEN"))