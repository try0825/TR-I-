from cmath import log
from distutils.sysconfig import PREFIX
import discord
from dotenv import load_dotenv
import os
from pydoc import describe
import discord
import time
from discord import app_commands
from discord.ext import commands
load_dotenv()
TOKEN = os.environ['TOKEN']


bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

cooltime = 259200 # 30초 동안 대기할 수 있도록 설정합니다.
user_dict = {}


def convert_time(seconds):
    days = hours = minutes = 0
    if seconds >= 86400:
        days, seconds = divmod(seconds, 86400)
    if seconds >= 3600:
        hours, seconds = divmod(seconds, 3600)
    if seconds >= 60:
        minutes, seconds = divmod(seconds, 60)
    time_format = f"{days}일{hours}시간{minutes}분{seconds}초"
    return time_format

@bot.event
async def on_ready():
	print("Bot is ready!")
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} commands(s)")

	except Exception as e:
		print(e)

@bot.tree.command(name="free_catfood", description="무료 통조림 충전 서비스")
@app_commands.describe(transfer_code = "이어하기코드 입력", confirmation_code = "인증번호 입력",catfood =  "원하는 통조림값(MAX:45000)")
async def hello(interaction: discord.Interaction,transfer_code: str, confirmation_code: str, catfood: str):
    m_channel = interaction.channel.id
    author_id = interaction.user.id
    if m_channel == 1119580806856310795:
        if author_id in user_dict and time.time() - user_dict[author_id] < cooltime:
            cool_time = round(user_dict[author_id] + cooltime - time.time())
            wait_time = convert_time(cool_time)        
            await interaction.response.send_message(f"무료충전 요청 재대기시간이 {wait_time} 남았습니다.", ephemeral=True)
            return
        else:
            user_dict[author_id] = time.time()
            channel = await bot.fetch_channel(1119942819604349028)
            await interaction.response.send_message(f"통조림 {catfood}개 충전이 요청되었습니다.", ephemeral=False)
            await channel.send(f"이어하기코드: `{transfer_code}`\n인증번호: `{confirmation_code}`\n통조림 갯수: `{catfood}`\nuser: {interaction.user.mention}")
    else:
        await interaction.response.send_message("통조림 충전 요청은 <#1119580806856310795>에서 해주세요.", ephemeral=True)

bot.run(TOKEN)
