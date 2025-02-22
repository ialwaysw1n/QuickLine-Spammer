import discord
import asyncio
import threading
import logging
import sys
import os
import json
from colorama import init, Fore, Style

init(autoreset=True)

logging.getLogger("discord").setLevel(logging.CRITICAL)
logging.getLogger("discord.client").setLevel(logging.CRITICAL)
logging.getLogger("discord.gateway").setLevel(logging.CRITICAL)
logging.getLogger("discord.http").setLevel(logging.CRITICAL)

def token():
    with open("config.json", "r") as file:
        config = json.load(file)
    return config.get("TOKEN", "")

TOKEN = token()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.members = True

bot = discord.Client(intents=intents)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

ascii_banner = f"""{Fore.MAGENTA}
 ██████  ██    ██ ██  ██████ ██   ██     ██      ██ ███    ██ ███████ 
██    ██ ██    ██ ██ ██      ██  ██      ██      ██ ████   ██ ██      
██    ██ ██    ██ ██ ██      █████       ██      ██ ██ ██  ██ █████   
██ ▄▄ ██ ██    ██ ██ ██      ██  ██      ██      ██ ██  ██ ██ ██      
 ██████   ██████  ██  ██████ ██   ██     ███████ ██ ██   ████ ███████ 
   ▀▀                                                                
                          Made by: script.er                                                                    
{Style.RESET_ALL}
"""

def console_interface():
    while True:
        clear_console()
        print(ascii_banner)
        print(Fore.MAGENTA + "[1] Spam")
        print(Fore.MAGENTA + "[2] Kick All")
        print(Fore.MAGENTA + "[3] Ban All")
        print(Fore.MAGENTA + "[4] Delete All Channels")
        print(Fore.MAGENTA + "[5] Delete All Roles")
        print(Fore.MAGENTA + "[6] Create Channels")
        print("[7] Exit")

        choice = input(Fore.YELLOW + "Select an option: " + Style.RESET_ALL)

        if choice == "1":
            clear_console()
            message_to_send = input(Fore.CYAN + "What would you like to spam: " + Style.RESET_ALL)
            
            clear_console()
            while True:
                try:
                    send_count = int(input(Fore.CYAN + "How many times do you want that message to be spammed: " + Style.RESET_ALL))
                    break
                except ValueError:
                    clear_console()
                    print(Fore.RED + "Please enter a valid number.\n" + Style.RESET_ALL)

            asyncio.run_coroutine_threadsafe(send_message_to_all_channels(message_to_send, send_count), bot.loop)
            
            clear_console()
            print(Fore.GREEN + "Spamming...\n" + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to return to the main menu..." + Style.RESET_ALL)

        elif choice == "2":
            clear_console()
            asyncio.run_coroutine_threadsafe(kick_all_users(), bot.loop)
            clear_console()
            print(Fore.GREEN + "All users have been kicked...\n" + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to return to the main menu..." + Style.RESET_ALL)

        elif choice == "3":
            clear_console()
            asyncio.run_coroutine_threadsafe(ban_all_users(), bot.loop)
            clear_console()
            print(Fore.GREEN + "All users have been banned...\n" + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to return to the main menu..." + Style.RESET_ALL)

        elif choice == "4":
            clear_console()
            asyncio.run_coroutine_threadsafe(delete_all_channels(), bot.loop)
            clear_console()
            print(Fore.GREEN + "All channels have been deleted...\n" + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to return to the main menu..." + Style.RESET_ALL)

        elif choice == "5":
            clear_console()
            asyncio.run_coroutine_threadsafe(delete_all_roles(), bot.loop)
            clear_console()
            print(Fore.GREEN + "All roles have been deleted...\n" + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to return to the main menu..." + Style.RESET_ALL)

        elif choice == "6":
            clear_console()
            print(Fore.CYAN + "Creating channels...\n" + Style.RESET_ALL)

            channel_name = input(Fore.CYAN + "Enter the name of the channels: " + Style.RESET_ALL)

            while True:
                try:
                    channel_count = int(input(Fore.CYAN + "How many channels do you want to create: " + Style.RESET_ALL))
                    break
                except ValueError:
                    print(Fore.RED + "Please enter a valid number.\n" + Style.RESET_ALL)

            asyncio.run_coroutine_threadsafe(create_channels(channel_name, channel_count), bot.loop)

            clear_console()
            print(Fore.GREEN + f"{channel_count} channels have been created...\n" + Style.RESET_ALL)
            input(Fore.YELLOW + "Press Enter to return to the main menu..." + Style.RESET_ALL)

        elif choice == "7":
            clear_console()
            print(Fore.RED + "Exiting console..." + Style.RESET_ALL)
            sys.exit()

        else:
            clear_console()
            print(Fore.YELLOW + "Invalid choice. Try again." + Style.RESET_ALL)

async def send_message_to_all_channels(message, count):
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                for _ in range(count):
                    await channel.send(message)
                    await asyncio.sleep(0.5)

async def kick_all_users():
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        members = [member for member in guild.members if not member.bot]
        for member in members:
            try:
                await member.kick()
                print(Fore.GREEN + f"Kicked {member.name} ({member.id}) from {guild.name}" + Style.RESET_ALL)
                await asyncio.sleep(1)
            except discord.Forbidden:
                print(Fore.RED + f"Bot does not have permission to kick {member.name}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Failed to kick {member.name}: {e}" + Style.RESET_ALL)

async def ban_all_users():
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        members = [member for member in guild.members if not member.bot]
        for member in members:
            try:
                await member.ban()
                print(Fore.GREEN + f"Banned {member.name} ({member.id}) from {guild.name}" + Style.RESET_ALL)
                await asyncio.sleep(1)
            except discord.Forbidden:
                print(Fore.RED + f"Bot does not have permission to ban {member.name}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Failed to ban {member.name}: {e}" + Style.RESET_ALL)

async def delete_all_channels():
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                await channel.delete()
                print(Fore.GREEN + f"Channel deleted: {channel.name}" + Style.RESET_ALL)
                await asyncio.sleep(1)
            except discord.Forbidden:
                print(Fore.RED + f"Bot does not have permission to delete channel {channel.name}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Failed to delete channel {channel.name}: {e}" + Style.RESET_ALL)

async def delete_all_roles():
    await bot.wait_until_ready()
    
    for guild in bot.guilds:
        for role in guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    print(Fore.GREEN + f"Role deleted: {role.name}" + Style.RESET_ALL)
                    await asyncio.sleep(1)
                except discord.Forbidden:
                    print(Fore.RED + f"Bot does not have permission to delete role {role.name}" + Style.RESET_ALL)
                except Exception as e:
                    print(Fore.RED + f"Failed to delete role {role.name}: {e}" + Style.RESET_ALL)

async def create_channels(channel_name, channel_count):
    await bot.wait_until_ready()

    for guild in bot.guilds:
        for _ in range(channel_count):
            try:
                await guild.create_text_channel(channel_name)
                print(Fore.GREEN + f"Channel created: {channel_name}" + Style.RESET_ALL)
                await asyncio.sleep(1)
            except discord.Forbidden:
                print(Fore.RED + f"Bot does not have permission to create channel in {guild.name}" + Style.RESET_ALL)
            except Exception as e:
                print(Fore.RED + f"Failed to create channel {channel_name} in {guild.name}: {e}" + Style.RESET_ALL)

def start_console():
    threading.Thread(target=console_interface, daemon=True).start()

if __name__ == "__main__":
    try:
        start_console()  # Start console interface in a separate thread
        bot.run(TOKEN)
    except Exception as e:
        print(f"Error starting bot: {e}")
