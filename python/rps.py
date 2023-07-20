from getpass import getpass
from jnpr.junos import Device
from colorama import Fore, Style

    print("error reading location")
username = input("username: ")
password = getpass("password: ")
for hostname in hostnames:
    dev = Device(host=hostname, user=username, password=password)
    dev.open()
    response = dev.cli("command here")
    dev.close()
    config = None
    for line in response.splitlines():
        if "" in line:
            config = line.strip()
        if config:
            if "" in config:
                print(Fore.RED + hostname +": xxx" + Style.RESET_ALL)
            elif "" in config:
                print(Fore.Green + hostname +": xxx" + Style.RESET_ALL)
        else:
            print("error parsing config")