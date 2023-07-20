from jnpr.junos import Device
from jnpr.junos.utils.fs import FS
from pprint import pprint
from getpass import getpass
else:
    print("error reading location")
username = input("username: ")
password = getpass("password: ")

for hostname in hostnames:
    dev = Device(host=hostname, user=username, password=password)
    dev.open()
    facts = dev.facts

    filename = f"{hostname}_facts.txt"
    with open(filename, mode='w') as file:
        for key, value in facts.items():
            file.write(f"{key}: {value}\n")

    dev.close()