from sys import stdout
from jnpr.junos import Device
from getpass import getpass
from colorama import Fore, Style
import re
from lxml.etree import tostring
from lxml import etree
import xml.etree.ElementTree as ET

ew_block = []
xml_dst_array = []
xml_next_array = []
xml_irb_array = []

u = ""
p = getpass("password: ")

dsts = []
with open('next.txt', 'r') as file:
    for line in file:
        line = line.strip()
        dsts.append(line)
    for dst in dsts:
        dev = Device(host=ip, user=u, password=p)
        dev.open()
        next_hop = dev.cli("show route next-hop {dst}")
        dev.close()
        next_hop.append