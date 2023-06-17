from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os

from discord import app_commands
from discord.ext import commands
load_dotenv()
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
TOKEN = os.environ['TOKEN']
@bot.event
async def on_ready():
	print("Bot is ready!")
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} commands(s)")

	except Exception as e:
		print(e)

@bot.tree.command(name="hello")
async def hello(interaction: discord.Interaction):
	await interaction.response.send_message(f"Hey {interaction.user.mention}! This is a slash command!", ephemeral=True)

@bot.tree.command(name="say")
@app_commands.describe(thing_to_say = "what should I say?")
async def say(interaction: discord.Interaction, thing_to_say: str):
	await interaction.response.send_message(f"{interaction.user.name} said: `{thing_to_say}`")

bot.run(TOKEN)
