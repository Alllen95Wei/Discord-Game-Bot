def update(pid, os_name):
    import shlex
    import subprocess
    from time import sleep

    subprocess.run(shlex.split("git fetch --all"))
    subprocess.run(shlex.split("git reset --hard origin/main"))
    subprocess.run(shlex.split("git pull"))
    sleep(5)
    subprocess.Popen("python main.py", shell=True)
    if os_name == "Windows":
        subprocess.run(shlex.split("taskkill /f /PID {0}".format(pid)))
    elif os_name == "Linux":
        subprocess.run(shlex.split("kill -9 {0}".format(pid)))


if __name__ == "__main__":
    import os
    from platform import system

    update(os.getpid(), system())
