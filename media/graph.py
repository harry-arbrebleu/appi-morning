import os
from collections import defaultdict
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

# TOKEN = os.getenv("DISCORD_TOKEN")
TOKEN = ""
AuthB = "Bot " + TOKEN
headers = {"Authorization": AuthB}
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

bot = MyBot(command_prefix = '！', description = 'discord bot', intents = discord.Intents.all())
bot.remove_command("help")

member = dict()
status = dict()
time_in = dict()
time_sum = dict()
id_out = 1157995194361323571
id_hys = 1157994781859909685
id_ygm = 1157995100664758312
chan_tst = 1157994782874939408
chan_tgt = 1158005327107739678
blg = {"矢上": 1, "日吉": 2, "out": 0}
status = dict()

@bot.event
async def on_ready():
    print("Successfully logged in")
    await bot.change_presence(activity = discord.Game("Python"))
@bot.event
async def on_message(message):
    msg = str(message.content)
    # msg = input()
    atr = str(message.author)
    path_bs = "./data/" + atr
    path = path_bs + '/' + atr + ".csv"
    if msg == "！グラフ":
        path_to = path_bs + '/' + atr + ".png"
        data = np.loadtxt(path, dtype = "str", delimiter = ",", encoding = "utf-8")
        data = data[2:].T
        x = pd.to_datetime(data[0])
        r = [data[1][i] for i in range(len(data[1]))]
        k = pd.to_timedelta(data[2])
        y = [int(k[i].seconds) / 60  for i in range(len(k))]
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