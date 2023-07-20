from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from getpass import getpass
password = getpass("password: ")
loop = []
dsts = ["8.8.8.8", "8.8.4.4"]
deviceIP = [""]
def run_traceroute(deviceIP):
    try:
        device = Device(host=deviceIP, user='charles.fleming', password=password)
        device.open()
        for dst in dsts:
            traceroute_output = device.rpc.ping_traceroute(host=dst)
            destinations = []
            for hop in traceroute_output.findall('traceroute-results/hop'):
                destinations.append(hop.findtext('host'))
            if destinations[0] == destinations[2]:
                print("checking for routing loop")
                if destinations[1] == destinations[3]:
                    destinations.append(loop)
            device.close()
    except ConnectError as e:
        print(f"{e}")