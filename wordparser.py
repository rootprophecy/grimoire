import sys

if len(sys.argv) != 2:
	print("Specify file to parse")
	exit(0)

filename = sys.argv[1]

w = open("wordlist.txt", "w")

for word in filename.split():
	w.write(word+"\n")

w.close
