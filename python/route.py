from sys import stdout
from jnpr.junos import Device
from getpass import getpass
from colorama import Fore, Style
import re
from lxml.etree import tostring
from lxml import etree
import xml.etree.ElementTree as ET

ew_block = ["10.119.4.92"]
xml_dst_array = []
xml_next_array = []
xml_irb_array = []

p = getpass("password: ")

for ip in ew_block:
    dev = Device(host=ip, user="charles.fleming", password=p)
    dev.open()
    route = dev.rpc.get_route_information()
    dev.close()
    # route_string = (tostring(route, encoding='unicode'))
    #rt_dsts = route_string.findall(".//rt-destination")
    rt_dsts = route.findall(".//rt-destination")
    rt_nxt_hops = route.findall(".//to")
    rt_irbs = route.findall(".//via")
    for rt_dst in rt_dsts:
        appelle_moi_si_tu_te_perds = (tostring(rt_dst, encoding='unicode'))
        le_fleur = appelle_moi_si_tu_te_perds.replace("<rt-destination>", "").replace("</rt-destination>", "")
        le_fleur = le_fleur.splitlines()
        for dst in le_fleur:
            xml_dst_array.append(dst)
    for rt_nxt_hop in rt_nxt_hops:
        chercheur_de_soleil = (tostring(rt_nxt_hop, encoding='unicode'))
        reservee = chercheur_de_soleil.replace("<to>", "").replace("</to>", "")
        reservee = reservee.splitlines()
        for ip in reservee:
            xml_next_array.append(ip)
    for rt_irb in rt_irbs:
        a = (tostring(rt_irb, encoding='unicode'))
        b = a.replace("<via>", "").replace("</via>", "")
        b = b.splitlines()
        for irb in b:
            xml_irb_array.append(irb)
for ip_dst in xml_dst_array:
    print(ip_dst)
for next_hop in xml_next_array:
    print(next_hop)
for irbs in xml_irb_array:
    print(irbs)
"""
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
"""