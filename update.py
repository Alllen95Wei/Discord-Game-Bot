def update(pid, os_name):
    import subprocess
    from time import sleep

    subprocess.run("git fetch --all")
    subprocess.run("git reset --hard origin/main")
    subprocess.run("git pull")
    sleep(5)
    subprocess.Popen("python main.py", creationflags=subprocess.CREATE_NEW_CONSOLE)
    if os_name == "Windows":
        subprocess.run("taskkill /f /PID {0}".format(pid))
    elif os_name == "Linux":
        subprocess.run("kill -9 {0}".format(pid))


if __name__ == "__main__":
    import os
    from platform import system

    update(os.getpid(), system())
