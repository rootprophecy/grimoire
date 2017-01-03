import argparse
import sys
import socket
import threading

def client_sender(buffer):
	client = socket.socket()

	try:
		client.connect((target, port))
		if len(buffer):
			client.send(buffer.encode())
		while True:
			print("ENTERING NEW INPUT")
			resp = client.recv(4096)
			buffer = input()
			client.send(buffer.encode())			
	except Exception as e:
		print(e)
		exit(0)

def server_loop():
		

def main():
	parser = argparse.ArgumentParser(description='Netcat-like client-server utility process featuring Python3!')

	parser.add_argument(dest='target',default=None,help='host to connect with')
	parser.add_argument(dest='port',default=None,help='port to connect to')
	parser.add_argument('-l','--listen',dest='listen',action='store_true', help='listen mode')
	parser.add_argument('-e','--execute',dest='execute',action='store', help='given file to execute')
	parser.add_argument('-c','--command',dest='command',action='store_true',help='command shell')
	parser.add_argument('-u','--upload',dest='upload',action='store',help='upload data to given file upon receiving a connection')

	args = parser.parse_args()
	print(args)

	global target 
	target = args.target
	global port  
	port = int(args.port)

	if not args.listen:
		buffer = sys.stdin.read()
		client_sender(buffer)
	
	else
		server_loop()

if __name__ == '__main__':
	main()
