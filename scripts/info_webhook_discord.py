import requests
from colorama import Fore, Back, Style, init

def get_info(webhook_url):
    response = requests.get(webhook_url)
    if response.status_code == 200:
        print(f"{Fore.GREEN} ✔ Webhook information retrieved successfully.{Style.RESET_ALL}")
        print(f"{Fore.GREEN} ✔ Webhook URL: {response.json()['url']}{Style.RESET_ALL}")
        print(f"{Fore.GREEN} ✔ Webhook Channel ID: {response.json()['channel_id']}{Style.RESET_ALL}")
        print(f"{Fore.GREEN} ✔ Webhook Guild ID: {response.json()['guild_id']}{Style.RESET_ALL}")
        print(f"{Fore.GREEN} ✔ Webhook Name: {response.json()['name']}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED} ✖ Error retrieving webhook information.{Style.RESET_ALL}")
        print(f"{Fore.RED} ✖ Status code: {response.status_code}{Style.RESET_ALL}")
        print(f"{Fore.RED} ✖ Message: {response.text}{Style.RESET_ALL}")