import os
from collections import defaultdict
import discord
import gspread
import requests
import json
from oauth2client.service_account import ServiceAccountCredentials
import datetime, time
from datetime import timedelta
from discord_buttons_plugin import *
from discord.ext import commands
from pprint import pprint
import aiohttp
import numpy as np
import math
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib import cm
from scipy import optimize
from scipy.optimize import curve_fit

# TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN = ""# 読み込む処理を書く
AuthB = "Bot " + TOKEN
headers = {"Authorization": AuthB}
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

bot = MyBot(command_prefix = '！', description = 'discord bot', intents = discord.Intents.all())
bot.remove_command("help")
buttons = ButtonsClient(bot)
# def connect_gspread(jsonf, key):
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     credentials = ServiceAccountCredentials.from_json_keyfile_name(jsonf, scope)
#     gc = gspread.authorize(credentials)
#     SPREADSHEET_KEY = key
#     worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
#     print("connected")
#     return worksheet
jsonf = "keys.json"
spread_sheet_key = "116EfxTsPPDKMueEZofW1mcHMMLIaqlvFp0d783FVCDc"
# ws = connect_gspread(jsonf, spread_sheet_key)


member = dict()
status = dict()
time_in = dict()
time_sum = dict()
id_out = 1254321306133073931
id_hys = 1254321124381298719
id_ygm = 1254321044143996978
# chan_tst = 1157994782874939408
# chan_tgt = 1158005327107739678
cnt = 1
@bot.event
async def on_ready():
    print("Successfully logged in")
    await bot.change_presence(activity = discord.Game("Python"))
@bot.event
async def on_message(message):
    # if message.channel.id != chan_tst and message.channel.id != chan_tgt:
        # return
    global cnt
    if message.content == "！助けて":
        embed = discord.Embed(
        title = "botの使い方を説明します！",
        color = 0x800080,
        )
        embed.add_field(name = "！登録", value = "さあはじめましょう！まずは「！登録」と入力して記録を始めましょう．", inline = False)
        embed.add_field(name = "！矢上", value = "矢上メディアに入館したら「！矢上」と入力してください．", inline = False)
        embed.add_field(name = "！日吉", value = "日吉メディアに入館したら「！日吉」と入力してください．", inline = False)
        embed.add_field(name = "！退館", value = "メディアから出たら「！退館」と入力してください．", inline = False)
        embed.add_field(name = "！ランキング", value = "「！ランキング」と入力することで，累積在館時間のランキングが5位まで出力されます．", inline = False)
        embed.add_field(name = "！助けて", value = "「！助けて」と打つとコマンドが表示されます", inline = False)
        if message.author.guild_permissions.administrator:
            embed.add_field(name = "sudo end task", value = "terminate task", inline = False)
        embed.add_field(name = "注意", value = "コマンドは「bot-command」チャンネルで使ってくださいね！", inline = False)
        await message.channel.send(embed = embed)
    if message.content == "！登録":
        if message.author not in member:
            member[message.author] = cnt
            status[message.author] = "out"
            time_sum[message.author] = timedelta(0)
            # ws.update_cell(1, cnt * 3 - 1, str(message.author) + "の入館時刻")
            # ws.update_cell(1, cnt * 3, str(message.author) + "の退館時刻")
            # ws.update_cell(1, cnt * 3 + 1, str(message.author) + "の滞在時間")
            role = message.author.guild.get_role(id_out)
            await message.author.add_roles(role)
            reply = f"{message.author.mention} を登録しました．{cnt}人目の登録者です．"
            cnt += 1
            await message.channel.send(reply)
        else:
            reply = f"{message.author.mention} は既に登録されています．"
            await message.channel.send(reply)
    elif message.content == "！日吉" or message.content == "！矢上":
        reply = ""
        if status[message.author] == "ygm" or status[message.author] == "hys":
            reply = "あなたは入館済みです．再度入館するときは「！退館」を先に実行してください．"
        else:
            # ws.update_cell(status[message.author] // 2, member[message.author] * 3 - 1, str(datetime.datetime.now().time()))
            time_in[message.author] = datetime.datetime.now().replace(microsecond = 0)
            reply = f"{message.author.mention} が{str(time.strftime('%Y/%m/%d %H:%M:%S'))}に入館しました．"
            if message.content == "！日吉":
                await message.author.edit(roles=[])
                role_ad = message.author.guild.get_role(id_hys)
                status[message.author] = "hys"
                await message.author.add_roles(role_ad)
            if message.content == "！矢上":
                await message.author.edit(roles=[])
                role_ad = message.author.guild.get_role(id_ygm)
                status[message.author] = "ygm"
                await message.author.add_roles(role_ad)
        await message.channel.send(reply)
    elif message.content == "！退館":
        if status[message.author] == "out":
            reply = "あなたは退館済です．再度入館するときは「！矢上」か「！日吉」を実行してください．"
            await message.channel.send(reply)
        else:
            await message.author.edit(roles = [])
            role_ad = message.author.guild.get_role(id_out)
            await message.author.add_roles(role_ad)
            # ws.update_cell(status[message.author] // 2, member[message.author] * 3, str(datetime.datetime.now().time()))
            td = datetime.datetime.now().replace(microsecond = 0) - time_in[message.author]
            # ws.update_cell(status[message.author] // 2, member[message.author] * 3 + 1, td)
            time_sum[message.author] += td
            embed = discord.Embed(
                title = f"{message.author}さんの統計",# タイトル
                color = 0x00ff00, # フレーム色指定(今回は緑)
            )
            embed.add_field(name = "今回の在館時間", value = td)
            embed.add_field(name = "累計在館時間",value = time_sum[message.author])
            reply = f"{message.author.mention} が{str(time.strftime('%Y/%m/%d %H:%M:%S'))}に退館しました．在館時間は{td}です．今シーズンは累計{time_sum[message.author]}在館しています．"
            status[message.author] = "out"
            await message.channel.send(embed = embed)
    elif message.content == "！ランキング":
        li = list()
        embed = discord.Embed(
            title = f"{datetime.datetime.now().replace(microsecond = 0)}時点でのランキング",
            color = 0x001100,
        )
        for k in time_sum.keys():
            li.append([time_sum[k], k])
        if len(li) == 0:
            await message.channel.send("ランキングが無効です．")
        li.sort(reverse = True)
        for i in range(5):
            try:
                embed.add_field(name = f"{i + 1} 位", value = f"{li[i][1]}さん({li[i][0]})", inline = False)
            except IndexError:
                break
        await message.channel.send(embed = embed)
    elif message.content == "sudo end task":
        if message.author.guild_permissions.administrator:
            for k in time_sum.keys():
                await k.edit(roles = [])
            exit()
        else:
            await message.channel.send("You are not super user.")
    # elif message.content == "！グラフ":
    #     atr = message.author
    #     data = np.loadtxt("present.txt", dtype = "float", delimiter = ",")
    #     data = data.T
        
bot.run(TOKEN)
