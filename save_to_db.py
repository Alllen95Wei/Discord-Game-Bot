import os


def save_data(data, channel_id):
    base_dir = os.path.abspath(os.path.dirname(__file__)) + "\\data\\"
    with open(base_dir + str(channel_id) + ".txt", "w", encoding="utf-8") as txt:
        txt.write(str(data))
