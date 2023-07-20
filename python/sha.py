from getpass import getpass
from jnpr.junos import Device
from colorama import Fore, Style

}
username = input("username: ")
password = getpass("password: ")
for location, hostnames in locations.items():
    print(Fore.BLUE + location.capitalize() + ":")
    for hostname in hostnames:
        try:
            dev = Device(host=hostname, user=username, password=password)
            dev.open()
            try:
                response = dev.cli("show configuration system login password | display set")
            except Exception as e:
                print(Fore.YELLOW + f"error executing the command on the remote host {hostname}: {str(e)}")
                dev.close()
                print(Fore.RED + "[MALFORMED COMMAND] QUITTING SCRIPT!")
                exit()
            dev.close()
            admin_password = None
            for line in response.splitlines():
                if "sha1" in line:
                    admin_password = line.strip()
            if admin_password:
                if "sha1" in admin_password:
                    print(Fore.GREEN + hostname +": sha512")
                else:
                    print(Fore.RED + hostname +": sha1")
        except Exception as e:
            print(Fore.YELLOW + f"error initializing the jnpr.junos device connection for {hostname}: {str(e)}")