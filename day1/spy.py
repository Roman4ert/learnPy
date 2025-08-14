#!/usr/bin/env python3
import os
import platform
import psutil
import subprocess
import time
from colorama import Fore, Back, Style

def get_user():
    return os.getenv("USER") or subprocess.getoutput("whoami")

def get_kernel():
    return platform.release()

def get_cpu_load():
    return psutil.cpu_percent(interval=1)

def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent

def get_top_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    processes.sort(key=lambda p: p['cpu_percent'], reverse=True)
    return processes[:5]

def write_file():
    with open("/tmp/spy_report.txt", "a") as f:
        time_stamp = time.ctime(time.time())
        f.write(time_stamp + "\n")
        f.write("="*40 + "\n")
        f.write(Fore.RED + "User: " + f"{get_user()}\n")
        f.write(Fore.RED + "Kernel: " + f"{get_kernel()}\n")
        f.write(Fore.RED + "Load CPU: " + f"{get_cpu_load()}%\n")
        f.write(Fore.RED + "Usage Memory: " + f"{get_memory_usage()}%\n")
        f.write(Fore.RED + "Top 5 Load APP: ")
        for p in get_top_processes():
            f.write(Fore.RED + "pid" + f"={p["pid"]:5} | " + Fore.RED + "CPU" + f"={p["cpu_percent"]:5}% | " + Fore.RED + "name" + f"={p["name"]}\n")
        f.write("="*40 + "\n")


def main():
    write_file()
    print("complete!")

if __name__ == "__main__":
    main()
