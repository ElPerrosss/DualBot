import os
import requests
import ctypes
from colorama import Fore, Back, Style, init
from scripts.delete_webhook_discord import delete_webhook
from scripts.spam_webhook_discord import spam_webhook
from scripts.info_webhook_discord import get_info
from scripts.spam_channel_telegram import spam_channel

def get_version(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text.strip()
        else:
            print(f"{Fore.RED}[✘] Error to get version.{Style.RESET_ALL}")
            return "unknown"
    except requests.RequestException as e:
        print(f"{Fore.RED}[✘] We couldn't connect to the server.{Style.RESET_ALL}")
        return "unknown"
    
def check_proxy(proxy):
    test_url = "https://httpbin.org/ip"  
    try:
        response = requests.get(test_url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=5)
        if response.status_code == 200:
            print(f"{Fore.GREEN}✔ Proxy {proxy} is working.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}✖ Proxy {proxy} failed with status code {response.status_code}.{Style.RESET_ALL}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}✖ Proxy {proxy} is not working: {str(e)}{Style.RESET_ALL}")
        return False

def load_proxies():
    proxies = []
    try:
        with open("proxies.txt", "r") as f:
            proxies = [line.strip() for line in f.readlines() if line.strip()]
        if proxies:
            proxy = len(proxies)
            print(f"{Fore.GREEN} ✔ Proxies loaded: {proxy}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED} ✖ No valid proxies found in proxies.txt. {Style.RESET_ALL}")
    except FileNotFoundError:
        print(f"{Fore.RED} ✖ We couldn't find the proxies.txt file. {Style.RESET_ALL}")
    return proxies

def save_working_proxies(working_proxies):
    with open("working_proxies.txt", "w") as f:
        for proxy in working_proxies:
            f.write(f"{proxy}\n")
    print(f"{Fore.GREEN}✔ Working proxies saved to 'working_proxies.txt'.{Style.RESET_ALL}")

def check_and_save_working_proxies():
    proxies = load_proxies()
    working_proxies = []
    
    for proxy in proxies:
        if check_proxy(proxy):
            working_proxies.append(proxy)

    if working_proxies:
        save_input = input(f"{Fore.BLUE} ● {Fore.WHITE}Do you want to save the working proxies to 'working_proxies.txt'? (yes/no): ").strip().lower()
        if save_input == "yes":
            save_working_proxies(working_proxies)
        else:
            print(f"{Fore.YELLOW}✔ Skipping save operation.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}✖ No working proxies found.{Style.RESET_ALL}")


def set_console_title(title):
    if os.name == "nt":  
        if "powershell" in os.environ.get("TERM", "").lower(): 
            os.system(f"$host.ui.RawUI.WindowTitle = '{title}'")
        else:
            os.system(f"title {title}")
    else: 
        os.system(f"echo -ne '\033]0;{title}\007'")

def clear_screen():
    if os.name == "nt": 
        os.system("cls")
    else: 
        os.system("clear")

def banner():
    version_url = "https://raw.githubusercontent.com/ElPerrosss/TelegramSpam/refs/heads/main/extra/version.txt"
    version = get_version(version_url)
    proxies = load_proxies()
    proxies_count = len(proxies)
    clear_screen()
    set_console_title(f"DualBot v{version} - Proxies loaded: {proxies_count}")
    print(f"""
     {Fore.RED}    
     {Fore.RED}  ▓█████▄  █    ██  ▄▄▄       ██▓     ▄▄▄▄    ▒█████  ▄▄▄█████▓
     {Fore.RED}  ▒██▀ ██▌ ██  ▓██▒▒████▄    ▓██▒    ▓█████▄ ▒██▒  ██▒▓  ██▒ ▓▒
     {Fore.RED}  ░██   █▌▓██  ▒██░▒██  ▀█▄  ▒██░    ▒██▒ ▄██▒██░  ██▒▒ ▓██░ ▒░
     {Fore.RED}  ░▓█▄   ▌▓▓█  ░██░░██▄▄▄▄██ ▒██░    ▒██░█▀  ▒██   ██░░ ▓██▓ ░ 
     {Fore.RED}  ░▒████▓ ▒▒█████▓  ▓█   ▓██▒░██████▒░▓█  ▀█▓░ ████▓▒░  ▒██▒ ░ 
     {Fore.RED}   ▒▒▓  ▒ ░▒▓▒ ▒ ▒  ▒▒   ▓▒█░░ ▒░▓  ░░▒▓███▀▒░ ▒░▒░▒░   ▒ ░░   
     {Fore.RED}   ░ ▒  ▒ ░░▒░ ░ ░   ▒   ▒▒ ░░ ░ ▒  ░▒░▒   ░   ░ ▒ ▒░     ░    
     {Fore.RED}   ░ ░  ░  ░░░ ░ ░   ░   ▒     ░ ░    ░    ░ ░ ░ ░ ▒    ░      
     {Fore.RED}     ░       ░           ░  ░    ░  ░ ░          ░ ░           
     {Fore.RED}   ░                                       ░           
                                           
    {Fore.YELLOW}     I AM NOT RESPONSIBLE FOR THE MISUSE OF THIS PROGRAM

    {Style.RESET_ALL}""")

def options():
    print(f"""
    {Fore.BLUE}Discord                                        {Fore.CYAN}Telegram
    {Fore.WHITE}[1] Delete webhook                             {Fore.WHITE}[4] Spam telegram channel    
    {Fore.WHITE}[2] Spam webhook
    {Fore.WHITE}[3] Get webhook information

    {Fore.MAGENTA}Extra
    {Fore.WHITE}[5] Check proxies
    """)

def handle_options(option):
    if option == "1":
        webhook = input(f"{Fore.BLUE} ● {Fore.WHITE}Webhook URL: ")
        if not webhook or not webhook.startswith("https://discord.com/api/webhooks/"):
            print(f"{Fore.RED}❌ Invalid webhook URL.{Style.RESET_ALL}")
            return
        delete_webhook(webhook)
    elif option == "2":
        webhook = input(f"{Fore.BLUE} ● {Fore.WHITE}Webhook URL: ")
        if not webhook or not webhook.startswith("https://discord.com/api/webhooks/"):
            print(f"{Fore.RED}❌ Invalid webhook URL.{Style.RESET_ALL}")
            return
        message = input(f"{Fore.BLUE} ● {Fore.WHITE}Message: ")
        times = int(input(f"{Fore.BLUE} ● {Fore.WHITE}Times: "))
        spam_webhook(webhook, message, times)   
    elif option == "3":
        webhook = input(f"{Fore.BLUE} ● {Fore.WHITE}Webhook URL: ")
        if not webhook or not webhook.startswith("https://discord.com/api/webhooks/"):
            print(f"{Fore.RED}❌ Invalid webhook URL.{Style.RESET_ALL}")
            return
        get_info(webhook)
    elif option == "4":
        proxies = load_proxies()

        use_proxies = input(f"{Fore.BLUE} ● {Fore.WHITE}Do you want to use proxies for Telegram spam? (yes/no): ").strip().lower()
        
        if use_proxies == "yes":
            token = input(f"{Fore.BLUE} ● {Fore.WHITE}Telegram bot token: ")
            if not token:
                print(f"{Fore.RED}❌ Invalid token.{Style.RESET_ALL}")
                return
            channel_id = input(f"{Fore.BLUE} ● {Fore.WHITE}Channel ID: ")
            if not channel_id:
                print(f"{Fore.RED}❌ Invalid channel ID.{Style.RESET_ALL}")
                return
            message = input(f"{Fore.BLUE} ● {Fore.WHITE}Message: ")
            times = int(input(f"{Fore.BLUE} ● {Fore.WHITE}Times: "))
            spam_channel(token, channel_id, message, times, proxies)
        else:
            proxies = []
            token = input(f"{Fore.BLUE} ● {Fore.WHITE}Telegram bot token: ")
            if not token:
                print(f"{Fore.RED}❌ Invalid token.{Style.RESET_ALL}")
                return
            channel_id = input(f"{Fore.BLUE} ● {Fore.WHITE}Channel ID: ")
            if not channel_id:
                print(f"{Fore.RED}❌ Invalid channel ID.{Style.RESET_ALL}")
                return
            message = input(f"{Fore.BLUE} ● {Fore.WHITE}Message: ")
            times = int(input(f"{Fore.BLUE} ● {Fore.WHITE}Times: "))
            spam_channel(token, channel_id, message, times, proxies)
            
        
    elif option == "5":
        check_and_save_working_proxies()

def main():
    banner()
    options()
    option = input(f"{Fore.BLUE}root@srv:~# {Style.RESET_ALL}")
    handle_options(option)

if __name__ == "__main__":
	main()