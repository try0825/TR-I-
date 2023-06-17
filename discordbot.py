from cmath import log
from distutils.sysconfig import PREFIX
import discord
from discord.ext import commands
from discord_slash import SlashCommand

from dotenv import load_dotenv
import os
load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

TOKEN = os.environ['TOKEN']

@bot.event
async def on_ready():
    print("Bot is ready!")
    print(f"Synced {len(bot.slash.commands)} command(s)")

@slash.slash(name="hello", description="Say hello")
async def hello(ctx):
    await ctx.send(f"Hey {ctx.author.mention}! This is a slash command!")

@slash.slash(name="say", description="Echo a message")
async def say(ctx, thing_to_say: str):
    await ctx.send(f"{ctx.author.name} said: `{thing_to_say}`")

bot.run(TOKEN)
