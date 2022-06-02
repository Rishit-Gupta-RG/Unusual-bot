from cgitb import text
from pydoc import describe
from unicodedata import name
import disnake
from disnake.ext import commands
from disnake import AllowedMentions, member, channel
from psutil import users
import random
import json
import datetime

mrole = 882516473304719430
hard = []
gg_gif = "https://images-ext-1.discordapp.net/external/nraLnI6Enk7ae63ADgjKkUtuKAnmo2BZETw15mfZ0bg/%3Fsize%3D4096/https/cdn.discordapp.com/icons/764549036090720267/9b954c862e9b092399dae9feee763d37.png?width=428&height=428"

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.slash_command(name="kick")
    @commands.check_any(commands.has_role(mrole), commands.is_owner(), commands.has_permissions(kick_members=True), commands.has_permissions(administrator=True))
    async def my_kick_command(self, ctx, member: disnake.Member, *,reason: str=None) -> None:
        """
        Kicks a member.
        
        Parameters
        ----------
        member: The member to kick.
        reason: Reason for kick.
        """
        embed = disnake.Embed(description=f"**❯ Type**: Kick\n**❯ Reason**: {reason}", timestamp=datetime.utcnow())
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(icon_url=gg_gif, text=ctx.guild.name)
        await member.send(embed=embed)
        await member.kick(reason=reason)
        await ctx.send(f"👌 Successfully {ctx.command}ed {ctx.member.mention} | `{ctx.member}`.\nWith the reason of: {reason}")

    @commands.slash_command(name="warn")
    @commands.check_any(commands.has_role(mrole), commands.is_owner(), commands.has_permissions(kick_members=True), commands.has_permissions(administrator=True))
    async def my_warn_command(self, ctx, member: disnake.Member, reason: str):
        """
        Warns a member.
        
        Parameters
        ----------
        member: Member to warn
        reason: Reason for warn
        """
        embed = disnake.Embed(description=f"**❯ Type**: Warning\n**❯ Reason**: {reason}", timestamp=datetime.utcnow())
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(icon_url=gg_gif, text=ctx.guild.name)
        await member.send(embed=embed)
        await ctx.send(f"👌 Successfully {ctx.command}ed {ctx.member.mention} | `{ctx.member}`.\nWith the reason of: {reason}")

    @commands.slash_command(name="timeout")
    @commands.check_any(commands.has_role(mrole), commands.is_owner(), commands.has_permissions(manage_nicknames=True), commands.has_permissions(administrator=True))
    async def my_timeout_command(self, ctx, member: disnake.Member, duration=None, reason: str=None) -> None:
        if duration == None:
            embed = disnake.Embed(description=f"**❯ Type**: Reverted Timeout\n**❯ Reason**: {reason}", timestamp=datetime.utcnow())
            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
            embed.set_footer(icon_url=gg_gif, text=ctx.guild.name)
            await member.send(embed=embed)
            await member.timeout(reason=reason, duration=None)
            await ctx.send(f"👌 Removed timeout from {ctx.member.mention}\nWith the reason of: {reason}")
        else:
            time_convert = {'s': 1 , 'm' : 60 , 'h' : 3600 , 'd' : 86400, 'S' : 1, 'M' : 60, 'H' : 3600, "D" : 86400}
            timeout_time = float(duration[0:len(duration)-1]) * time_convert[duration[-1]]
            embed = disnake.Embed(description=f"**❯ Type**:Timeout\n**❯ Duration**: {duration}\n**❯ Reason**: {reason}", timestamp=datetime.utcnow())
            embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
            embed.set_footer(icon_url=gg_gif, text=ctx.guild.name)
            await member.send(embed=embed)
            await member.timeout(reason=reason, duration=timeout_time)
            await ctx.send(f"👌 Successfully Timed out {ctx.member.mention} for {duration}\nWith the reason of: {reason}")

    @commands.slash_command(name="ban")
    @commands.check_any(commands.has_role(mrole), commands.is_owner(), commands.has_permissions(ban_members=True), commands.has_permissions(administrator=True))
    async def my_ban_command(self, ctx, member: disnake.Member,*, reason: str=None) -> None:
        """
        Bans a member.
        
        Parameters
        ----------
        member: The member to ban.
        reason: Reason for ban.
        """
        embed = disnake.Embed(description=f"**❯ Type**: Ban\n**❯ Reason**: {reason}", timestamp=datetime.utcnow())
        embed.set_author(name=ctx.author, icon_url=ctx.author.display_avatar.url)
        embed.set_footer(icon_url=gg_gif, text=ctx.guild.name)
        await member.send(embed=embed)
        await member.ban(reason=reason)
        await ctx.send(f"👌 Successfully banned {ctx.member.mention} | `{ctx.member}`\nWith the reason of: {reason}")
    
    @commands.slash_command(name="nick")
    @commands.check_any(commands.has_role(mrole), commands.is_owner(), commands.has_permissions(manage_nicknames=True), commands.has_permissions(administrator=True))
    async def my_nick_cmd(self, ctx, member: disnake.Member,*, nickname: str):
        """
        Changes nickname of a member.
        
        Parameters
        ----------
        member: The member whose nickname is to be changed.
        nickname: New nickname
        """
        await member.edit(nick=nickname)
        await ctx.send(f"👌 Changed nickname for {ctx.member.mention}.")

    @commands.slash_command(name="deletion")
    @commands.has_permissions(administrator=True)
    async def my_hard_delete_command(self, ctx, member: disnake.Member):
        """
        Toggles hard-deletion.
        
        Parameters
        ----------
        member: The member on whom hard delete is to be applied/removed.
        """
        if member.id in hard:
            hard.remove(member.id)
            await ctx.send("<:society:932186685926694914>")
        else:
            await ctx.send(f"👌 Removed hard delete from {member.mention}.")

    @commands.Cog.listener()
    async def on_message(msg):
        if msg.author.id in hard:
            await msg.delete()

def setup(bot):
    bot.add_cog(Moderation(bot))