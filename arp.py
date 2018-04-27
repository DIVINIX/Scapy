#!usr/bin/env python
from scapy.all import *

print("ARP sans ethernet")                                                                                           
rep, non_rep = sr(ARP(op=ARP.who_has, psrc="192.168.9.132", pdst="192.168.9.133"))
rep.show()

print("ARP avec ethernet sur cible")
rep, non_rep = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=ARP.who_has, psrc="192.168.9.132", pdst="192.168.9.133"))
rep.show()

print("ARP avec ethernet sur dreamzite")
rep, non_rep = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=ARP.who_has, psrc="192.168.9.132", pdst="192.168.8.53"))
rep.show()
