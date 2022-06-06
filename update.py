import shlex
import subprocess
from time import sleep


def update(pid, os_name):
    subprocess.run(shlex.split("git fetch --all"))
    subprocess.run(shlex.split("git reset --hard origin/main"))
    subprocess.run(shlex.split("git pull"))
    sleep(5)
    restart(pid, os_name)


def restart(pid, os_name):
    subprocess.Popen("python main.py", shell=True)
    if os_name == "Windows":
        subprocess.run(shlex.split("taskkill /f /PID {0}".format(pid)))
    elif os_name == "Linux":
        subprocess.run(shlex.split("kill -9 {0}".format(pid)))


if __name__ == "__main__":
    import os
    from platform import system

    update(os.getpid(), system())
