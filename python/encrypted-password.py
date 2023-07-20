from getpass import getpass
from jnpr.junos import Device
from colorama import Fore, Style

username = input("username: ")
password = getpass("password: ")
for hostname in hostnames:
    dev = Device(host=hostname, user=username, password=password)
    dev.open()
    response = dev.cli("show configuration system root-authentication encrypted-password | display set")
    dev.close()
    encrypted_password = None
    for line in response.splitlines():
        if "encrypted-password" in line:
            encrypted_password = line.strip()
    if encrypted_password:
        if "$6$" in encrypted_password:
            print(Fore.GREEN + hostname +": updated")
        elif "sha" in encrypted_password:
            print(Fore.RED + hostname +": pending update")
    else:
        print("error parsing config")

# made to keep track of the root password change
# if sha present output is red indicating update needed
# if using sha512 output is green indication password has been updated