#!/usr/bin/python3
import _thread
import time
import sys
import socket
from copy import deepcopy
import json
import time
neighbours = {}
seq = 0
currentSeq=0

graph = {}

class bootstrap: 
    def __init__(self):
        #check no of arguments for validity
        if(len(sys.argv)<4):
            print("invalid No. of arguments")
            sys.exit()
        try:
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
            graph[sys.argv[1]] = neighbours
        except:
            print("Invalid file name:")
            print("config/"+str(sys.argv[3]))
            sys.exit()

object = bootstrap()


def sendLinkState(MESSAGE,UDP_IP,UDP_PORT):
    # MESSAGE = json.dumps(MESSAGE)
    # MESSAGE = MESSAGE.encode('utf-8')
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
#ending function here


def receiveLinkState():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', int(sys.argv[2]))
    server.bind(server_address)
    currentSeq={}
    while True:
        print('\nwaiting to receive message')
        data, address = server.recvfrom(4096)
        data = data.decode('utf-8')
        data = json.loads(data)
        origin = data['key']
        receivedFrom = data['sender']
        
        if(origin not in currentSeq or data['seq']>currentSeq[origin]['seq']):
            # print(data['seq'],data['key'])
            currentSeq[origin] = {}
            currentSeq[origin]['seq'] = data['seq']
            # currentSeq[origin]['key'] = data['key']

            print(receivedFrom,origin,data['seq'])
            data['sender']=sys.argv[1]
            graph[origin] = data['neighbours']
            data = json.dumps(data)
            data = data.encode('utf-8')
            for neighbour in neighbours.keys():
                if receivedFrom!=neighbour and neighbour!=origin:
                    sendLinkState(data, 'localhost', neighbours[neighbour]['port'])
        #time.sleep(5)
#ending function

def Dijkstra():
    time.sleep(10)
    currentNeighbours={}
    stack = []
    bestCost = {sys.argv[1]:{'cost':0,'path':sys.argv[1]}}
    stack.append(sys.argv[1])

    while len(stack)>0:
        currentNode = stack[-1]
        stack.pop()
        currentNeighbours = graph[currentNode]
        for key,value in currentNeighbours.items():
            if key not in bestCost:
                bestCost[key]={}
                bestCost[key]['cost'] = 999999
                bestCost[key]['path'] = ""
            if key in graph and bestCost[key]['cost']>bestCost[currentNode]['cost']+value['cost']:
                bestCost[key]['cost'] = bestCost[currentNode]['cost']+value['cost']
                bestCost[key]['path'] = bestCost[currentNode]['path']+key
                stack.append(key)
                print(key)

    print(bestCost)


def initiator():
    seq = 0
    while True:
        UDP_IP = 'localhost'
        MESSAGE = deepcopy(neighbours)
        seq+=1
        MESSAGE = {'sender':sys.argv[1],'seq':seq,'key':sys.argv[1],'neighbours':MESSAGE}
        MESSAGE = json.dumps(MESSAGE)
        MESSAGE = MESSAGE.encode('utf-8')
        for neighbour in neighbours.values():
            UDP_PORT = neighbour['port']
            sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
        time.sleep(5)
        #print(graph)
        
#ending function


# print('Argument List:', str(sys.argv))

# Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# # Create two threads as follows
try:
    _thread.start_new_thread( receiveLinkState, () )
    _thread.start_new_thread( initiator, () )
    _thread.start_new_thread( Dijkstra, () )
except:
   print ("Error: unable to start thread")

while 1:
   pass

initiator()