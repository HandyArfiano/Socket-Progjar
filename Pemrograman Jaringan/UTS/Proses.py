import subprocess

commands = [
    "python Server.py",
    "python 01.Client.py",
    "python 02.Client.py",
    "python 03.Client.py",
    "python 04.Client.py",
    "python 05.Client.py",
    "python 06.Client.py",
    "python 07.Client.py",
    "python 08.Client.py",
    "python 09.Client.py",
    "python 10.Client.py",
]

for command in commands:
    subprocess.Popen(["start", "cmd", "/k", command], shell=True)