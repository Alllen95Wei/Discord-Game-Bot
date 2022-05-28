import os
import time as t


def save_data(starter, target_num, channel_id, time=int(t.time())):
    base_dir = os.path.abspath(os.path.dirname(__file__)) + "\\data\\"
    game_data = {"starter": starter, "target_num": target_num, "time": time}
    with open(base_dir + str(channel_id) + ".txt", "a", encoding="utf-8") as txt:
        txt.write(str(game_data))