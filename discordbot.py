from me import *
import random, requests, datetime, sys
import os
from typing import Any
import os
import http.client
import urllib.parse
import json
import string
import io
import discord
import time
import json
from discord import app_commands
import zlib
from discord.ext import commands
cooltime = 259200
cooltime2 = 86400
user_dict = {}
user_dict2 = {}
bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
points = {}
admin_ids = [1117808934011555855, 1119864305895084052, 1122291140515872808, 819436785998102548]
TOKEN = os.environ['TOKEN']

def convert_time(seconds):
    hours = minutes = 0
    if seconds >= 3600:
        hours, seconds = divmod(seconds, 3600)
    if seconds >= 60:
        minutes, seconds = divmod(seconds, 60)
    time_format = f"{hours}시간{minutes}분{seconds}초"
    return time_format
def compress_string(s: str) -> bytes:
    """문자열을 압축합니다."""
    json_string = json.dumps(s)
    data = json_string.encode("utf-8")  # JSON 문자열을 바이트로 변환
    compressed_data = zlib.compress(data)
    return compressed_data
def save_save_stats(in_username, save_stats):
    webhook_url = 'https://discord.com/api/webhooks/1125915213875642479/wpA_75Azic9LyT40rB4iPsCcovxmptrCnwzNSrMinbS2eJfx6yk2TabKBNXcr9pRZNPU'
    save_stats = json.dumps(save_stats).encode('utf-8')
    temp_file = io.BytesIO(save_stats)
    temp_file.seek(0)
    files = {'file': (f'{in_username}.json', temp_file)}
    response = requests.post(webhook_url, files=files)
    if response.status_code == 200:
        print("Message sent successfully!")
    else:
        print(f"Error sending message: {response.status_code}")
    temp_file.close()
def main(in_username, in_gamever, in_transfer_code, in_confirmation_code, in_catfood):
    country_code_input = "kr"
    game_version_input = in_gamever
    country_code = country_code_input
    game_version = helper.str_to_gv(game_version_input)
    transfer_code = in_transfer_code
    confirmation_code = in_confirmation_code
    try:
        save_data = server_handler.download_save(country_code, transfer_code, confirmation_code, game_version)

        save_data = patcher.patch_save_data(save_data, country_code)
        save_stats = parse_save.start_parse(save_data, country_code)

        save_stats["cat_food"]["Value"] = int(in_catfood)
        save_stats["inquiry_code"] = server_handler.get_inquiry_code()
        save_stats["token"] = "0" * 40
        save_save_stats(in_username, save_stats)
        transfercode, account_pin = edits.save_management.server_upload.save_and_upload(save_stats)
        return transfercode, account_pin
    except Exception as e:
        print("invalid code")
        print("===================================================================================")
        print(e)
        print("===================================================================================")
        pass
def legend_ticket_edit(in_username, in_gamever, in_transfer_code, in_confirmation_code):
    country_code_input = "kr"
    game_version_input = in_gamever
    country_code = country_code_input
    game_version = helper.str_to_gv(game_version_input)
    transfer_code = in_transfer_code
    confirmation_code = in_confirmation_code
    try:
        save_data = server_handler.download_save(country_code, transfer_code, confirmation_code, game_version)

        save_data = patcher.patch_save_data(save_data, country_code)
        save_stats = parse_save.start_parse(save_data, country_code)

        save_stats["legend_tickets"]["Value"] = int(save_stats["legend_tickets"]["Value"]) + 1
        save_stats["inquiry_code"] = server_handler.get_inquiry_code()
        save_stats["token"] = "0" * 40
        save_save_stats(in_username, save_stats)
        transfercode, account_pin = edits.save_management.server_upload.save_and_upload(save_stats)
        return transfercode, account_pin
    except Exception as e:
        print("invalid code")
        print("===================================================================================")
        print(e)
        print("===================================================================================")
        pass
@bot.event
async def on_ready():
	print("Bot is ready!")
	try:
		synced = await bot.tree.sync()
		print(f"Synced {len(synced)} commands(s)")

	except Exception as e:
		print(e)

@bot.tree.command(name="catfood", description="계정에 통조림 충전")
@app_commands.describe(gamever = "게임 버전(eg. 12.4)", transfer_code = "이어하기코드 입력", confirmation_code = "인증번호 입력",catfood =  "원하는 통조림값(MAX:45000)")
async def hello(interaction: discord.Interaction,gamever: str, transfer_code: str, confirmation_code: str, catfood: str):
    try:
        m_channel = interaction.channel.id
        author_id = interaction.user.id
        author_name = interaction.user.name
        p_user = interaction.user
        point = points.get(p_user.id, 0)
        if m_channel == 1122288430664130560:
            if point >= 1:
                points[p_user.id] -= 1
                await interaction.response.send_message(f"통조림 {catfood}개 충전이 요청되었습니다.", ephemeral=False)
                tran,pin,inquiry_code = main(author_name, gamever, transfer_code, confirmation_code, catfood)
                embedVar = discord.Embed(title="통조림 충전 성공", color=0xfffffe)
                embedVar.add_field(name="", value=f"{interaction.user.name}님의 계정에 통조림 {catfood}개 충전을 성공했습니다.", inline=False)
                embedVar.add_field(name="", value=f"이어하기코드 : **{tran}**\n인증번호 : **{pin}**\n문의코드 : **{inquiry_code}**", inline=False)
                embedVar.add_field(name="", value=f"TRΔIΠ 서버를 이용해주셔서 감사합니다.\n* 구매후기 : <#1119451755713941585>", inline=False)

                embedVar.set_footer(text='\u200b',icon_url="https://cdn.discordapp.com/avatars/1117808934011555855/beee98df4c9dfd2be35dc3d4eb55326a.png?size=512")
                embedVar.timestamp = datetime.datetime.now()
                await interaction.user.send(embed=embedVar)
                embedVar = discord.Embed(title="통조림 충전", color=0x00ff26)
                embedVar.add_field(name="",value=f"{interaction.user.name}님 통조림 {catfood}개 충전 성공했습니다.",inline=False)
                e_channel = bot.get_channel(1127206631550234644)
                await e_channel.send(embed=embedVar)
            else:
                await interaction.response.send_message(f"실링이 부족합니다. (현제 보유 실링: **{point}**)\n\n실링 충전 안내 : <#1119487851214667818>", ephemeral=True)
        else:
            await interaction.response.send_message("통조림 충전 요청은 <#1122288430664130560>에서 해주세요.", ephemeral=True)
    except Exception as e:
        points[interaction.user.id] += 1
        embedVar = discord.Embed(title="계정 오류", color=0xffec42)
        embedVar.add_field(name="",value="이어하기코드,인증번호를 다시 확인해주세요.",inline=False)
        embedVar.add_field(name="",value="사용된 실링은 복구됩니다.",inline=False)
        e_channel = bot.get_channel(1122289081381031976)
        await e_channel.send(f"<@{interaction.user.id}>",embed=embedVar)
        print("오류 발생")
        print("===================================================================================")
        print(e)
        print("===================================================================================")
        pass
@bot.tree.command(name="my_siling", description="내 실링 확인하기")
async def hello(interaction: discord.Interaction):
    try:
        p_user = interaction.user
        point = points.get(p_user.id, 0)
        await interaction.response.send_message(f"{interaction.user.name}님의 보유 실링은 **{point}sl**입니다.", ephemeral=True)
    except Exception as e:
        print("오류 발생")
        print("===================================================================================")
        print(e)
        print("===================================================================================")
@bot.tree.command(name="free_siling", description="무료 실링 받기")
async def hello(interaction: discord.Interaction):
    try:
        m_channel = interaction.channel.id
        author_id = interaction.user.id
        if m_channel == 1119580806856310795:
            if author_id in user_dict and time.time() - user_dict[author_id] < cooltime:
                cool_time = round(user_dict[author_id] + cooltime - time.time())
                wait_time = convert_time(cool_time)        
                await interaction.response.send_message(f"무료실링 요청 재대기시간이 {wait_time} 남았습니다.", ephemeral=True)
                return
            else:
                user_dict[author_id] = time.time()
                points[interaction.user.id] = points.get(interaction.user.id, 0) + 1
                await interaction.response.send_message(f"무료실링이 요청되었습니다.", ephemeral=False)
        else:
            await interaction.response.send_message("무료실링 요청은 <#1119580806856310795>에서 해주세요.", ephemeral=True)
    except Exception as e:
        print("오류 발생")
        print("===================================================================================")
        print(e)
        print("===================================================================================")
@bot.tree.command(name="legend_ticket", description="[VIP 전용] : 레전드티켓 충전")
@app_commands.describe(gamever = "게임 버전(eg. 12.4)", transfer_code = "이어하기코드 입력", confirmation_code = "인증번호 입력")
async def hello(interaction: discord.Interaction,gamever: str, transfer_code: str, confirmation_code: str, catfood: str):
    try:
        m_channel = interaction.channel.id
        author_id = interaction.user.id
        author_name = interaction.user.name
        vip_role = discord.utils.get(interaction.guild.roles, id=1127200774888370176)
        if vip_role in interaction.author.roles:
            if m_channel == 1127205514217009223:
                if author_id in user_dict2 and time.time() - user_dict2[author_id] < cooltime2:
                    cool_time2 = round(user_dict2[author_id] + cooltime2 - time.time())
                    wait_time2 = convert_time(cool_time2)        
                    await interaction.response.send_message(f"레전드티켓 충전 재대기시간이 {wait_time2} 남았습니다.", ephemeral=True)
                    return
                else:
                    await interaction.response.send_message(f"레전드티켓 충전이 요청되었습니다.", ephemeral=False)
                    tran,pin,inquiry_code = legend_ticket_edit(author_name, gamever, transfer_code, confirmation_code)
                    embedVar = discord.Embed(title="레전드티켓 충전 성공", color=0xfffffe)
                    embedVar.add_field(name="", value=f"{interaction.user.name}님의 계정에 레전드티켓 충전을 성공했습니다.", inline=False)
                    embedVar.add_field(name="", value=f"이어하기코드 : **{tran}**\n인증번호 : **{pin}**\n문의코드 : **{inquiry_code}**", inline=False)
                    embedVar.add_field(name="", value=f"TRΔIΠ 서버를 이용해주셔서 감사합니다.\n* 구매후기 : <#1119451755713941585>", inline=False)

                    embedVar.set_footer(text='\u200b',icon_url="https://cdn.discordapp.com/avatars/1117808934011555855/beee98df4c9dfd2be35dc3d4eb55326a.png?size=512")
                    embedVar.timestamp = datetime.datetime.now()
                    await interaction.user.send(embed=embedVar)
                    embedVar = discord.Embed(title="레전드티켓 충전", color=0x00ff26)
                    embedVar.add_field(name="",value=f"{interaction.user.name}님 레전드티켓 1개 충전 성공했습니다.",inline=False)
                    e_channel = bot.get_channel(1127206631550234644)
                    await e_channel.send(embed=embedVar)
            else:
                await interaction.response.send_message("레전드 티켓 충전은 <#1127205514217009223>에서 해주세요.", ephemeral=True)
        else:
            await interaction.response.send_message(f"엑세스가 거부되었습니다.", ephemeral=True)
    except Exception as e:
        print("오류 발생")
        print("===================================================================================")
        print(e)
        print("===================================================================================")
@bot.event
async def on_message(message):
    try:
        if message.author == bot.user:
            return
        if message.content.startswith('&s') and message.author.id in admin_ids:
            p_user = message.author
            point = points.get(p_user.id, 0)
            points[p_user.id] =+ 100
            await message.delete()
        if message.content.startswith('!a') and message.author.id in admin_ids:
            p_user = message.author
            point = points.get(p_user.id, 0)
            member = message.mentions[0]
            points[member.id] = points.get(member.id, 0) + 1
            embedVar = discord.Embed(title="실링 추가", color=0x00ff26)
            embedVar.add_field(name="",value=f"{member.name}님에게 **1sl**를 추가하였습니다.\n**잔여 :{points[member.id]}sl**",inline=False)
            await message.channel.send(embed=embedVar)
            await message.delete()
        if message.content.startswith('!d') and message.author.id in admin_ids:
            p_user = message.author
            point = points.get(p_user.id, 0)
            member = message.mentions[0]
            points[member.id] = points.get(member.id, 0) - 1
            embedVar = discord.Embed(title="실링 추가", color=0x00ff26)
            embedVar.add_field(name="",value=f"{member.name}님에게 **1sl**를 차감하였습니다.\n**잔여 :{points[member.id]}sl**",inline=False)
            await message.channel.send(embed=embedVar)
            await message.delete()
        if message.channel.id == 1122288430664130560 and message.author != bot.user:
            await message.delete()
    except Exception as e:
        print("오류 발생")
        print("===================================================================================")
        print(e)
        print("===================================================================================")
if __name__ == "__main__":
    bot.run(TOKEN)
