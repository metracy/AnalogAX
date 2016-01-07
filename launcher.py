#!/usr/bin/python
# -*- coding: utf-8 -*-
# Launcher program for scheduled delivery of toluene vapor.

import sys
import os
import csv
import subprocess as sp
import datetime
import time

print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' Startup Sequence initialized')
def lg(arg1): #Function to Log Data
    label = ["Date","SolenoidSequenceStatus"]
    cdate = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = '/home/inhalant/Desktop/python_scripts/'+cdate+'_SolenoidActivationSchedule.csv'
    if os.path.isfile(filename) == False:
	    with open(filename, "a") as logfile:
		    wr = csv.writer(logfile)
		    wr.writerow(label)
    else:
        pass
    
    logfile = open(filename, "a")
    logfile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "," + arg1 + '\n')
    logfile.close()

def get_sensors():
    cdate = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = '/home/inhalant/Desktop/python_scripts/'+cdate+'TolueneSensorData.csv'
    if os.path.exists(filename) == True:
        line = sp.check_output(["tail", "-1",filename])
        sv = line[:-1].split(",")
        return (sv[2],sv[4],sv[5])
    else:
        time.sleep(12)
        line = sp.check_output(["tail", "-1",filename])
        sv = line[:-1].split(",")
        return (sv[2],sv[4],sv[5])

def activatesolenoid():
    sp.Popen(["python","15mgas.py"], shell=False)

tl_1 = ['060000']
tl_3 = ['180000','000000','060000']
tl_6 = ['150000','180000','210000','000000','030000','060000']
tl_10 = ['140000','160000','180000','200000','220000','000000','020000','040000','060000']
tl_15 = ['140000','151600','163200','174800','190400','202000','213600','225200','000800','012400','024000','035600','051200','062800']

while True:
    current = datetime.datetime.now().strftime("%H%M%S")
    for ctime in tl_15:
        if int(current[0:4]) == int(ctime[0:4]):
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ': Solenoid Sequence Activated')
            lg('Initiated')
            activatesolenoid()
            time.sleep(65)
        elif (int(current) > (int(ctime))) and (int(current) < (int(ctime)+1400)):
            c1, c2, c6 = get_sensors()
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Sequence Still Open V1: " + str(c1) + " V2: " + str(c2) + " V6: " + str(c6))
        elif int(current) >= (int(ctime)+1400) and (int(current) < (int(ctime)+1500)):
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Terminating Exposure in ' + str(60-int(current[4:6])) + ' seconds.')
            lg('Terminating in '+ str(60-int(current[4:6])) + ' seconds.')
        else:
            pass
    time.sleep(5)
    
