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
from discord.ext import commands, tasks
from pprint import pprint
import aiohttp
import numpy as np
import math
from matplotlib import pyplot as plt
from scipy.interpolate import make_interp_spline
from matplotlib import cm
from scipy import optimize
from scipy.optimize import curve_fit
import asyncio

TOKEN = "" # ここに読み込む処理を書く
AuthB = "Bot " + TOKEN
headers = {"Authorization": AuthB}
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
bot = MyBot(command_prefix = '/', description = 'discord bot', intents = discord.Intents.all())
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
# ws = connect_gspread(jsonf, spread_sheet_key)
def embed_out(d: dict, color: str, title: str):
    embed = discord.Embed(
        title = title,
        color = color,
    )
    for k in d.keys():
        embed.add_field(name = k, value = d[k])
# def add_data_by_reaction()
member = dict()
status = dict()
time_in = dict()
time_sum = dict()
id_out = 1254321306133073931
id_hys = 1254321124381298719
id_ygm = 1254321044143996978
# chan_tst = 1157994782874939408
# chan_tgt = 1158005327107739678
CHANNEL_ID = 1254319090735120477
@bot.event
async def on_ready():
    print("Successfully logged in")
    await bot.change_presence(activity = discord.Game("Python"))
@tasks.loop(seconds=1)  # 1分毎にループを実行
async def daily_message():
    now = datetime.datetime.now()
    target_time = datetime.time(hour=21, minute=24)  # 送信したい時刻を指定 
    if now.time() >= target_time:
        channel = bot.get_channel(CHANNEL_ID)
        await channel.send("おはようございます！これは毎日のメッセージです。")
@bot.command(name='vote')
async def vote(ctx, *, question):
    message = await ctx.send(f'投票: {question}\n👍: Yes\n👎: No')
    await message.add_reaction('👍')
    await message.add_reaction('👎')

@bot.command(name='result')
async def result(ctx, message_id: int):
    message = await ctx.fetch_message(message_id)
    thumbs_up = discord.utils.get(message.reactions, emoji='👍')
    thumbs_down = discord.utils.get(message.reactions, emoji='👎')
    await ctx.send(f"👍: {thumbs_up.count - 1} votes\n👎: {thumbs_down.count - 1} votes")

def main():
    bot.run(TOKEN)
if __name__ == "__main__":
    main()