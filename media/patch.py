import os
from collections import defaultdict, deque
import discord
import gspread
import requests
import json
from datetime import datetime, timedelta
from discord_buttons_plugin import *
from discord.ext import commands
from pprint import pprint
import pandas as pd
import aiohttp
import numpy as np
import math
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib import cm
from scipy import optimize
from scipy.optimize import curve_fit
import csv
from matplotlib.dates import drange
from matplotlib.dates import DateFormatter
from matplotlib.dates import date2num
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import japanize_matplotlib
import sys
import shutil
import time

# TOKEN = os.getenv("DISCORD_TOKEN")
AuthB = "Bot " + TOKEN
headers = {"Authorization": AuthB}
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

bot = MyBot(command_prefix = '！', description = "discord bot", intents = discord.Intents.all())
bot.remove_command("help")

mb = set()
time_sum = dict()
id_out = 1157995194361323571
# id_hys = 1157994781859909685
# id_ygm = 1157995100664758312
chan_tst = 1157994782874939408
chan_tgt = 1158005327107739678
blg = {"矢上": 1, "日吉": 2, "out": 0}
rl = {"矢上": 1157995100664758312, "日吉": 1157994781859909685, "out": 1157995194361323571}
status = dict()

@bot.event
async def on_ready():
    if os.path.exists("./data"):
        shutil.rmtree("./data")
        os.mkdir("./data")
    print("Successfully logged in")
    await bot.change_presence(activity = discord.Game("Python"))
@bot.event
async def on_message(message):
    msg = str(message.content)
    atr = str(message.author)
    path_bs = "./data/" + atr
    path = path_bs + '/' + atr + ".csv"
    if message.content == "！助けて":
        embed = discord.Embed(
        title = "botの使い方を説明します！",
        color = 0x800080,
        )
        embed.add_field(name = "！登録", value = "さあはじめましょう！まずは「！登録」と入力して記録を始めましょう．", inline = False)
        embed.add_field(name = "！矢上", value = "矢上メディアに入館したら「！矢上」と入力してください．", inline = False)
        embed.add_field(name = "！日吉", value = "日吉メディアに入館したら「！日吉」と入力してください．", inline = False)
        embed.add_field(name = "！退館", value = "メディアから出たら「！退館」と入力してください．", inline = False)
        embed.add_field(name = "！グラフ", value = "自身の累積在館時間を見たいときは「！グラフ」と入力してください．", inline = False)
        embed.add_field(name = "！ランキング", value = "「！ランキング」と入力することで，累積在館時間のランキングが5位まで出力されます．", inline = False)
        embed.add_field(name = "！助けて", value = "「！助けて」と打つとコマンドが表示されます", inline = False)
        if message.author.guild_permissions.administrator:
            embed.add_field(name = "sudo end task", value = "terminate task", inline = False)
        embed.add_field(name = "注意", value = "コマンドは「bot-command」チャンネルで使ってくださいね！", inline = False)
        await message.channel.send(embed = embed)
    elif msg == "！登録":
        if os.path.exists(path_bs):
            reply = "あなたは登録済みです．早くメディアに入館しましょう！"
            await message.channel.send(reply)
        else:
            os.mkdir(path_bs)
            f = open(path, mode = 'w')
            role = message.author.guild.get_role(rl["out"])
            await message.author.add_roles(role)
            with open(path, 'a', newline = "", encoding = "cp932") as f:
                writer = csv.writer(f)
                now_tm = datetime.now().replace(microsecond = 0)
                writer.writerow([atr, "status", now_tm - now_tm])
                writer.writerow(["time", "status", now_tm - now_tm])
            f.close()
            reply = "登録が完了しました．メディアに行きましょう！"
            await message.channel.send(reply)
    elif msg[1:] in blg and msg[1:] != "！退館":
        if not os.path.exists(path_bs):
            reply = "あなたは登録されていません．「！登録」コマンドから，先に登録を済ませてください．"
            await message.channel.send(reply)
        else:
            status[atr] = blg[msg[1:]]
            with open(path, 'a', newline = "", encoding = "cp932") as f:
                writer = csv.writer(f)
                now_tm = datetime.now().replace(microsecond = 0)
                data = np.loadtxt(path, dtype = "str", delimiter = ",", encoding = "cp932")
                data = data.T
                if data[1][-1] != "0" and data[1][-1] != status:
                    reply = "あなたは他のメディア入館済みです．先に「！退館」コマンドを実行してください"
                    await message.channel.send(reply)
                else:
                    writer.writerow([now_tm, blg[msg[1:]], data[2][-1]])
                    reply = f"{message.author.mention} が{str(time.strftime('%Y/%m/%d %H:%M:%S'))}に{msg[1:]}キャンパスに入館しました．"
                    await message.channel.send(reply)
                    await message.author.edit(roles=[])
                    role_ad = message.author.guild.get_role(rl[msg[1:]])
                    await message.author.add_roles(role_ad)
    elif msg == "！退館":
        if not os.path.exists(path_bs):
            reply = "あなたは登録されていません．「！登録」コマンドから，先に登録を済ませてください．"
            await message.channel.send(reply)
        else:
            status[atr] = 0
            with open(path, 'a', newline = "", encoding = "cp932") as f:
                data = np.loadtxt(path, dtype = "str", delimiter = ",", encoding = "cp932")
                data = data.T
                if data[1][-1] == "0":
                    reply = "あなたはメディアに入館していません．「！(キャンパス名)」コマンドで入館してください，"
                    await message.channel.send(reply)
                else:
                    writer = csv.writer(f)
                    now_tm = datetime.now().replace(microsecond = 0)
                    if data[1][-1] == "status":
                        reply = "あなたはメディアに入館していません．「！(キャンパス名)」コマンドで入館してください，"
                        await message.channel.send(reply)
                        return
                    await message.author.edit(roles = [])
                    role_ad = message.author.guild.get_role(rl["out"])
                    await message.author.add_roles(role_ad)
                    acm = pd.to_datetime(data[2][-1])
                    pls = now_tm - pd.to_datetime(data[0][-1])
                    acm += pls
                    writer.writerow([now_tm, 0, str(acm)[11:]])
                    embed = discord.Embed(
                        title = f"{atr}さんの統計",
                        color = 0x00ff00, # フレーム色指定(今回は緑)
                    )
                    cps = ""
                    for k in blg:
                        if data[1][-1] == k:
                            cps = blg[k]
                            break
                    embed.add_field(name = "今回訪れたキャンパス", value = cps)
                    embed.add_field(name = "今回の在館時間", value = pls)
                    embed.add_field(name = "累計在館時間",value = acm)
                    await message.channel.send(embed = embed)
    elif msg == "！ランキング":
        if not os.path.exists(path_bs):
            reply = "あなたは登録されていません．「！登録」コマンドから，先に登録を済ませてください．"
            await message.channel.send(reply)
        else:
            li = list()
            embed = discord.Embed(
                title = f"{datetime.now().replace(microsecond = 0)}時点でのランキング",
                color = 0x001100,
            )
            for dirpath, _, files in os.walk("./data"):
                for f in files:
                    fl = os.path.join(dirpath, f)
                    data = np.loadtxt(fl, dtype = "str", delimiter = ",", encoding = "cp932")
                    data = list(data.T)
                    tmp = pd.to_timedelta(data[2][-1][-8:])
                    li.append([tmp, data[0][0]])
            if len(li) == 0:
                await message.channel.send("ランキングが無効です．")
                return
            if len(li) == 1:
                embed.add_field(name = f"{1} 位", value = f"{li[0][1]}さん({li[0][0]})", inline = False)
                await message.channel.send(embed = embed)
                return
            li.sort(reverse = True)
            for i in range(min(5, len(li))):
                embed.add_field(name = f"{i + 1} 位", value = f"{li[i][1]}さん({li[i][0]})", inline = False)
            await message.channel.send(embed = embed)
    elif msg == "！グラフ":
        if not os.path.exists(path_bs):
            reply = "あなたは登録されていません．「！登録」コマンドから，先に登録を済ませてください．"
            await message.channel.send(reply)
            return
        path_to = path_bs + '/' + atr + ".png"
        data = np.loadtxt(path, dtype = "str", delimiter = ",", encoding = "cp932")
        data = data[2:].T
        tx = pd.to_datetime(data[0])
        r = [data[1][i] for i in range(len(data[1]))]
        k = pd.to_timedelta(data[2])
        ty = [int(k[i].seconds) / 60  for i in range(len(k))]
        x = list()
        y = list()
        for i in range(0, len(tx), 2):
            x.append(tx[i])
            y.append(ty[i])
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        plt.rcParams["font.size"] = 14
        plt.rcParams["xtick.direction"] = "in"
        plt.rcParams["ytick.direction"] = "in"
        li = []
        tmp = x[0]
        while True:
            li.append(tmp)
            tmp += timedelta(days = 31)
            if tmp > x[-1]:
                li.append(x[-1])
                break
        new_xticks = date2num(li)
        ax1.xaxis.set_major_locator(ticker.FixedLocator(new_xticks))
        ax1.xaxis.set_major_formatter(DateFormatter("%m-%d"))
        ax1.plot(x, y, color = 'b')
        ax1.fill_between(x, y, color = "lightblue", alpha = 0.5)
        ax1.set_xlabel("日付")
        ax1.set_ylabel(r"累積滞在時間$/\ \rm{min}$")
        ax1.yaxis.set_ticks_position("left")
        ax1.xaxis.set_ticks_position("bottom")
        ax1.scatter(x, y, lw = 1, marker = 'o', color = 'k')
        fig.savefig(path_to)
        await message.channel.send(file = discord.File(path_to))
bot.run(TOKEN)
