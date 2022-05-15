from asyncio import events
from cgitb import text
from email.mime import application
from unicodedata import name
import disnake
from disnake.ext import commands
from disnake import AllowedMentions, member, channel
from psutil import users
import random
import json

class Apps(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.user_command(name="Avatar")
    async def avatar(inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        emb = disnake.Embed(title=f"{user}'s avatar", color=inter.author.color)
        emb.set_image(url=user.display_avatar.url)
        await inter.response.send_message(embed=emb)
    
    @commands.user_command(name="Info")
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

    @commands.message_command()
    async def Quote(inter, message: disnake.Message):
        msg_link = f'https://discord.com/channels/{inter.guild.id}/{inter.channel.id}/{message.id}'
        embed = disnake.Embed(description=f"[Jump to message ►]({msg_link})\n {message.content}",color=inter.author.color, timestamp=message.created_at)
        embed.set_author(name=message.author, icon_url=message.author.display_avatar.url)
        await inter.send(embed=embed)

    @commands.message_command(name="Reverse")
    async def reverse(inter: disnake.ApplicationCommandInteraction, message: disnake.Message):
        await inter.response.send_message(message.content[::-1])

def setup(bot):
    bot.add_cog(Apps(bot))