# Editing from Automate the Boring Stuff with Python <- Al Sweigart is awesome.

import subprocess as sp
from Tkinter import *
import time
import datetime
import os
#ct = datetime.datetime.now().strftime("%H%M%S")

def get_sensors():
    cdate = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = '/home/inhalant/Desktop/python_scripts/'+cdate+'TolueneSensorData.csv'
    if os.path.exists(filename) == True:
        line = sp.check_output(["tail", "-1",filename])
        sv = line[:-1].split(",")
        return (sv[0], sv[2], sv[4],sv[5])
    else:
        time.sleep(12)
        line = sp.check_output(["tail", "-1",filename])
        sv = line[:-1].split(",")
        return (sv[0], sv[2], sv[4],sv[5])

class App:
	
    def __init__(self, master):
        self.master = master
        frame = Frame(master)
        frame.pack()
        label1 = Label(frame, text='Chamber 1  ', font=("Arial", 16))
        label1.grid(row=1,column=0)
        label2 = Label(frame, text='Chamber 3  ', font=("Arial", 16))
        label2.grid(row=1,column=1)
        label3 = Label(frame, text='Chamber 6', font=("Arial", 16))
        label3.grid(row=1,column=2)
        self.date_label = Label(frame, text='Date', font=("Arial", 16))        
        self.reading_label = Label(frame, text='1', font=("Arial", 16))
        self.reading_label2 = Label(frame, text='2', font=("Arial", 16))
        self.reading_label3 = Label(frame, text='3', font=("Arial", 16))

        self.date_label.grid(row=0,column=1)
        self.reading_label.grid(row=2,column=0)
        self.reading_label2.grid(row=2,column=1)
        self.reading_label3.grid(row=2,column=2)
        self.update_reading()

    def update_reading(self):
        try:
            date, sv1, sv3, sv6 = get_sensors()
            date_str = date
            reading_str = "{:.6f}".format(float(sv1))
            reading_str1 = "{:.6f}".format(float(sv3))
            reading_str2 = "{:.6f}".format(float(sv6))
            self.date_label.configure(text=date_str)
            self.reading_label.configure(text=reading_str)
            self.reading_label2.configure(text=reading_str1)
            self.reading_label3.configure(text=reading_str2)
            self.master.after(1000, self.update_reading)
        except:
            time.sleep(10)



root = Tk()
root.wm_title('Toluene Analog Sensors')
app = App(root)
root.geometry("500x85+0+0")
root.mainloop()

