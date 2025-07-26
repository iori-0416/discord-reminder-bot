import discord
from discord.ext import tasks, commands
import datetime  # 時間を扱うために必要
import os
from flask import Flask
from threading import Thread

# --- 設定項目 ---
# Renderの環境変数からトークンを読み込む
BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN") 
CHANNEL_ID = 1305846029257805824 # 通知を送りたいチャンネルのID

# --- トークンが設定されているか確認 ---
if BOT_TOKEN is None:
    print("エラー: Discord Botのトークンが設定されていません。")
    print("RenderのEnvironment VariablesにDISCORD_BOT_TOKENを設定してください。")
    exit() # トークンがない場合はプログラムを終了

# --- Webサーバー機能（Renderのスリープ防止用）---
app = Flask('')

@app.route('/')
def home():
    return "Botは正常に起動しています。"

def run():
  app.run(host='0.0.0.0', port=8080)

def start_web_server():
    t = Thread(target=run)
    t.start()
# --- Webサーバー機能ここまで ---


# --- Discord Bot本体のコード ---

# Botの接続設定
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

# Botが起動したときに一度だけ実行される処理
@bot.event
async def on_ready():
    print(f'{bot.user} としてログインしました')
    # 定期実行タスクを開始
    notify.start()

# 毎日21時に実行されるタスク
# JST（日本時間）で21時を指定
@tasks.loop(time=datetime.time(hour=21, minute=0, tzinfo=datetime.timezone(datetime.timedelta(hours=9))))
async def notify():
    # 今日が平日（月曜=0, ..., 金曜=4）かどうかを判定
    if datetime.date.today().weekday() < 5:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("出勤フォーム入力")
            print(f"#{channel.name} に通知を送信しました。")
        else:
            print(f"エラー: チャンネルID {CHANNEL_ID} が見つかりませんでした。")

# --- Botの起動 ---
start_web_server() # Webサーバーを起動
bot.run(BOT_TOKEN) # Botを起動
