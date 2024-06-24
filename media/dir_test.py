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
li = list()
for dirpath, _, files in os.walk("./data"):
    for f in files:
        fl = os.path.join(dirpath, f)
        # print(fl)
        data = np.loadtxt(fl, dtype = "str", delimiter = ",", encoding = "utf-8")
        data = list(data.T)
        tmp = pd.to_timedelta(data[2][-1][-8:])
        li.append([tmp, data[0][0]])