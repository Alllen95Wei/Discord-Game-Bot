import time
import discord
from dotenv import load_dotenv
import os
from random import randint
import subprocess

import log_writter
import save_to_db as stdb

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    music = discord.Activity(type=discord.ActivityType.playing, name="猜數字遊戲(？)")
    await client.change_presence(status=discord.Status.online, activity=music)
    log_writter.write_log("-------------------------------------------------------------\n", True)
    log_writter.write_log("\n登入成功！\n目前登入身份：" +
                          str(client.user) + "\n以下為使用紀錄(只要開頭訊息有\"ag!\"，則這則訊息和系統回應皆會被記錄)：\n\n")


test_mode = False


@client.event
async def on_message(message):
    global test_mode
    final_msg_list = []
    msg_in = str(message.content)
    default_color = 0x584BF1
    error_color = 0xF1411C
    if message.author == client.user:
        return
    elif msg_in.isdigit():
        if test_mode:
            return
        else:
            use_log = str(message.channel) + "/" + str(message.author) + ":\n" + msg_in + "\n\n"
            log_writter.write_log(use_log)
            game_data_dir = os.path.abspath(os.path.dirname(__file__)) + "\\data\\"
            now_playing_channel = [f for f in os.listdir(game_data_dir) if
                                   os.path.isfile(os.path.join(game_data_dir, f))]
            if "{0}.txt".format(str(message.channel.id)) in now_playing_channel:
                with open(game_data_dir + str(message.channel.id) + ".txt", "r", encoding="utf-8") as txt:
                    game_data = eval(txt.read())
                    txt.close()
                if len(msg_in) != len(str(game_data["target_num"])):
                    embed = discord.Embed(title="guessnum", description="請輸入{0}位數的數字。"
                                          .format(len(str(game_data["target_num"]))), color=error_color)
                    final_msg_list.append(embed)
                else:
                    if "guess_times" in game_data.keys():
                        game_data["guess_times"] += 1
                    else:
                        game_data["guess_times"] = 1
                    current_guess_num = []
                    target_num_list = []
                    for i in range(len(msg_in)):
                        current_guess_num.append(int(msg_in[i]))
                    for i in range(len(game_data["target_num"])):
                        target_num_list.append(int(game_data["target_num"][i]))
                    answer_status = []
                    for i in range(len(current_guess_num)):
                        if current_guess_num[i] == target_num_list[i]:
                            answer_status.append(2)
                        elif current_guess_num[i] in target_num_list:
                            answer_status.append(1)
                        else:
                            answer_status.append(0)
                    if answer_status == [2, 2, 2, 2]:
                        embed = discord.Embed(title="guessnum", description="恭喜你答對了！", color=default_color)
                        embed.add_field(name="答案", value="`{0}`".format(msg_in), inline=False)
                        embed.add_field(name="次數", value=str(game_data["guess_times"]), inline=False)
                        final_msg_list.append(embed)
                        try:
                            subprocess.Popen("rm {0}".format(os.path.join(game_data_dir, "{0}.txt"
                                                                          .format(message.channel.id))))
                        except Exception as e:
                            embed = discord.Embed(title="guessnum", description="發生錯誤。\n{0}".format(e),
                                                  color=error_color)
                            final_msg_list.append(embed)
                    else:
                        answer_status_str = ""
                        for n in range(len(answer_status)):
                            if answer_status[n] == 2:
                                answer_status[n] = ":green_circle:"
                            elif answer_status[n] == 1:
                                answer_status[n] = ":yellow_circle:"
                            else:
                                answer_status[n] = ":red_circle:"
                            answer_status_str += answer_status[n]
                        if ":green_circle:" in answer_status_str:
                            title = "似乎猜中了一些！"
                        elif "yellow_circle" in answer_status_str:
                            title = "接近了！"
                        else:
                            title = "呃...再加把勁！"
                        embed = discord.Embed(title="guessnum", description=title, color=default_color)
                        embed.add_field(name="你的答案", value="`{0}`".format(msg_in), inline=False)
                        embed.add_field(name="結果", value=answer_status_str, inline=False)
                        embed.set_footer(text="第{0}次猜測".format(str(game_data["guess_times"])))
                        final_msg_list.append(embed)
                with open(game_data_dir + str(message.channel.id) + ".txt", "w", encoding="utf-8") as txt:
                    txt.write(str(game_data))
                    txt.close()
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
                embed = discord.Embed(title="Allen Game Bot在此！", description="使用`ag!help`來取得指令支援。",
                                      color=default_color)
                final_msg_list.append(embed)
            elif parameter[:4] == "help":
                embed = discord.Embed(title="help", description="一隻可以用來玩猜數字的機器人。", color=default_color)
                embed.add_field(name="`help`", value="顯示此協助訊息。", inline=False)
                embed.add_field(name="`guessnum(gn)`", value="開始猜數字遊戲。", inline=False)
                embed.add_field(name="`ping`", value="查看本機器人的延遲毫秒數。", inline=False)
                final_msg_list.append(embed)
            elif parameter[:8] == "guessnum" or parameter[:2] == "gn":
                game_data_dir = os.path.abspath(os.path.dirname(__file__)) + "\\data\\"
                now_playing_channel = [f for f in os.listdir(game_data_dir) if
                                       os.path.isfile(os.path.join(game_data_dir, f))]
                if "{0}.txt".format(str(message.channel.id)) in now_playing_channel:
                    embed = discord.Embed(title="錯誤", description="此頻道目前已正在進行遊戲。", color=error_color)
                    final_msg_list.append(embed)
                else:
                    starter = message.author
                    if parameter == "guessnum" or parameter == "gn":
                        target_num = "{0}{1}{2}{3}".format(randint(0, 9), randint(0, 9), randint(0, 9), randint(0, 9))
                        embed = discord.Embed(title="guessnum", description="完成設定！", color=default_color)
                        embed.add_field(name="發起者", value="<@{0}>".format(starter.id), inline=False)
                        embed.add_field(name="目標數字", value="({0}位數數字)".format(len(target_num)), inline=False)
                        try:
                            true_member_count = len([m for m in message.channel.guild.members if not m.bot])
                        except AttributeError:
                            true_member_count = 1
                        if true_member_count == 1:
                            mode = "單人模式"
                        else:
                            mode = "同樂模式"
                        embed.add_field(name="模式", value=mode, inline=False)
                        embed.add_field(name="發起時間", value="<t:{0}:R>".format(int(time.time())), inline=False)
                        embed.add_field(name="遊玩頻道", value="<#{0}>".format(message.channel.id), inline=False)
                        embed.add_field(name="說明", value="[點我](https://is.gd/ZE2aFA)來獲得關於結果的判讀說明。",
                                        inline=False)
                        stdb.save_data(starter.id, target_num, message.channel.id)
                        final_msg_list.append(embed)
                    else:
                        game_set = parameter.split(" ")
                        del game_set[0]
                        target_num = game_set[0]
                        if target_num.isdigit():
                            if len(target_num) > 8:
                                embed = discord.Embed(title="guessnum", description="請指定一個**8位以內**的數字。",
                                                      color=error_color)
                                final_msg_list.append(embed)
                            else:
                                try:
                                    await message.delete()
                                    embed = discord.Embed(title="guessnum", description="完成設定！",
                                                          color=default_color)
                                    embed.add_field(name="目標數字", value="({0}位數數字)".format(len(target_num)),
                                                    inline=False)
                                    embed.add_field(name="模式", value="同樂模式", inline=False)
                                    embed.add_field(name="發起時間", value="<t:{0}>".format(int(time.time())),
                                                    inline=False)
                                    embed.add_field(name="遊玩頻道", value="<#{0}>".format(message.channel.id),
                                                    inline=False)
                                    stdb.save_data(starter.id, target_num, message.channel.id)
                                except Exception as e:
                                    embed = discord.Embed(title="錯誤", description="無法刪除你的訊息。({0})".format(e),
                                                          color=error_color)
                                final_msg_list.append(embed)
                        else:
                            embed = discord.Embed(title="guessnum", description="請輸入一個數字。", color=error_color)
                            final_msg_list.append(embed)
            elif parameter[:6] == "cancel":
                game_data_dir = os.path.abspath(os.path.dirname(__file__)) + "\\data\\"
                now_playing_channel = [f for f in os.listdir(game_data_dir) if
                                       os.path.isfile(os.path.join(game_data_dir, f))]
                if "{0}.txt".format(str(message.channel.id)) in now_playing_channel:
                    with open(game_data_dir + str(message.channel.id) + ".txt", "r", encoding="utf-8") as txt:
                        game_data = eval(txt.read())
                    if message.author.id == game_data["starter"] or message.author.id == message.guild.owner.id:
                        try:
                            subprocess.Popen("rm {0}".format(os.path.join(game_data_dir, "{0}.txt"
                                                                          .format(message.channel.id))))
                            embed = discord.Embed(title="cancel", description="已取消遊戲。", color=default_color)
                            final_msg_list.append(embed)
                        except Exception as e:
                            embed = discord.Embed(title="guessnum", description="發生錯誤。\n{0}".format(e),
                                                  color=error_color)
                            final_msg_list.append(embed)
                    else:
                        msg = "你沒有權限進行此操作。請聯絡發起者(<@{0}>)或伺服器擁有者(<@{1})進行此操作。"\
                            .format(game_data["starter"], message.guild.owner.id)
                        embed = discord.Embed(title="cancel", description=msg, color=error_color)
                        final_msg_list.append(embed)
                else:
                    embed = discord.Embed(title="錯誤", description="此頻道目前未正在進行遊戲。", color=error_color)
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
