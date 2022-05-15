from asyncio import events
from cgitb import text
from unicodedata import name
import disnake
from disnake.ext import commands
from disnake import AllowedMentions, member, channel
from psutil import users
import random
import json

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listner()
    async def on_member_join(self, member):
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

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        bye = self.bot.get_channel(908296565255442462)
        await bye.send(f'''**{member}** `({member.id})` has left the server 💔
Sorry to see you go 😔
We hope you had a good time here ❤
_ _''')

    @commands.Cog.listener()
    async def on_message(message):
        if message.attachments and message.channel.id==852926176514670632:
            await message.add_reaction('🔼')
            await message.add_reaction('🔽')

    @commands.Cog.listener()
    async def on_message(message):
        if message.channel.id == 852926176514670632:
            if "https://" in message.content:
                if "https://tenor.com" in message.content:
                  return
                elif "https://giphy.com" in message.content:
                  return
                else:
                    await message.add_reaction('🔼')
                    await message.add_reaction('🔽')

def setup(bot):
    bot.add_cog(Events(bot))