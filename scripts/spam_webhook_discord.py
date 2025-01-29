import requests
from colorama import Fore, Back, Style, init

def spam_webhook(webhook_url, message, times):
    for i in range(times):
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 204:
            print(f"{Fore.YELLOW}[-] Message {i + 1} sent successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[✖] Error sending message.{Style.RESET_ALL}")
            print(f"{Fore.RED}[✖] Status code: {response.status_code}{Style.RESET_ALL}")
            print(f"{Fore.RED}[✖] Message: {response.text}{Style.RESET_ALL}")