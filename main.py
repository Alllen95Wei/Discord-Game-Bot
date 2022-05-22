import discord
from dotenv import load_dotenv
import os
from random import randint

import log_writter

client = discord.Client()


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.playing, name="快要有點什麼的機器人")
    await client.change_presence(status=discord.Status.online, activity=music)
    log_writter.write_log("-------------------------------------------------------------\n", True)
    log_writter.write_log("\n登入成功！\n目前登入身份：" +
                          str(client.user) + "\n以下為使用紀錄(只要開頭訊息有\"ag!\"，則這則訊息和系統回應皆會被記錄)：\n\n")


test_mode = False


@client.event
async def on_message(message):
    global test_mode
    final_msg_list = []
    msg_in = message.content
    default_color = 0x584BF1
    error_color = 0xF1411C
    if message.author == client.user:
        return
    elif msg_in.startswith("ag!"):
        if msg_in == "ag!test":
            use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
            log_writter.write_log(use_log)
            if test_mode:
                test_mode = False
                embed = discord.Embed(title="測試模式", description="測試模式已**關閉**。", color=default_color)
                final_msg_list.append(embed)
            else:
                test_mode = True
                embed = discord.Embed(title="測試模式", description="測試模式已**開啟**。", color=default_color)
                final_msg_list.append(embed)
        elif test_mode:
            return
        else:
            use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
            log_writter.write_log(use_log)
            parameter = msg_in[3:]
            if parameter == "":
                embed = discord.Embed(title="Allen Game Bot在此！", description="使用`ag!help`來取得指令支援。", color=default_color)
                final_msg_list.append(embed)
            elif parameter[:4] == "help":
                embed = discord.Embed(title="help", description="嗯。什麼都沒有。我已經開工了！敬請期待！。", color=default_color)
                final_msg_list.append(embed)
            elif parameter[:8] == "guessnum" or parameter[:2] == "gn":
                starter = message.author
                if parameter == "guessnum" or parameter == "gn":
                    target_num = [randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9)]
                    embed = discord.Embed(title="guessnum", description="完成設定！", color=default_color)
                    embed.add_field(name="發起者", value="<@{0}>".format(starter.id), inline=False)
                    embed.add_field(name="目標數字", value="({0}位數數字)".format(len(target_num)), inline=False)
                    embed.add_field(name="模式", value="同樂模式", inline=False)
                    final_msg_list.append(embed)
                else:
                    game_set = parameter.split(" ")
                    del game_set[0]
                    target_num_str = game_set[0]
                    if target_num_str.isdigit():
                        target_num = []
                        for i in range(len(target_num_str)):
                            target_num.append(int(target_num_str[i]))
                        if len(target_num) > 8:
                            embed = discord.Embed(title="guessnum", description="請指定一個**8位以內**的數字。", color=error_color)
                            final_msg_list.append(embed)
                        else:
                            embed = discord.Embed(title="guessnum", description="完成設定！", color=default_color)
                            embed.add_field(name="目標數字", value="({0}位數數字)".format(len(target_num)), inline=False)
                            embed.add_field(name="模式", value="同樂模式", inline=False)
                            final_msg_list.append(embed)
                    else:
                        embed = discord.Embed(title="guessnum", description="請輸入一個數字。", color=error_color)
                        final_msg_list.append(embed)
            elif parameter[:4] == "ping":
                embed = discord.Embed(title="ping", description="延遲：{0}ms"
                                      .format(str(round(client.latency * 1000))), color=default_color)
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
