import os
import time


def write_log(content, no_time_stamp=False):
    log = content
    if not no_time_stamp:
        local_time = time.localtime()
        time_stamp = time.strftime("%Y-%m-%d %p %I:%M:%S", local_time)
        log = "[" + time_stamp + "]" + log
    try:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        log_file = open(os.path.join(base_dir, "log.txt"), mode="a", encoding="utf-8")
        log_file.write(log)
        log_file.close()
    except Exception as e:
        print("無法寫入記錄檔。(" + str(e) + ")")
    print(log, end="")
