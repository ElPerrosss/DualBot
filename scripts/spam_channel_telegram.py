import requests
from colorama import Fore, Style

def spam_channel(token, channel_id, message, times, proxies):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    if not proxies:
        print(f"{Fore.YELLOW}✔ No proxies will be used. Sending message directly.{Style.RESET_ALL}")
        for i in range(times):
            payload = {
                "chat_id": channel_id,
                "text": message
            }
            try:
                response = requests.post(url, json=payload)
                if response.status_code == 200:
                    print(f"{Fore.YELLOW}- Message {i + 1} sent successfully.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✖ Error sending message. Status code: {response.status_code}{Style.RESET_ALL}")
                    print(f"{Fore.RED}✖ Message: {response.text}{Style.RESET_ALL}")
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}✖ Error sending message: {str(e)}{Style.RESET_ALL}")
                continue
    else:
        for i in range(times):
            proxy = {"http": f"http://{proxies[i % len(proxies)]}", "https": f"http://{proxies[i % len(proxies)]}"}
            
            payload = {
                "chat_id": channel_id,
                "text": message
            }
            try:
                response = requests.post(url, json=payload, proxies=proxy)
                if response.status_code == 200:
                    print(f"{Fore.YELLOW}- Message {i + 1} sent successfully using proxy {proxies[i % len(proxies)]}.{Style.RESET_ALL}")
                else:
                    print(f"{Fore.RED}✖ Error sending message with proxy {proxies[i % len(proxies)]}.{Style.RESET_ALL}")
                    print(f"{Fore.RED}✖ Status code: {response.status_code}{Style.RESET_ALL}")
                    print(f"{Fore.RED}✖ Message: {response.text}{Style.RESET_ALL}")
            except requests.exceptions.RequestException as e:
                print(f"{Fore.RED}✖ Error sending message with proxy {proxies[i % len(proxies)]}: {str(e)}{Style.RESET_ALL}")
                continue