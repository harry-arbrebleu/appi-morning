import os
from collections import defaultdict
import discord
import gspread
import requests
import json
from oauth2client.service_account import ServiceAccountCredentials
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

# bot の準備
AuthB = "Bot " + TOKEN
headers = {"Authorization": AuthB}
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
bot = MyBot(command_prefix = '！', description = 'discord bot', intents = discord.Intents.all())
bot.remove_command("help")
buttons = ButtonsClient(bot)

# const類
blg = {"矢上": 1, "日吉": 2, "out": 0}
status = dict()
# 入退館の度にファイルを管理する．データは[日時, 種別, 累積和]
msg = input()
path_bs = "./" + msg.author
path = path_bs + ".csv"
if msg == "！登録":
    os.mkdir(path_bs)
    f = open(path, mode = 'w')
    f.close()
if msg[1:] in blg and msg[1:] != "！退館":
    status[msg.author] = blg[msg[1:]]
    with open(path, 'a', newline = "") as f:
        writer = csv.writer(f)
        now_tm = datetime.now().strftime('%H:%M:%S.%f')
        data = np.loadtxt(path, dtype = "str", delimiter = ",")
        data = data.T
        acm = data[2][-1]
        writer.writerow([now_tm, blg[msg[1:]], acm])
if msg == "！退館":
    status[msg.author] = 0
    with open(path, 'a', newline = "") as f:
        writer = csv.writer(f)
        now_tm = datetime.now().strftime('%H:%M:%S.%f')
        data = np.loadtxt(path, dtype = "str", delimiter = ",")
        data = data.T
        lst = data[0][-1]
        acm = data[2][-1]
        acm += datetime.now().strftime('%H:%M:%S.%f') - pd.to_datetime(lst)
        writer.writerow([now_tm, 0, acm])
