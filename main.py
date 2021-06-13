import requests
from threading import Thread
from colorama import Fore
import logging
from time import sleep
from os import system

logging.basicConfig(level=logging.INFO, format="%(message)s")

system("")

names = open('usernames.txt', 'r').read().splitlines()  # read names from file


def check(name):
    r = requests.get(f'https://steamcommunity.com/id/{name}')
    if "<h3>The specified profile could not be found.</h3><br><br>" in r.text:
        logging.info(f"{Fore.GREEN}[AVAILABLE] {name}")
        with open('available.txt', 'a') as f:
            f.write(name + '\n')
    elif "Steam Community ::" in r.text:
        logging.info(f"{Fore.RED}[UNAVAILABLE] {name}")
    else:
        logging.info(f"{Fore.RED}[ERROR] Received status code {r.status_code} on {name}")
        logging.info(r.text)


print(f"{Fore.GREEN}Started check for {len(names)} usernames on dsc.bio")

threads = []
for name in names:
    threads.append(Thread(target=check, args=[name]))
for t in threads:
    t.start()
    sleep(0.02)
for t in threads:
    t.join()

print(f"{Fore.GREEN}Done checking.")
print(Fore.RESET)
