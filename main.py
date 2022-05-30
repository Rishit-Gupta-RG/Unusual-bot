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
from unicodedata import name
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
import json
import contextlib
import io
import datetime, time
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
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned, test_guilds=[764549036090720267], intents=intents, case_insensitive=True)

bot.load_extension('jishaku')

#PREFIX BASED
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
#------------------------------------------------------------------------------------------------------

#SLASH COMMANDS
@bot.slash_command(name="timeout", description="Timeout a user.")
@commands.check_any(commands.has_role(787149777103486986), commands.has_permissions(administrator=True))
async def timeout(inter: disnake.CommandInteraction, member: disnake.Member,time, *, reason=None) -> None:
    """
    Parameters
    ----------

    member: The user to timeout
    time: How long they should be timed out for
    reason: Reason for timeout
    """
    time_convert = {'s': 1 , 'm' : 60 , 'h' : 3600 , 'd' : 86400, 'S' : 1, 'M' : 60, 'H' : 3600, "D" : 86400}
    timeout_time = float(time[0:len(time)-1]) * time_convert[time[-1]]
    await member.timeout(duration=timeout_time, reason=reason)
    await inter.response.send_message(f"{member.mention} has been timed out by {inter.author.mention} for {time}.\n **Reason -** {reason}")

@bot.slash_command(name="remove-timeout", description="Removes a user from timeout", aliases=["rto"])
@commands.check_any(commands.has_role(787149777103486986), commands.has_permissions(administrator=True))
async def rto(inter: disnake.CommandInteraction, member: disnake.Member, *,reason=None) -> None:
    """
    Parameters
    ----------
    
    member: The user to remove timeout
    reason: Reason for remove-timeout
    """
    await member.timeout(duration=None)
    await inter.response.send_message(f"Timeout for {member.mention} has been removed by {inter.author.mention}.\n**Reason -** {reason}")

@bot.slash_command(description="Changes nickname of member.")
@commands.check_any(commands.has_role(787149777103486986), commands.has_permissions(administrator=True))
async def nick(inter: disnake.CommandInteraction, member: disnake.Member,*, nick: str):
    """
    Parameters
    ----------
    
    member: Member to change their nick
    nick: New nickname
    """
    await member.edit(nick=nick)
    await inter.response.send_message(f'\✅ **Nickname was changed for {member.mention}.**')

Party = ['Watch Together', 'chess']

async def autocomplete_langs(inter, string: str) -> List[str]:
    return [lang for lang in Party if string.lower() in lang.lower()]

@bot.slash_command(name="activity", description="[BETA COMMAND] Starts voice channel activity.")
async def activity(inter: disnake.CommandInteraction,channel: disnake.VoiceChannel ,party:  str = commands.Param(autocomplete=autocomplete_langs)):
    """
    Parameters
    ----------
    
    channel: The voice channel for activity
    party: Select a party type from the above list only
    """
    if party == "Watch Together":
        invite = await channel.create_invite(target_type=disnake.InviteTarget.embedded_application, target_application=disnake.PartyType.chess)
        await inter.response.send_message(f"[Click to open Watch Together in {channel}]({invite})")
    elif Party == "chess":
        invite = await channel.create_invite(target_type=disnake.InviteTarget.embedded_application, target_application=disnake.PartyType.chess)
        await inter.response.send_message(f"[Click to open Chess in {channel}]({invite})")
    else:
        await inter.response.send_message(f"Please choose an activity from the autocomplete only!", ephemeral=True)

ANIMALS = ["Panda", "Dog", "Cat", "Fox", "Red panda", "Koala", "Bird", "Racoon", "Kangaroo", "Whale", "Pikachu"]
async def autocomp_animals(inter: disnake.CommandInteraction, user_input: str):
    return [lang for lang in ANIMALS if user_input.lower() in lang]
FACT_ANIMALS = ["Panda", "Dog", "Cat", "Fox", "Red panda", "Koala", "Bird", "Racoon", "Kangaroo", "Whale", "Pikachu"]
async def autocomp_animalfact(inter: disnake.CommandInteraction, user_input: str):
    return [lang for lang in FACT_ANIMALS if user_input.lower() in lang]

@bot.slash_command()
async def animal(inter):
    pass

@animal.sub_command(description="Sends a picture of selected animal.")
async def image(inter: disnake.CommandInteraction, animal: str = commands.Param(autocomplete=autocomp_animals)):
    """
    Sends a picture of selected animal.
    
    Parameters
    ----------
    animal: Select an animal to see its picture.
    """
    if animal in ("Panda", "Dog", "Cat", "Fox","Koala", "Bird", "Racoon", "Kangaroo", "Whale", "Pikachu"):
        k = animal.lower()
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://some-random-api.ml/img/{k}')
            whalejson = await request.json()
        embed = disnake.Embed(title=f"{animal}!", color=inter.author.color)
        embed.set_image(url=whalejson['link'])
        await inter.response.send_message(embed=embed)
    elif animal == "Red Panda":
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://some-random-api.ml/img/red_panda')
            whalejson = await request.json()
        embed = disnake.Embed(title=f"{animal}!", color=inter.author.color)
        embed.set_image(url=whalejson['link'])
        await inter.response.send_message(embed=embed)
    else:
        await inter.response.send_message("Select animal from autocomplete only!", ephemeral=True)

@animal.sub_command(description="Sends a random fact of selected animal.")
async def fact(inter: disnake.CommandInteraction, animal: str = commands.Param(autocomplete=autocomp_animalfact)):
    """
    Sends a random fact of selected animal.
    
    Parameters
    ----------
    animal: Select an animal to see its fact.
    """
    if animal in ("Panda", "Dog", "Cat", "Fox","Koala", "Bird", "Racoon", "Kangaroo", "Whale"):
        k = animal.lower()
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://some-random-api.ml/facts/{k}')
            whalejson = await request.json()
        embed = disnake.Embed(title=f"{animal} Fact!",description=whalejson['fact'],color=inter.author.color)
        await inter.response.send_message(embed=embed)
    elif animal == "Red Panda":
        async with aiohttp.ClientSession() as session:
            request = await session.get(f'https://some-random-api.ml/facts/red_panda')
            whalejson = await request.json()
        embed = disnake.Embed(title=f"{animal} Fact!",description=whalejson['fact'],color=inter.author.color)
        await inter.response.send_message(embed=embed)
    else:
        await inter.response.send_message("Select animal from autocomplete only!", ephemeral=True)

@bot.command()
@commands.cooldown(1,35,commands.BucketType.guild)
async def spam(ctx, Amount : int, *, Message=None):
    if ctx.channel.id == 917866202968236052 or ctx.channel.permissions_for(ctx.author).administrator:
        if ctx.message.author.id == 787149777103486986:
            limit = 10000
        elif ctx.message.author.id == 764497721389350963:
            limit = 250
        else:
            limit = 25
    if Amount > limit:
        await ctx.send(f":negative_squared_cross_mark: **The amount provided `{Amount}` is too big! It needs to be less then `{limit}`.**")
        return
    else:
        for _ in range(Amount): 
            await ctx.send(Message)

deletion_list = []
@bot.slash_command(name="delete-add", description="Applies hard delete on a user.", enabled=True)
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def deleteadd(inter: disnake.CommandInteraction, user: disnake.User):
    """
    Applies hard delete on a user.

    Parameters
    ----------
    user: User to whom hard delete is to be applied.
    """
    deletion_list.append(user.id)
    await inter.response.send_message("<:society:932186685926694914>")

@bot.slash_command(name="verify", description="Verifies a new member.")
@commands.has_permissions(manage_nicknames=True)
async def verify(inter: disnake.CommandInteraction, member: disnake.Member):
    """
    Parameters
    ----------
    
    member: Member to verify
    """
    uner = inter.guild.get_role(882503122554093589)
    if uner in member.roles:
        await member.remove_roles(uner)
        await inter.response.send_message(f"Successfully verified {member.mention}.")
    else:
        await inter.response.send_message('User is already verified!')
    
@bot.slash_command(name="purge", description="Bulk deletion of messages.", enabled=True)
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def purge(inter: disnake.ApplicationCommandInteraction, amount: int):
    """
    Bulk deletion of messages.
    
    Parameters
    ----------
    amount: Number of messages to purge.
    """
    await inter.channel.purge(limit=amount, bulk=True)
    await inter.response.send_message(f"Successfully purged `{amount}` messages.", ephemeral=True)

@bot.slash_command(name="delete-remove", description="Removes hard delete from a user.",enabled=True)
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
async def deleteremove(inter: disnake.CommandInteraction, user: disnake.User):
    """
    Removes hard delete from a user.

    Parameters
    ----------
    user: The user on whom hard delete was applied earlier.
    """
    deletion_list.remove(user.id)
    await inter.response.send_message(f'Removed hard delete from {user}')

@bot.slash_command(name="google", description="Provides a google redirect button for the provided query.")
async def google(inter: disnake.CommandInteraction, *, query: str):
    """
    Parameters
    ----------
    
    query: The query to search
    """
    button = disnake.ui.Button
    view = disnake.ui.View()
    query = quote_plus(query)
    url = f"https://www.google.com/search?q={query}"
    view.add_item(button(label="Click here", url=url))
    await inter.response.send_message(f"Google Result for: `{query}`", view=view)

@bot.slash_command(name= "reboot", description="Restarts the bot, can only be used by the bot owner")
@commands.is_owner()
async def reboot(inter: disnake.CommandInteraction):
    await inter.response.send_message("**Rebooting** <a:malloading:922167995961335808>")
    os.system("clear")
    os.execv(sys.executable, ['python'] + sys.argv)
#-----------------------------------------------------------------------------------------------------

#APPLICATION COMMANDS

@bot.user_command(name="Avatar")
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
    embed = disnake.Embed(description=f"[Jump to message ►]({msg_link})\n {message.content}",color=inter.author.color, timestamp=message.created_at)
    embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
    await inter.send(embed=embed)

@bot.message_command(name="Reverse")
async def reverse(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
    await inter.response.send_message(message.content[::-1])
#-----------------------------------------------------------------------------------------------------

#EVENTS
@bot.listen()
async def on_message(msg):
    if msg.author.id in deletion_list:
        await msg.delete()

bot.messages = 0
@bot.listen()
async def on_message(message):
    bot.messages += 1
    if bot.messages == 50:
        ronit = bot.get_emoji(958468656034099312)
        await message.add_reaction(ronit)
        bot.messages = 0

@bot.listen()
async def on_message(message):
    if message.channel.id == 852926176514670632:
        if "https://" in message.content:
                await message.add_reaction('🔼')
                await message.add_reaction('🔽')

@bot.listen()
async def on_message(message):
    if message.attachments and message.channel.id==852926176514670632:
        await message.add_reaction('🔼')
        await message.add_reaction('🔽')

@bot.listen()
async def on_member_remove(member):
    bye = self.bot.get_channel(908296565255442462)
    await bye.send(f'''**{member}** `({member.id})` has left the server 💔
Sorry to see you go 😔
We hope you had a good time here ❤
_ _''')

@bot.listen()
async def on_member_join(member):
    welcome = self.bot.get_channel(908296505876688958)
    verify = self.bot.get_channel(900106358823739442)
    await member.send(f"""👋 {member.mention}, welcome to **{member.guild.name}**!

📝 Please verify yourself in <#900106358823739442> to gain access to rest of the server. 

🚀 **After verification, here's how to get started:**
<#809297410979397663> - Read the rules
<#850694848323256360> - Grab some roles
<#853143136620904518> - Start chatting and have fun

✨ Hope you have a good time in the server! 
_ _""")
    await verify.send(f"""👋 Hey {member.mention}, welcome to **{member.guild.name}**!

📝 Verify yourself here

📸 Send a picture of yours and gain access to rest of the server
_ _""")
    await welcome.send(f"""👋 {member.mention}, welcome to **{member.guild.name}**!

🚀 **Here's how to get started:**
<#809297410979397663> - Read the rules
<#850694848323256360> - Grab some roles
<#853143136620904518> - Start chatting and have fun

✨ Hope you have a good time here! 
_ _""")

@bot.listen('on_command_error')
async def error_handler(inter, error):
    raise error

@bot.listen()
async def on_command_error(inter: disnake.CommandInteraction, error: commands.CommandError):
    if isinstance(error, commands.CommandNotFound):
            return
    elif isinstance(error, commands.MissingPermissions):
        message = "<:notstonks:876167180666949692> You do not have permission to use this command!"
    elif isinstance(error, commands.MissingRole):
        message = "<:notstonks:876167180666949692> You do not have permission to use this command!"
    elif isinstance(error, commands.BadArgument):
        message = f"A bad argument was passed, please check the help descriptions properly or ask <2787149777103486986> for help."
    elif isinstance(error, commands.DisabledCommand):
        message = "❎ This command is disabled!"
    elif isinstance(error, commands.UserInputError):
        message = f"There's an issue in your input dear, please check the help descriptions properly or ask <2787149777103486986> for help."
    elif isinstance(error, commands.CommandOnCooldown):
        message = "**This command is on cooldown!**, try again in {:.2f}s".format(error.retry_after)
    elif isinstance(error, commands.NotOwner):
        message = "❎ **Only bot owner can use this command!**"
    
    await inter.response.send_message(message)
    
@bot.event
async def on_ready():
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.streaming, name="Board Exams", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
    print('Bot is ready')
#-----------------------------------------------------------------------------------------------------

bot.run(os.getenv("TOKEN"))
