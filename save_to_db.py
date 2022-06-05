import os
from platform import system


def save_data(data, channel_id):
    if system() == "Windows":
        base_dir = os.path.abspath(os.path.dirname(__file__)) + "\\data\\"
    else:
        base_dir = os.path.abspath(os.path.dirname(__file__)) + "/data/"
    with open(base_dir + str(channel_id) + ".txt", "w", encoding="utf-8") as txt:
        txt.write(str(data))
