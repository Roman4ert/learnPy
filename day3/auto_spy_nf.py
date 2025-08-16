#!/usr/bin/env python3
import time
import psutil
import os
import platform
import subprocess
import datetime
from colorama import Fore, Style

LOG_DIR = "/tmp/spy_logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

file_path = os.path.join(LOG_DIR, f"spy_report_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")

INTERVAL = 30

# --- Сообщение о записи ---
def sleep_message():
    print(Fore.GREEN + "Logs write! " + Style.RESET_ALL + f"{time.ctime(time.time())}\n")

# --- Цвета для терминала ---
def overload_color(percent):
    if percent <= 30:
        return Fore.GREEN + f"{percent}%" + Style.RESET_ALL
    elif percent <= 70:
        return Fore.YELLOW + f"{percent}%" + Style.RESET_ALL
    else:
        return Fore.RED + f"{percent}%" + Style.RESET_ALL

# --- Текст для файла ---
def overload_text(percent):
    if percent <= 30:
        return f"{percent}% (Низкая)"
    elif percent <= 70:
        return f"{percent}% (Средняя)"
    else:
        return f"{percent}% (Высокая)"

# --- Топ процессов ---
def get_top_processes():
    proc = []
    for p in psutil.process_iter(["pid", "name", "cpu_percent"]):
        try:
            proc.append(p.info)
        except:
            pass
    proc.sort(key=lambda p: p['cpu_percent'], reverse=True)
    return proc[:5]

# --- Кто онлайн ---
def get_user_online():
    who_online = {}
    users = subprocess.getoutput("who | awk '{print $1}{print $3}'").split()
    for i in range(0, len(users), 2):
        who_online[users[i]] = users[i+1]
    return who_online

# --- Запись лога ---
def write_to_file():
    while True:
        cpu_now = psutil.cpu_percent()
        with open(file_path, "a") as f:
            f.write("Date Logging: " + time.ctime(time.time()) + "\n")
            f.write("User Online Now and when Login:\n")
            online_now = get_user_online()
            f.write("="*40 + "\n")
            for u, t in online_now.items():
                f.write(f"{u}\t\t{t}\n")
                f.write("-"*40 + "\n")
            f.write("="*40 + "\n")
            f.write(f"Active now: \n {time.ctime()} - User: {os.getenv('USER')}, Kernel: {platform.release()}, CPU: {overload_text(cpu_now)}\n")
            f.write("Top-5 processes:\n")
            for i in get_top_processes():
                f.write(f"{i['pid']}\t\t{i['name']}\t\t{overload_text(i['cpu_percent'])}\n")
                f.write("-"*40 + "\n")

        # Сообщение в терминал с цветом
        print(f"[{time.ctime()}] CPU: {overload_color(cpu_now)}")
        sleep_message()
        time.sleep(INTERVAL)

def main():
    try:
        write_to_file()
    except KeyboardInterrupt:
        print("Stop program. Good bye!\n")

if __name__ == "__main__":
    main()
