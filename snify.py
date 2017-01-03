#Implementing sniffing in Python, fundamental to approach new MITM attacks
#I'll just begin with some raw decoding to learn the basics, then just move to scapy

import os
import sys
import socket
import struct
from scapy.all import ETH_P_ALL, MTU
from ctypes import *

#Define host address, or take as standard my default

if len(sys.argv) == 2:
	host = sys.argv[1]
else:
	host = "wlan0"

class IP(Structure):

	_fields_ = [
		("ihl", 	c_ubyte, 4),
		("version", c_ubyte, 4),
		("tos",		c_ubyte, 8),
		("len",		c_ushort, 16),
		("id",		c_ushort, 16),
		("offset",	c_ushort, 16),
		("ttl",		c_ubyte, 8),
		("protocol_num", c_ubyte, 8),
		("checksum",	c_ushort, 16),
		("source",		c_uint, 32),
		("dest",		c_uint, 32)
		]

	def __new__(self, socket_buffer = None):
		return self.from_buffer_copy(socket_buffer)
		
	def __init__(self, socket_buffer = None):
	
		self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
	
		self.source_address = socket.inet_ntoa(struct.pack("<L",self.source))
		self.dest_address = socket.inet_ntoa(struct.pack("<L",self.dest))
			
		try:
			self.protocol = self.protocol_map[self.protocol_num]	
		except:
			self.protocol = str(self.protocol_num)
		

sniffer = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(ETH_P_ALL))
sniffer.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2**30)

sniffer.bind((host, ETH_P_ALL))

try:

	while True:
		
		data, source = sniffer.recvfrom(MTU)
		header = IP(data[14:34])
		
		print("Protocol %s %s ==> %s" %(header.protocol, header.source_address, header.dest_address))
except KeyboardInterrupt:
	print("Received interrupt, exiting")
	
	
						
		

