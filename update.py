def update(pid, os):
    import subprocess
    from time import sleep

    subprocess.run("git fetch --all")
    subprocess.run("git reset --hard origin/main")
    subprocess.run("git pull")
    sleep(5)
    subprocess.Popen("python main.py", creationflags=subprocess.CREATE_NEW_CONSOLE)
    if os == "Windows":
        subprocess.run("taskkill /f /PID {0}".format(pid))
    elif os == "Linux":
        subprocess.run("kill -9 {0}".format(pid))
