#!usr/bin/env python
from scapy.all import *

sr1(IP(dst="dreamzite.com")/TCP(dport=443, flags="S"))
send(IP(dst="dreamzite.com")/TCP(dport=443, flags="A"))
