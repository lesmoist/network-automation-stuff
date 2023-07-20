from getpass import getpass
from jnpr.junos import Device
from colorama import Fore, Style

username = input("username: ")
password = getpass("password: ")
for location, hostnames in locations.items():
    print(Fore.BLUE + location.capitalize() + ":")
    for hostname in hostnames:
        try:
            dev = Device(host=hostname, user=username, password=password)
            dev.open()
            try:
                response = dev.cli("show configuration system root-authentication encrypted-password | display set")
            except Exception as e:
                print(Fore.YELLOW + f"error executing the command on the remote host {hostname}: {str(e)}")
                dev.close()
                print(Fore.RED + "[MALFORMED COMMAND] QUITTING SCRIPT!")
                exit()
            dev.close()
            encrypted_password = None
            for line in response.splitlines():
                if "encrypted-password" in line:
                    encrypted_password = line.strip()
                if encrypted_password:
                    if "$6$" in encrypted_password:
                        print(Fore.GREEN + hostname +": updated")
                    else:
                        print(Fore.RED + hostname +": pending")
        except Exception as e:
            print(Fore.YELLOW + f"error initializing the jnpr.junos device connection for {hostname}: {str(e)}")

# now includes error handling for the remote connections
# can now do in bulk instead of per location
# dev.cli("xxxxxxx") can be modified to send any command to all devices and compare
# if statements/variables will need to be adjusted depending on the command(s) being sent
# also added in error handling to the command being sent to the device

# THIS SCRIPT IS BEING SENT AT THE CLI LEVEL PER USER FORMAT COMMANDS ACCORDINGLY 