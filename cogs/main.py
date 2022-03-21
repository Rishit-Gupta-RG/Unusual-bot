from ast import alias
from cProfile import label
from email import message
from faulthandler import disable
from logging import fatal
from multiprocessing import context
from operator import inv
from pydoc import describe
from secrets import choice
from typing import List, Union, Optional
import disnake
from disnake import ChannelType, Guild, Option, OptionType, SlashCommand, VoiceState, channel
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
from disnake import Option, OptionType
import importlib
import subprocess
import copy
from collections import Counter
import inspect
from typing import Union, Optional
from contextlib import redirect_stdout
from disnake.enums import TextInputStyle
from inspect import getsource

intents = disnake.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix="!", test_guilds=[764549036090720267], intents=intents, case_insensitive=True)

initial_extensions = ['cogs.test']
bot.load_extension('jishaku')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.command(name="ping", description="Shows bot latency.")
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")


@bot.command(name="evaluate", aliases=["e", "eval"], description="Runs a python script.")
async def evaluate(ctx, *, code):
    str_obj = io.StringIO()
    try:
        with contextlib.redirect_stdout(str_obj):
            exec(code)
    except Exception as e:
        return await ctx.send(f"```{e.__class__.__name__}: {e}```")
    await ctx.send(f'```{str_obj.getvalue()}```')


@bot.command(name="timeout", description="Timeout a user.", aliases=['mute'])
@disnake.ext.commands.has_permissions(manage_nicknames=True)
async def timeout(ctx, member: disnake.Member,time, *, reason=None) -> None:
    time_convert = {'s': 1 , 'm' : 60 , 'h' : 3600 , 'd' : 86400, 'S' : 1, 'M' : 60, 'H' : 3600, "D" : 86400}
    timeout_time = float(time[0:len(time)-1]) * time_convert[time[-1]]
    await member.timeout(duration=timeout_time, reason=reason)
    await ctx.send(f"{member.mention} has been timed out by {ctx.author.mention} for {time}.\n **Reason -** {reason}")

@bot.command(name="Remove-Time-Out", description="Removes a user from timeout", aliases=["rto"])
@disnake.ext.commands.has_permissions(manage_nicknames=True)
async def rto(ctx, member: disnake.Member, *,reason=None) -> None:
    await member.timeout(duration=None)
    await ctx.send(f"Timeout for {member.mention} has been removed by {ctx.author.mention}.\n**Reason -** {reason}")

@bot.command(pass_context=True, aliases=['sn', 'setnick', "nickname"], description="Changes nickname of member.")
@disnake.ext.commands.has_permissions(manage_nicknames=True)
async def nick(ctx, member: disnake.Member,*, nick):
    await member.edit(nick=nick)
    await ctx.send(f'✅ **Nickname was changed for {member.mention}.**')

bot.messages = 0
@bot.listen()
async def on_message(message):
    bot.messages += 1
    if bot.messages == 50:
        ok = ['ok','🆗', 'ok and?', 'okay so?', '...', 'didn\'t ask', 'don\'t care', 'your mom', 'didn\'t ask + don\'t care']
        await message.reply(random.choice(ok), mention_author=False)
        bot.messages = 0

meme_channel = 852926176514670632
@bot.listen()
async def on_message(message):
    if message.attachments and message.channel.id == int(meme_channel):
        await message.add_reaction('🔼')
        await message.add_reaction('🔽')

@bot.listen()
async def on_message(message):
    if message.channel.id == 852926176514670632:
         if "https://" in message.content:
            await message.add_reaction('🔼')
            await message.add_reaction('🔽')
            
@bot.slash_command(description="Monke")
async def test(ctx):
    await ctx.send("Monke")

@bot.command(name="watch-together",description="Starts watch together activity in a voice channel.")
async def yt(ctx, channel: Optional[disnake.VoiceChannel]):
    channel = ctx.author.VoiceState.channel
    if channel != None:
        invite = await channel.create_invite(
        target_type=disnake.InviteTarget.embedded_application, 
        target_application=disnake.PartyType.watch_together)
        await ctx.send(invite)
    else:
        await ctx.send("❎ You are not in a voice channel!")

@bot.command(name="gaming", description="Pings Gaming role.")
async def gaming(ctx):
    role = ctx.guild.get_role(935094470423240764)
    if role in ctx.author.roles:
        await ctx.send("<@&935094470423240764>")
    else:
        await ctx.send("Sorry I cannot ping gaming role for because you do not have it yourself, you can get it by typing `?role Gaming` in <#889231397351460894>.")

#@bot.slash_command(name="chess-in-the-park",description="Starts chess in the park activity in a voice channel.")
#async def chess(ctx, channel: disnake.VoiceChannel):
#    invite = await channel.create_invite(target_type=disnake.InviteTarget.embedded_application, target_application=disnake.PartyType.chess)
#    await ctx.send([f"[Click to open Chess in the park in {channel}]({invite})"])

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
    embed.add_field(name="Account Created",value=disnake.utils.format_dt(member.created_at, style="F"))
    embed.add_field(name="Joined",value=disnake.utils.format_dt(member.joined_at, style="F"))
    members = sorted(inter.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Status", value=member.status)
    await inter.response.send_message(embed=embed)

@bot.message_command()
async def Quote(inter, message: disnake.Message):
    msg_link = f'https://discord.com/channels/{inter.guild.id}/{inter.channel.id}/{message.id}'
    embed = disnake.Embed(description=f"[Jump to message ►][{msg_link}]\n {message.content}",color=inter.author.color, timestamp=message.created_at)
    embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
    await inter.send(embed=embed)

Party = ['Watch Together', 'chess']

async def autocomplete_langs(inter, string: str) -> List[str]:
    return [lang for lang in Party if string.lower() in lang.lower()]

@bot.slash_command(enabled=False)
async def activity(inter: disnake.CommandInteraction,channel: disnake.VoiceChannel ,Party:  str = commands.Param(autocomplete=autocomplete_langs)):
    if Party == "Watch Together":
        invite = await channel.create_invite(target_type=disnake.InviteTarget.embedded_application, target_application=disnake.PartyType.chess)
        await inter.response(f"[Click to open Watch Together in {channel}]({invite})")
    elif Party == "chess":
        invite = await channel.create_invite(target_type=disnake.InviteTarget.embedded_application, target_application=disnake.PartyType.chess)
        await inter.response(f"[Click to open Chess in {channel}]({invite})")

@bot.command()
@commands.cooldown(1,35,commands.BucketType.guild)
async def spam(ctx, Amount : int, *, Message=None):
    if ctx.channel.id == 917866202968236052 or ctx.channel.permissions_for(ctx.author).administrator:
        if ctx.message.author.id == 787149777103486986:
            limit = 10000
        else:
            limit = 25
    if Amount > limit:
        await ctx.send(f":negative_squared_cross_mark: **The amount provided `{Amount}` is too big! It needs to be less then `{limit}`.**")
        return
    else:
        for _ in range(Amount): 
            await ctx.send(Message)

@bot.message_command(name="Reverse")  # optional
async def reverse(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    # Let's reverse it and send back
    await inter.response.send_message(message.content[::-1])

deletion_list = []
@bot.slash_command(name="delete-add", description="Applies hard delete on a user.", enabled=True)
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def deleteadd(ctx, user: disnake.User):
    """
    Applies hard delete on a user.

    Parameters
    ----------
    user: User to whom hard delete is to be applied
    """
    deletion_list.append(user.id)
    await ctx.send("<:society:932186685926694914>")

@bot.slash_command(name="delete-remove", description="Removes hard delete from a user.",enabled=True)
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def deleteremove(ctx, user: disnake.User):
    """
    Removes hard delete from a user.

    Parameters
    ----------
    user: The user on whom hard delete was applied earlier.
    """
    deletion_list.remove(user.id)
    await ctx.send(f'Removed hard delete from {user}')

@bot.listen()
async def on_message(msg):
    if msg.author.id in deletion_list:
        await msg.delete()

@bot.command(name="Google", description="Provides a google redirect button for the provided query.")
async def google(ctx: commands.Context, *, query: str):
    button = disnake.ui.Button
    view = disnake.ui.View()
    query = quote_plus(query)
    url = f"https://www.google.com/search?q={query}"
    view.add_item(button(label="Click here", url=url))
    await ctx.send(f"Google Result for: `{query}`", view=view)

@bot.command()
@disnake.ext.commands.has_permissions(ban_members=True)
async def ban(ctx, member: disnake.Member):
    message = await ctx.send(f"kardu? (y/n)")
    check = lambda m: m.author == ctx.author and m.channel == ctx.channel

    try:
        confirm = await ctx.bot.wait_for("message", check=check, timeout=30)
    except asyncio.TimeoutError:
        await message.edit(content="Ban cancelled, timed out.")
        return

    if confirm.content == "y":
        await member.ban()
        await message.edit(content=f"{member} has been banned.")
        return

    await message.edit(content="Ban cancelled.")

snipe_message_author = {}
snipe_message_content = {}

@bot.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await asyncio.sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]

@bot.command(name = 'snipe', enabled=False)
async def snipe(ctx):
    channel = ctx.channel
    try: #This piece of code is run if the bot finds anything in the dictionary
        em = disnake.Embed(title= f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id], color=ctx.author.color)
        em.set_footer(text = f"by {snipe_message_author[channel.id]}", icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed = em)
    except KeyError: #This piece of code is run if the bot doesn't find anything in the dictionary
        await ctx.send(f"There are no recently deleted messages in #{channel.name}")


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

# Subclassing the modal.
class MyModal(disnake.ui.Modal):
    def __init__(self):
        # The details of the modal, and its components
        components = [
            disnake.ui.TextInput(
                label="Name",
                placeholder="Your discord Tag",
                custom_id="name",
                style=TextInputStyle.short,
                max_length=50,
            ),
            disnake.ui.TextInput(
                label="Description",
                placeholder="Your thoughts on monkes",
                custom_id="description",
                style=TextInputStyle.paragraph,
            ),
        ]
        super().__init__(
            title="Create Tag",
            custom_id="create_tag",
            components=components,
        )

    # The callback received when the user input is completed.
    async def callback(self, inter: disnake.ModalInteraction):
        embed = disnake.Embed(title="Tag Creation")
        for key, value in inter.text_values.items():
            embed.add_field(
                name=key.capitalize(),
                value=value[:1024],
                inline=False,
            )
        await inter.response.send_message(embed=embed)
    
@bot.slash_command()
async def tags(inter: disnake.AppCmdInter):
    """Sends a Modal to create a tag."""
    await inter.response.send_modal(modal=MyModal())

@bot.group(invoke_without_command=True)
async def tag(ctx):
    embed = disnake.Embed(title="Tag List", description="`code`", color=ctx.author.color)
    await ctx.send(embed=embed)

@tag.command()
async def code(ctx):
    embed = disnake.Embed(title="Code", description="""Here's how to format Python code on Discord:

\`\`\`py
monke = str"monkelife"
print(monke)
\`\`\`

Will give an output like:
```py
monke = str"monkelife"
print(monke)```""", color=ctx.author.color)
    embed.set_footer(text="Note: These are backticks not quotes.")
    await ctx.send(embed=embed)

class EvalCommand:
    def __init__(self):
        pass
    
    def resolve_variable(self, variable):
        if hasattr(variable, "__iter__"):
            var_length = len(list(variable))
            if (var_length > 100) and (not isinstance(variable, str)):
                return f"<a {type(variable).__name__} iterable with more than 100 values ({var_length})>"
            elif (not var_length):
                return f"<an empty {type(variable).__name__} iterable>"
        
        if (not variable) and (not isinstance(variable, bool)):
            return f"<an empty {type(variable).__name__} object>"
        return (variable if (len(f"{variable}") <= 1000) else f"<a long {type(variable).__name__} object with the length of {len(f'{variable}'):,}>")
    
    def prepare(self, string):
        arr = string.strip("```").replace("py\n", "").replace("python\n", "").split("\n")
        if not arr[::-1][0].replace(" ", "").startswith("return"):
            arr[len(arr) - 1] = "return " + arr[::-1][0]
        return "".join(f"\n\t{i}" for i in arr)
    
    @commands.command(pass_context=True, aliases=['eval', 'exec', 'evaluate'])
    @commands.is_owner()
    async def _eval(self, ctx, *, code: str):
        silent = ("-s" in code)
        
        code = self.prepare(code.replace("-s", ""))
        args = {
            "disnake": disnake,
            "sauce": getsource,
            "sys": sys,
            "os": os,
            "imp": __import__,
            "this": self,
            "ctx": ctx
        }
        
        try:
            exec(f"async def func():{code}", args)
            a = time()
            response = await eval("func()", args)
            if silent or (response is None) or isinstance(response, disnake.Message):
                del args, code
                return
            
            await ctx.send(f"```py\n{self.resolve_variable(response)}````{type(response).__name__} | {(time() - a) / 1000} ms`")
        except Exception as e:
            await ctx.send(f"Error occurred:```\n{type(e).__name__}: {str(e)}```")
        
        del args, code, silent

@bot.listen('on_command_error')
async def error_handler(ctx, error):
    raise error

@bot.command()
@commands.is_owner()
async def reboot(ctx):
    await ctx.send("**Rebooting** <a:malloading:922167995961335808>")
    os.system("clear")
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.listen()
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
            return
    elif isinstance(error, commands.MissingPermissions):
        message = "<:notstonks:876167180666949692> You do not have permission to use this command!"
    elif isinstance(error, commands.BadArgument):
        message = f"A bad argument was passed, type `!help {ctx.command}` to see how this works."
    elif isinstance(error, commands.DisabledCommand):
        message = "❎ This command is disabled!"
    elif isinstance(error, commands.TooManyArguments):
        message = f"Too many arguments detected! Type `!help {ctx.command}` to see how this works."
    elif isinstance(error, commands.UserInputError):
        message = f"There's an issue in your input dear, type `!help {ctx.command}` to see how it works."
    elif isinstance(error, commands.MissingRequiredArgument):
        message = f"❎ Missing arguments, type `!help {ctx.command}` to see the proper arguments."
    elif isinstance(error, commands.CommandOnCooldown):
        message = "**This command is on cooldown!**, try again in {:.2f}s".format(error.retry_after)
    elif isinstance(error, commands.NotOwner):
        message = "❎ **Only bot owner can use this command!**"
    
    await ctx.send(message)
    
@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.streaming, name="The Monke Game", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    print('Bot is ready')

bot.run(os.getenv("TOKEN"))
