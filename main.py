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


test_mode = False


@client.event
async def on_message(message):
    global test_mode
    final_msg_list = []
    msg_in = message.content
    if message.author == client.user:
        return
    elif msg_in.startswith("ag!"):
        if msg_in == "ag!test":
            use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
            log_writter.write_log(use_log)
            if test_mode:
                test_mode = False
                embed = discord.Embed(title="測試模式", description="測試模式已**關閉**。", color=0xFEE4E4)
                final_msg_list.append(embed)
            else:
                test_mode = True
                embed = discord.Embed(title="測試模式", description="測試模式已**開啟**。", color=0xFEE4E4)
                final_msg_list.append(embed)
        elif test_mode:
            return
        else:
            use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
            log_writter.write_log(use_log)
            parameter = msg_in[2:]
            if parameter == "":
                embed = discord.Embed(title="Allen Game Bot在此！", description="使用`ag!help`來取得指令支援。", color=0x584BF1)
                final_msg_list.append(embed)
            elif parameter[:4] == "help":
                embed = discord.Embed(title="help", description="嗯。什麼都沒有。我會考完會開工的。", color=0x584BF1)
                final_msg_list.append(embed)
            elif parameter[:4] == "ping":
                embed = discord.Embed(title="ping", description="延遲：{0}ms"
                                      .format(str(round(client.latency * 1000))), color=0x584BF1)
                final_msg_list.append(embed)
    for i in range(len(final_msg_list)):
        current_msg = final_msg_list[i]
        if isinstance(current_msg, discord.File):
            await message.channel.send(file=final_msg_list[i])
        elif isinstance(current_msg, discord.Embed):
            await message.channel.send(embed=final_msg_list[i])
        elif isinstance(current_msg, str):
            await message.channel.send(final_msg_list[i])
        new_log = str(message.channel) + "/" + str(client.user) + ":\n" + str(final_msg_list[i]) + "\n\n"
        log_writter.write_log(new_log)
    final_msg_list.clear()


# 取得TOKEN
base_dir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(base_dir, "TOKEN.env"))
TOKEN = str(os.getenv("TOKEN"))
client.run(TOKEN)
