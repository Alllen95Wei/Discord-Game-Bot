import discord
from dotenv import load_dotenv
import os

import log_writter

client = discord.Client()


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.listening, name="YURI IS GREAT!")
    await client.change_presence(status=discord.Status.idle, activity=music)
    log_writter.write_log("-------------------------------------------------------------\n", True)
    log_writter.write_log("\n登入成功！\n目前登入身份：" +
                          str(client.user) + "\n以下為使用紀錄(只要開頭訊息有\"y!\"，則這則訊息和系統回應皆會被記錄)：\n\n")


@client.event
async def on_message(message):
    msg_in = message.content
    if message.author == client.user:
        return
    elif msg_in.startswith("ag!"):
        use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
        log_writter.write_log(use_log)


# 取得TOKEN
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))
client.run(TOKEN)
