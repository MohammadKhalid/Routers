#!/usr/bin/python3
import _thread
import time
import sys


neighbours = {}

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
        except:
            print("Invalid file name:")
            print("config/"+str(sys.argv[3]))
            sys.exit()

object = bootstrap()
print(neighbours)
def sendLink():
    for()
# print('Argument List:', str(sys.argv))

# Define a function for the thread
# def print_time( threadName, delay):
#    count = 0
#    while count < 5:
#       time.sleep(delay)
#       count += 1
#       print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# # Create two threads as follows
# try:
#     _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
#     _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
# except:
#    print ("Error: unable to start thread")

# while 1:
#    pass