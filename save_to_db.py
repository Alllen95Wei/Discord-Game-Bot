import os
import time as t
import pymysql
from dotenv import load_dotenv


def save_data(starter, target_num, time=int(t.time())):
    base_dir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(dotenv_path=os.path.join(base_dir, "DB_PW.env"))
    PW = str(os.getenv("PW"))
    db_settings = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": PW,
        "db": "guessnum_data",
        "charset": "utf8"
    }
    try:
        db = pymysql.connect(**db_settings)
        with db.cursor() as cursor:
            print("已連線至資料庫。")
            target_num = "".join(str(i) for i in target_num)
            command = "INSERT INTO charts(time, starter, target_num) VALUES ({0}, {1}, {2})".format(time, starter,
                                                                                                    target_num)
            try:
                cursor.execute(command)
                db.commit()
                print("Data saved")
            except Exception as e:
                db.rollback()
                print("Data save failed({0})".format(e))
    except Exception as e:
        print(e)
