#!/usr/bin/python3
import _thread
import time
import sys
import socket
import json
import time
from copy import deepcopy


neighbours = {}
costTree = {
                'A':{
                    'cost':100000000,
                    'path':""
                },
                'B':{
                    'cost':100000000,
                    'path':""
                },
                'C':{
                    'cost':100000000,
                    'path':""
                },
                'D':{
                    'cost':100000000,
                    'path':""
                },
                'E':{
                    'cost':100000000,
                    'path':""
                },
                'F':{
                    'cost':100000000,
                    'path':""
                }
}
class bootstrap: 
    def __init__(self):
        #check no of arguments for validity
        if(len(sys.argv)<4):
            print("invalid No. of arguments")
            sys.exit()
        try:
            print("total")
            config = open("config/"+str(sys.argv[3]),'r')
            total = config.readline()
            total = int(total)
            for i in range(0,total):
                row = config.readline()
                row = row.split(" ")
                ID = row[0]
                cost = float(row[1])
                port = int(row[2])
                neighbours[ID] = {"cost":cost,"port":port}
                costTree[ID] = {"cost":cost,"path":sys.argv[1]+ID}
                # costTree[ID]['cost'] = cost
                # costTree[ID]['path'] = sys.argv[1]+ID
        except:
            print("Invalid file name:")
            print("config/"+str(sys.argv[3]))
            sys.exit()



object = bootstrap()



print(neighbours)
def sendLink():
    while(True):
        for neighbour in neighbours:
            UDP_IP = "127.0.0.1"
            UDP_PORT = neighbours[neighbour]["port"]
            MESSAGE = deepcopy(costTree)
            for key in MESSAGE.keys():
                MESSAGE[key]['cost'] += neighbours[neighbour]["cost"]
            MESSAGE = json.dumps(MESSAGE)
            MESSAGE = MESSAGE.encode('utf-8')
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        time.sleep(5)
# sendLink()


def receiveLink():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', int(sys.argv[2]))
    server.bind(server_address)
    while True:
        print('\nwaiting to receive message')
        data, address = server.recvfrom(4096)
        data = data.decode('utf-8')
        data = json.loads(data)
        for key,value in data.items():
            if costTree[key]['cost']>(data[key]['cost']) and key!=sys.argv[1]:
                costTree[key]['cost'] = data[key]['cost']
                costTree[key]['path'] = sys.argv[1]+data[key]['path']
        print(costTree)

# receiveLink()
# print('Argument List:', str(sys.argv))

# Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# Create two threads as follows
try:
    _thread.start_new_thread( sendLink,())
    _thread.start_new_thread( receiveLink,())
except:
   print ("Error: unable to start thread")

while 1:
   pass