from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from getpass import getpass


username = input("username: ")
password = getpass("password: ")

for hostname in hostnames:
    dev = Device(host=hostname, user=username, password=password)
    dev.open()
    config_output = dev.cli("show config")
    with open(f"{hostname}.config", "w") as f:
        f.write(config_output)
    dev.close()