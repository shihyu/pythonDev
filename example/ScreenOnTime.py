#! /usr/bin/python2.7
import sys
import re
import os
from datetime import *

stack = []

def push(data):
    stack.append(data)

def pop():
    if len(stack) == 0:
        print 'Cannot pop from an empty stack!'
    else:
        return stack.pop()

def LogPaser():
    fin = open('/tmp/a.txt')
    line = fin.readline()

    while line:
        m = re.match(r'(\d+\-\d+ \d+:\d+\:\d+\.\d+).*\s\w+=(\d+)',line)
        if m:
            #print m.group(0)
            #print m.group(1)
            #print m.group(2)
            push(m.group(1))

        m = re.match(r'(\d+\-\d+ \d+:\d+\:\d+\.\d+).*\s\w+\s\w+\s\w+:\s(\d+)',line)
        if m:
            #print type(int(m.group(2)))
            if int(m.group(2)) > 0 and len(stack) > 0:
                fm = '%m-%d %H:%M:%S.%f'
                d1 = datetime.strptime(str(pop()), fm)
                d2 = datetime.strptime(str(m.group(1)), fm)

                #print m.group(0)
                #print m.group(1)
                #print m.group(2)
                t = d2 - d1
                #print t

                time_day = t.days  
                s_time = t.seconds  
                ms_time = t.microseconds / 1000000 
                usedtime = int(s_time + ms_time)  
                time_hour = usedtime / 60 / 60 
                time_minute = (usedtime - time_hour * 3600 ) / 60 
                time_second =  usedtime - time_hour * 3600 - time_minute * 60 
                time_micsecond = (t.microseconds - t.microseconds / 1000000) / 1000 
                retstr = "%d day %d hours %d minutes %d seconds %d millisecondsds"  %(time_day, time_hour, time_minute, time_second, time_micsecond)  
                print retstr

                del stack[0:len(stack)]

        line = fin.readline()

if __name__ == '__main__':
    command = "grep -E 'keycode=26|Set LcdLight brightness:' " +  str(sys.argv[1]) + "| grep -v 'down:False' > /tmp/a.txt"
    #print command
    os.system(command) 
    LogPaser()
