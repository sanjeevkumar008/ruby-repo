#!/bin/env python
#!/usr/bin/python
#
##### Moudle used ##########
import getopt
import glob
import os
import re
import shutil
import subprocess
import sys
import time
import socket
from shutil import copyfile
try:
   import json
except:
   import simplejson as json
from smtplib import SMTP
##############################
##############   Colors defination  #############
CEND      = '\33[0m'
CBOLD     = '\33[1m'
CITALIC   = '\33[3m'
CURL      = '\33[4m'
CBLINK    = '\33[5m'
CBLINK2   = '\33[6m'
CSELECTED = '\33[7m'

CBLACK  = '\33[30m'
CRED    = '\33[31m'
CGREEN  = '\33[32m'
CYELLOW = '\33[33m'
CBLUE   = '\33[34m'
CVIOLET = '\33[35m'
CBEIGE  = '\33[36m'
CWHITE  = '\33[37m'

####################################################

def check_output(cmd):
    proc_list = []
    cmd_list = cmd.strip().split("|")
    for i, sub_cmd in enumerate(cmd_list):
        cmd_list = sub_cmd.strip().split(" ")
        STDIN = None
        if i > 0:
            STDIN = proc_list[i - 1].stdout
        proc_list.append(subprocess.Popen(cmd_list, stdin=STDIN, stdout=subprocess.PIPE))
    if len(proc_list) == 0:
        return ''
    output = proc_list[i].communicate()[0]
    return output

#####################################################

def command(cmd):
   p = subprocess.Popen(cmd.split(),stdout=subprocess.PIPE)
   (out,err) = p.communicate()
   value = p.wait()
   if (value == 0):
      return out.strip().split('\n')
   else:
      return None

########################################################
def free_cpus():
    global free_cpu
    total_cpu = check_output('xm info | grep nr_cpus | cut -d: -f2')
    free_cpu = 0
    xm_list = command('xm list')
    used_cpu = 0
    for line in xm_list:
      if (line == ''):
         continue
      (name,id,mem,vcpus,state,times) = line.split()
      if (name == 'Name'):
         continue
      if (name == 'Domain-0'):
         continue
      used_cpu = used_cpu + int(vcpus)
    free_cpu = int(total_cpu) - int(used_cpu)
    #print "Free_CPU = ", free_cpu

########################################################
free_cpus()

hostName = socket.gethostname()

if os.path.exists(hostName):
   os.remove(hostName)

file = open(hostName,'a+')
file.write('\n')
print >> file, "Hostname :" + hostName
file.write('\n')
print >> file, "Pool :" + check_output('df -kP -t nfs | grep _con | grep -v swap').split()[0].split('/')[2]
file.write('\n')
print >> file, "Model_Name : " + check_output('dmidecode | grep -i prod | head -1 | cut -d: -f2')
print >> file, "Serial_Number : " + check_output('dmidecode | grep -i number | head -1 | cut -d: -f2')
print >> file, "Total_CPU : " + check_output('xm info | grep nr_cpus | cut -d: -f2')
print >> file, "Free_CPU : ", free_cpu
file.write('\n')
print >> file, "Total_Memory : " + check_output('xm info | grep total_memory | cut -d: -f2')
print >> file, "Free_Memory : " + check_output('xm info | grep free_memory | cut -d: -f2')

##########################################################
file.write('\n')
file.close()
#file = open(hostName,'r')
#print file.read()
file.close()
#os.rename("info.txt", hostName)
path = "/mig-os/info/"
copyfile(hostName, path + hostName)    

[root@rmc002oodhost702 kuksanje]#                 