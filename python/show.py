from getpass import getpass
from jnpr.junos import Device
from colorama import Fore, Style

    print("error reading location")
username = input("username: ")
password = getpass("password: ")
for hostname in hostnames:
    dev = Device(host=hostname, user=username, password=password)
    dev.open()
    response = dev.cli("show configuration system login password | display set")
    dev.close()
    root_login_config = None
    for line in response.splitlines():
        if "format" in line:
            root_login_config = line.strip()
    if root_login_config:
        if "sha1" in root_login_config:
            print(Fore.RED + hostname +": using sha1" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + hostname +": sha512" + Style.RESET_ALL)
    else:
        print("error parsing config")