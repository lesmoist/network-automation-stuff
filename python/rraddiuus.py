from sys import stdout
from jnpr.junos import Device
from getpass import getpass
from colorama import Fore, Style
import logging

username = input("username: ")
password = getpass("password: ")

logging.basicConfig(filename='radius_servers.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

for ip in lxa:
    dev = Device(host=ip, user=username, password=password)
    dev.open()
    output = dev.cli("show configuration system radius-server")
    lines = output.splitlines()
    first_server = None
    for line in lines:
        if line.startswith(""):
            print(Fore.GREEN + ip +": correct primary")
        else:
            print(Fore.RED + ip +": incorrect primary")
    dev.close()
for ip in hrz:
    dev = Device(host=ip, user=username, password=password)
    dev.open()
    output = dev.cli("show configuration system radius-server")
    lines = output.splitlines()
    first_server = None
    for line in lines:
        if line.startswith(""):
            print(Fore.GREEN + ip +": correct primary")
        else:
            print(Fore.RED + ip +": incorrect primary")
    dev.close()