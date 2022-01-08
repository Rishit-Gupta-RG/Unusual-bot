import disnake
from disnake.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix=">")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.event
async def on_ready():
    print('I\'m on')

bot.run(os.getenv("TOKEN"))