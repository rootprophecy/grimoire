import sys
import threading
import socket

def response_handler(response):
	try:
		f = open('response_dump.txt', 'a')
		f.write(response.decode("utf-8", "replace")+'\n')
		f.close()
	except:
		pass
	return response

def request_handler(request):
	try:
		f = open('request_dump.txt', 'a')
		f.write(request.decode("utf-8", "replace")+'\n')
		f.close()
	except:
		pass
	return request

def hexdump( src, length=16, sep='.' ):
	result = [];

	# Python3 support
	try:
		xrange(0,1);
	except NameError:
		xrange = range;

	for i in xrange(0, len(src), length):
		subSrc = src[i:i+length];
		hexa = '';
		isMiddle = False;
		for h in xrange(0,len(subSrc)):
			if h == length/2:
				hexa += ' ';
			h = subSrc[h];
			if not isinstance(h, int):
				h = ord(h);
			h = hex(h).replace('0x','');
			if len(h) == 1:
				h = '0'+h;
			hexa += h+' ';
		hexa = hexa.strip(' ');
		text = '';
		for c in subSrc:
			if not isinstance(c, int):
				c = ord(c);
			if 0x20 <= c < 0x7F:
				text += chr(c);
			else:
				text += sep;
		result.append(('%08X:  %-'+str(length*(2+1)+1)+'s  |%s|') % (i, hexa, text));

	print('\n'.join(result));

def receive_from(connection):
	
	print('Reading data...')
	connection.settimeout(2)
	
	buffer = b""
	try:
		while True:
			data = connection.recv(4096)
			buffer += data
	except:
		pass
	return buffer
	

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
	
	print('[+]Started proxy handler')
	remote_socket = socket.socket()
	try:
		remote_socket.connect((remote_host, int(remote_port)))
		print('[+]Connected to remote host')
	except Exception as e:
		print(e)
		exit(0)
	if receive_first:
		
		remote_buffer = receive_from(remote_socket)
		remote_buffer = response_handler(remote_buffer)
		print(remote_buffer)

		if len(remote_buffer):
			print('Sending %d bytes to client' %(len(remote_buffer)))
			client_socket.send(remote_buffer)

	while True:
		
		local_buffer = receive_from(client_socket)
			
		if local_buffer:
			print('======>Received %d bytes from client=======>' %(len(local_buffer)))
			local_buffer = request_handler(local_buffer)
			hexdump(local_buffer)

			remote_socket.send(local_buffer)
	
		remote_buffer = receive_from(remote_socket)
	

		if remote_buffer:
			print('<======Sending %d bytes to client<=====' %(len(remote_buffer)))
			remote_buffer = response_handler(remote_buffer)
				
			client_socket.send(remote_buffer)

		if not local_buffer and not remote_buffer:
			client_socket.close()
			remote_socket.close()
			print('Nothing left to do, closing connections.')
			exit()


				
		
		

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
	
	server = socket.socket()

	try:
		server.bind((local_host, int(local_port)))
		print('[+]TCP Proxy running')
	except:
		print('Could not bind socket to given host and port')
		exit(0)

	server.listen(5)

	while True:
		
		client_socket, addr = server.accept()

		print('======>Received connection from %s:%d' %(addr[0],addr[1]))
		
		proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket,remote_host, remote_port, receive_first))	
		
		proxy_thread.start()
def main():
	
	if(len(sys.argv) != 6):

		print('usage: python %s [localhost] [localport] [remotehost] [remoteport] [receivefirst]')
		print('example: python proxy_tcp.py 127.0.0.1 9999 192.168.1.9 1234 True')
		exit(0)

	if sys.argv[5] == 'True':
		receive_first = True
	else:
		receive_first = False

	local_host = sys.argv[1]
	local_port = sys.argv[2]
	remote_host = sys.argv[3]
	remote_port = sys.argv[4]

	server_loop(local_host, local_port, remote_host, remote_port, receive_first)


if __name__ == '__main__':
	main()
