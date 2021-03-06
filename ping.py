#!/usr/bin/env python

from socket import *
import os
import sys
import struct
import time
import select

ICMP_ECHO_REQUEST = 8

def checksum(str):
     csum = 0
     countTo = (len(str) / 2) * 2

     count = 0
     while count < countTo:
         thisVal = ord(str[count+1]) * 256 + ord(str[count])
         csum = csum + thisVal
         csum = csum & 0xffffffffL
         count = count + 2

     if countTo < len(str):
         csum = csum + ord(str[len(str) - 1])
         csum = csum & 0xffffffffL

     csum = (csum >> 16) + (csum & 0xffff)
     csum = csum + (csum >> 16)
     answer = ~csum
     answer = answer & 0xffff
     answer = answer >> 8 | (answer << 8 & 0xff00)
     return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
     timeLeft = timeout
     while 1:
         startedSelect = time.time()
         whatReady = select.select([mySocket], [], [], timeLeft)
         howLongInSelect = (time.time() - startedSelect)

         if whatReady[0] == []: # Timeout
             return "Request timed out."

         timeReceived = time.time()
         recPacket, addr = mySocket.recvfrom(1024)

         #TODO: Fetch the ICMP header from the IP packet
         print 'received packet:\n', recPacket

         timeLeft = timeLeft - howLongInSelect
         if timeLeft <= 0:
             return "Request timed out."


def sendOnePing(mySocket, destAddr, ID):
     # Header is type (8), code (8), checksum (16), id (16), sequence (16)

     myChecksum = 0
     # Make a dummy header with a 0 checksum.
     # struct -- Interpret strings as packed binary data
     header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
     data = struct.pack("d", time.time())
     # Calculate the checksum on the data and the dummy header.
     myChecksum = checksum(header + data)

     # Get the right checksum, and put in the header
     if sys.platform == 'darwin':
         myChecksum = htons(myChecksum) & 0xffff
         #Convert 16-bit integers from host to network byte order.
     else:
         myChecksum = htons(myChecksum)

     header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
     packet = header + data

     print 'Sent packet:\n', packet

     mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
     #Both LISTS and TUPLES consist of a number of objects
     # #which can be referenced by their position number within the object


def doOnePing(destAddr, timeout):
     icmp = getprotobyname("icmp")
     mySocket = socket(AF_INET, SOCK_RAW, icmp)

     print 'dest addr', destAddr

     myID = os.getpid() & 0xFFFF #Return the current process i
     sendOnePing(mySocket, destAddr, myID)
     delay = receiveOnePing(mySocket, myID, timeout, destAddr)

     mySocket.close()
     return delay


def ping(host, timeout=1):
     dest = gethostbyname(host)
     print "Pinging " + dest + " using Python:"
     print ""
     delay = 0

     #Send ping requests to a server separated by approximately one second
     for i in range(0, 10):
         delay = doOnePing(dest, timeout)
         print delay
         time.sleep(.5)# one second


     return delay


print 'Ensure you run this as root'
ping("www.google.com")