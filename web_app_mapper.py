import threading
import os
import queue
import urllib.request
import sys

if len(sys.argv) != 2:
	print("Usage: python(3) %s <web_app url>" %(sys.argv[0]))
	sys.exit(0)

to_map = sys.argv[1]

threads = 10

web_paths = queue.Queue()
for r,d,f in os.walk('.'):
	for file in f:
		remote_path = "%s/%s" %(r, file)
		if remote_path.startswith("."):
			remote_path = remote_path[1:]
		web_paths.put(remote_path)


def test_remote():
	
	while not(web_paths.empty()):
		target_url = "%s%s" %(to_map,web_paths.get())
		try:
			request = urllib.request.Request(target_url)
			response = urllib.request.urlopen(request)
			print("[%d]==> %s" %(response.code, target_url))
		except urllib.error.URLError as error:
			pass

for i in range(threads):
	t = threading.Thread(target=test_remote)
	t.start()
