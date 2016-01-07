#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# simple test of pyfirmata and Arduino; read from a sound detector on A0,

import time
import pyfirmata
import datetime
import csv
import os

def lg(arg1,arg2,arg3,arg4,arg5): #Function to Log Data
    label = ["Date","Tol Sensor 0","Tol Sensor 1","Tol Sensor 2 Tol","Tol Sensor 3 Tol","Tol Sensor 6"]
    print('Logged: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + str(float("{0:.4f}".format(arg2))) + "," + str(float("{0:.4f}".format(arg4))) + "," + str(float("{0:.4f}".format(arg5))))
    today = datetime.datetime.now().strftime("%Y-%m-%d") + "TolueneSensorData.csv"
    if os.path.isfile(today) == False:
	    with open(today, "a") as logfile:
		    wr = csv.writer(logfile)
		    wr.writerow(label)
    else:
        pass
    
    logfile = open(today, "a")
    logfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + str(arg1) + "," + str(arg2) + "," + str(arg3) + "," + str(arg4) + "," + str(arg5) + '\n')
    logfile.close()
# Create a new board, specifying serial port
board = pyfirmata.ArduinoMega('/dev/ttyACM1')

# start an iterator thread so that serial buffer doesn't overflow
it = pyfirmata.util.Iterator(board)
it.start()
#Survey 1000 samples 
survey = 2000
totalA0 = 0
totalA1 = 0
totalA2 = 0
totalA3 = 0
totalA4 = 0
# set up pins
pin0=board.get_pin('a:0:i')             # A0 Input Toluene Sensor 0    
pin1=board.get_pin('a:1:i')             # A1 Input Toluene Sensor 1
pin2=board.get_pin('a:2:i')             # A2 Input Toluene Sensor 2
pin3=board.get_pin('a:3:i')
pin4=board.get_pin('a:6:i')
# IMPORTANT! discard first reads until A1 gets something valid
while pin0.read() is None:
    print("None")
    board.pass_time(1)
    pass

while pin1.read() is None:
    print("None")
    board.pass_time(1)
    pass

while pin2.read() is None:
    print("None")
    board.pass_time(1)
    pass

while pin3.read() is None:
    print("None")
    board.pass_time(1)
    pass

while pin4.read() is None:
    print("None")
    board.pass_time(1)
    pass

while True:
    for i in range(survey): 
        totalA0 += pin0.read()
        board.pass_time(0.001)
        totalA1 += pin1.read()
        board.pass_time(0.001)
        totalA2 += pin2.read()
        board.pass_time(0.001)
        totalA3 += pin3.read()
        board.pass_time(0.001)
        totalA4 += pin4.read()
        board.pass_time(0.001)
    averageA0 = 5*totalA0 / survey
    averageA1 = 5*totalA1 / survey
    averageA2 = 5*totalA2 / survey
    averageA3 = 5*totalA3 / survey
    averageA4 = 5*totalA4 / survey    

#    print("TOLUENE SENSOR A0: FUNCTIONAL", float("{0:.3f}".format(averageA0)), "V")
#    print("TOLUENE SENSOR A1: FUNCTIONAL", float("{0:.3f}".format(averageA1)), "V")
#    print("TOLUENE SENSOR A2: FUNCTIONAL", float("{0:.3f}".format(averageA2)), "V") 
#    print("TOLUENE SENSOR A3: FUNCTIONAL", float("{0:.3f}".format(averageA3)), "V")
#    print("TOLUENE SENSOR A4: FUNCTIONAL", float("{0:.3f}".format(averageA4)), "V")

    totalA0 = 0
    totalA1 = 0
    totalA2 = 0
    totalA3 = 0
    totalA4 = 0
    lg(averageA0,averageA1,averageA2,averageA3,averageA4)
    board.pass_time(0.001)                  # pause 5 second
                         
board.exit()
