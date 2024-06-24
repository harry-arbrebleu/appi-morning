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

li = list()
embed = discord.Embed(
    title = f"{datetime.now().replace(microsecond = 0)}時点でのランキング",
    color = 0x001100,
)
for dirpath, _, files in os.walk("./data"):
    for f in files:
        fl = os.path.join(dirpath, f)
        data = np.loadtxt(fl, dtype = "str", delimiter = ",", encoding = "utf-8")
        data = list(data.T)
        tmp = pd.to_timedelta(data[2][-1][-8:])
        li.append([tmp, data[0][0]])
print(li)
# if len(li) == 0:
#     # await message.channel.send("ランキングが無効です．")
# #     # return
# if len(li) == 1:
#     embed.add_field(name = f"{1} 位", value = f"{li[0][1]}さん({li[0][0]})", inline = False)
#     # await message.channel.send(embed = embed)
#     # return
# li.sort(reverse = True)
# for i in range(min(5, len(li))):
#     embed.add_field(name = f"{i + 1} 位", value = f"{li[i][1]}さん({li[i][0]})", inline = False)
# await message.channel.send(embed = embed)