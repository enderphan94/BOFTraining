#!/usr/bin/env python

import sys
import socket
import time

def generate_pattern(size):
	string =""
	for i in range(ord('A'), ord('Z') +1):
		for j in range(ord('a'), ord('z')+1):
			for k in range(10):
				string += chr(i) + chr(j) +str(k)
	return string[:size]
				
def usage():
	print " Usage: fuzz.py [ip_addr] [port] ip_addr: IP Address of the Server port: Port of the Server"
	sys.exit(1)

if len(sys.argv) <> 3:
	usage()

host = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.settimeout(2.0)

maxchar = raw_input("how many butes do you want to send (End with 0):")
maxchar = int(maxchar)

while maxchar != 0:
	s.send(generate_pattern(maxchar))
	try:
		data = s.recv(1024)
		print "data returned:%s" %data
	except socket.error as e:
		print "\n#################################################################################"
		print "There is no response from the server maybe crashed with a string length of %d" %maxchar
		print "#################################################################################"
		break
	maxchar = raw_input("how many butes do you want to send (End with 0):")
	maxchar = int(maxchar)
		
s.close()

