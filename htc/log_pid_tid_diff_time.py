#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
from datetime import *

#use
#python log_pid_tid_diff_time.py device_i0002_20130928_145715_FA36WPN00121_dlpdtu_0.1.0.0.txt 2 
# 2s , defalut 1s 

D = {}
'''
def myprint(obj, end='\n'):
    sys.stdout.write(str(obj) + end)
'''

def get_nodes(inputline, sec):

    p = re.compile("(\d+\-\d+ \d+:\d+\:\d+\.\d+)(\s+\d+\s+\d+)")
    
    for l in inputline:    
        l = l.strip()
        #print l
        n = p.findall(l)[0]
        #print n
        #print n[1]
        #print n[0]
        #print n[1]
        #print n[2]

        if D.has_key(n[1]):
            #print l
            #print D.get(n[1], 0) 
            #print n[0]

            fm = '%m-%d %H:%M:%S.%f'
            d1 = datetime.strptime(str(D.get(n[1], 0)), fm)
            d2 = datetime.strptime(str(n[0]), fm)
            t = d2 - d1

            if t.seconds > sec:
                print "[+]"
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

                #myprint('%ds:%d' % (t.seconds, t.microseconds / 1000))
                #print t
                print l
                print "[-]"
                print ""
                #raw_input("raw_input: ")

            D[n[1]] = n[0]

            #print t
            #print D.items()
            #raw_input("raw_input: ")
        else: 
            D[n[1]] = n[0]

    #print D.items() 

if __name__ == "__main__":

    fin = open(sys.argv[1])

    if len(sys.argv) > 2:
        get_nodes(fin, int(sys.argv[2]))
    else:
        get_nodes(fin, 1)

