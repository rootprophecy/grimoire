import paramiko
import threading
import sys
import socket
	
	
class Server(paramiko.ServerInterface):
	
	def init(self):
		self.event = threading.Event()
	def check_channel_request(self, kind, chanid):
		if kind == 'session':
			return paramiko.OPEN_SUCCEEDED
		return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

	def check_auth_password(self, username, password):
		if(username == 'justin' and password == 'lovesthepython'):
			return paramiko.AUTH_SUCCESSFUL
		return paramiko.AUTH_FAILED
	
def main():	
	
	host_key = paramiko.RSAKey(filename='test_rsa.key')
	if len(sys.argv) != 3:
		print('Usage: sshserver.py <host> <port>')
		sys.exit(0)	
		
	ssh_host = sys.argv[1]
	ssh_port = int(sys.argv[2])
	
	try:
		sock = socket.socket()
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
		sock.bind((ssh_host, ssh_port))
		sock.listen(100)
		print('[+]Server started..')
		
		client, addr = sock.accept()
	except Exception as e:
		print('Listen failed: %s' %(e))
		sys.exit(0)
		
	print('Got a connection from %s:%d' %(addr[0],addr[1]))
	
	try:
		t = paramiko.Transport(client)
		t.add_server_key(host_key)
		server = Server()
		try:
			t.start_server(server=server)
		except Exception as e:
			print('SSH Negotiation failed: %s' %(e))
			sys.exit(0)
		
		chan = t.accept(20)
		if not chan:
			print('Auth failed!')
			sys.exit(0)
		
		print(chan.recv(1024).decode())
		chan.send('Welcome to bh_ssh!')
		while True:
			try:
				command = input('Enter Command: \n').strip('\n')
				if command != 'exit':
					chan.send(command)
					print(chan.recv(1024).decode() + '\n')
				
				else:
					chan.send('exit')
					print('Exiting')
					t.close()
					raise Exception ('exit')
			except KeyboardInterrupt:
				t.close()
	except Exception as e:
		print('[-]Caught exception: %s' %(e))
		try:
			t.close()
		except:
			pass
		sys.exit(1)	
		
						
				
if __name__ == '__main__':
	main()
