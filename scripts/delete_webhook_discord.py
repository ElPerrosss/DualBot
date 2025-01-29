import requests
from colorama import Fore, Back, Style, init

def delete_webhook(webhook_url):
    response = requests.delete(webhook_url)
    
    if response.status_code == 204:
        print(f"{Fore.GREEN} ✔ Webhook deleted successfully.{Style.RESET_ALL}")
    elif response.status_code == 404:
        print(f"{Fore.YELLOW} - Webhook not found.{Style.RESET_ALL}")
    elif response.status_code == 401:
        print(f"{Fore.RED} ✖ Unauthorized request.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED} ✖ Error deleting webhook.{Style.RESET_ALL}")
        print(f"{Fore.RED} ✖ Status code: {response.status_code}{Style.RESET_ALL}")
        print(f"{Fore.RED} ✖ Message: {response.text}{Style.RESET_ALL}")
