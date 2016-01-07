#!/usr/bin/python
import pyfirmata
import time
import math
import datetime

board = pyfirmata.ArduinoMega('/dev/ttyACM0')

it = pyfirmata.util.Iterator(board)
it.start()

b=2*math.pi
threshold=0
p=-0.454833


start = time.time()
end = time.time()
elapsed = end - start


def startt():
    global start
    start = time.time()
   
def myround(z, threshold=0.48):
    z = math.sin(((2*math.pi)*((float(z)/30))-(-1.73949624846459*math.pi)))/2+.5
    if z >= threshold:
        return 1.0
    else:
        return 0.0

def chktime():
    global start
    global end
    global elapsed
    end = time.time()
    elapsed = end - start
    return elapsed

pin22 = board.get_pin('d:22:o')
pin22.write(0)
startt()
chktime()
try:
    while chktime() <= 900.0:
        if elapsed <= 120.0:
            pin22.write(1)
        elif myround(chktime()) >= 1.0:
            print 'Solenoid Activated'
            pin22.write(1)
        else:
            print 'Solenoid Deactivated'
            pin22.write(0)
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' Time Elapsed: ' + '%8.2f' % (elapsed))
        time.sleep(.2)
except:
    pin22.write(0)
print('Sequence Finished at ' + '%8.0f' % (elapsed))
pin22.write(0)
board.exit()
