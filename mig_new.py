[root@rmc002oodhost701 kuksanje]# more migration.py
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
def usage():
   print "\nUsage:\n" + sc_name + " --vmname <VM_NAME> --domzname <SRC_DOM0> --trgtdomz <DST_DOM0>\n"
   sys.exit()

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
def vm_find():
   global vm_list, vm_memory, vm_cpu, vm_FE, vm_BE, vm_UUID, VM_Data, used_cpu, used_memory
   xm_list = command('xm list')
   VM_Data = {}
   vm_list = []
   vm_memory = []
   vm_cpu = []
   vm_FE = []
   vm_BE = []
   vm_UUID = []
   #key = command('xm list | grep -v Name | wc -l')
   keys = range(6)
   values = ""
   cfgs = []
   data = {}
   for line in xm_list:
      if (line == ''):
         continue
      (name,id,mem,vcpus,state,times) = line.split()
      if (name == 'Name'):
         continue
      if (name == 'Domain-0'):
         continue
      cfg_paths = glob.glob('/OVS/Repositories/*/*/' + name + '/vm.cfg')
      for cfg_path in cfg_paths:
         data = open(cfg_path)
         for line in data:
            if re.match('^OVM_simple_name',line):
               ovm_vm_name = line.split('=')[1].strip().split("'")[1]
               vm_list.append(ovm_vm_name)
            if re.match('^memory',line):
               vm_m = line.split('=')[1].strip()
               vm_memory.append(vm_m)
            if re.match('^vcpus',line):
               vm_c = line.split('=')[1].strip()
               vm_cpu.append(vm_c)
            if re.match('^vif ', line):
               FE_bridge = line.split("=")[5].split("_")[0].strip()
               vm_FE.append(FE_bridge)
               BE_bridge = line.split("=")[3].split("_")[0].strip()
               vm_BE.append(BE_bridge)
            if re.match('^name ', line):
               uuid = line.split('=')[1].strip().split("'")[1]
               vm_UUID.append(uuid)

   vm_list = tuple(vm_list)
   vm_memory = list(vm_memory)
   vm_cpu = list(vm_cpu)
   vm_cpu1 = list(vm_cpu)
   vm_FE = tuple(vm_FE)
   vm_BE = tuple(vm_BE)
   vm_UUID = tuple(vm_UUID)
   #vm_list = tuple(vm_list)
   #print (vm_list)
   #print (vm_memory)
   #print (vm_cpu)
   total_cpu = int(check_output('xm info | grep nr_cpus | cut -d: -f2'))
   used_cpu = sum(map(int, vm_cpu1))
   used_memory = sum(map(int, vm_memory))

   print "Total CPU : ",  total_cpu
   print "Used CPU : ",  used_cpu
   free_cpu = total_cpu - used_cpu

   print "Free CPU : ",  free_cpu
   print "Used Memory : ", used_memory

#######################################################

def listBridges():
   bridges = []
   for i,line in enumerate(command('brctl show')):
      if (re.match('^$',line)):
         continue
      if (re.match('^\s',line)):
         continue
      if (i == 0):
         continue
      bridges.append(line.split()[0])
   return bridges

#######################################################
def vm_dict():
   global vm
   vm = {}
   VM_Data = {}
   z = 0
   while z < len(vm_list):
      # print mytuple[z]
       vm = vm_list[z]
       #cpu = vm_cpu[z]
       #memory = vm_memory[z]

       VM_Data[vm] = {}
       #VM_Data[vm]['vm_name'] = vm
       VM_Data[vm]['UUID'] = vm_UUID[z]
       VM_Data[vm]['CPU'] = vm_cpu[z]
       VM_Data[vm]['Memory'] = vm_memory[z]
       VM_Data[vm]['FE Bridge'] = vm_FE[z]
       VM_Data[vm]['BE Bridge'] = vm_BE[z]

       z += 1
   values = [{"VM_Name": k, "VM_information": v} for k, v in VM_Data.items()]
   #values = [{k : v} for k, v in VM_Data.items()]
   print json.dumps(values, indent=4)

   print CGREEN + "VM searching....." + CEND

   #VM = "vmohsrigs081"
   for key, value in VM_Data.items():
      #if (key == argVmName):
      while (key == argVmName):
          print("VM is Found", key)
          print json.dumps(value, indent=4)
          break
      #else:
      print("VM is not Found")

########################################################
def source_dom0():
    global dom0_model, dom0_cpu, dom0_memory
    print argDomzName + " is Source Dom0"
    Dom0_Data = {}
    dom0 = argDomzName
    dom0_model = check_output('dmidecode | grep -i prod | head -1 | cut -d: -f2')
    dom0_cpu = 0
    dom0_memory = check_output('xm info | grep free_memory | cut -d: -f2')
    dom0_bridge = 0

    Dom0_Data[dom0] = {}
    Dom0_Data[dom0]['dom0_name'] = argDomzName
    Dom0_Data[dom0]['Model'] = dom0_model
    Dom0_Data[dom0]['Free_CPU'] = dom0_cpu
    Dom0_Data[dom0]['Memory'] = dom0_memory
    Dom0_Data[dom0]['Bridge'] = dom0_bridge
    print Dom0_Data
    values = [{"Dom0_Name": p, "Dom0_information": q} for p, q in Dom0_Data.items()]
    print json.dumps(values, indent=4)

########################################################
def target_dom0():
    print "Target", argTrgtName

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
def dom0_data():
    dom0_list = check_output("ls /mig-os/info ")
    print "No. of Dom-0 avaialble in this Pool :"
    print dom0_list

#######################################################
def comparison():
    dom0_list = check_output("ls /mig-os/info ")
    i = 0


###############    MAIN    #############################
#dom0_data()

#VM_NAME = "TEST_VM"
SRC_DOM0 = socket.gethostname()
COPY_SERVER = "TEST_COPY_SERVER"
#DST_DOM0 = "TEST_DST_DOM0"

global argVmNamee
global argDomzName
global argTrgtName

sc_name = os.path.basename(sys.argv[0]).replace('.py','')

arg_count = 0
opts, args = getopt.getopt(sys.argv[1:], 'v:d:t:h', ['vmname=','domzname=','trgtdomz=','copyserv=','help'])
for (opt, val) in opts:
   if opt in ['-v', '--vmname']:
      argVmName = val
      arg_count = arg_count + 1
   if opt in ['-d', '--domzname']:
      argDomzName = val
      arg_count = arg_count + 1
   if opt in ['-t', '--trgtdomz']:
      argTrgtName = val
      arg_count = arg_count + 1
   if opt in ['-h', '--help']:
      usage()

if (arg_count != 3):
   usage()

########################################################
free_cpus()
hostName = socket.gethostname()
hostFqdn = socket.getfqdn()
smtpHost = 'internal-mail-router.oracle.com'
today = time.strftime("%Y%m%d")
logDir = '/var/log/mig3.2'
print "===================================================="
print
print CGREEN + "      Dom0 Information" + CEND
print "===================================================="
print
print "Hostname :" + hostName
print
print
print "Pool :" + check_output('df -kP -t nfs | grep _con | grep -v swap').split()[0].split('/')[2]
print
print "Model Name : " + check_output('dmidecode | grep -i prod | head -1 | cut -d: -f2')
print "Serial Number : " + check_output('dmidecode | grep -i number | head -1 | cut -d: -f2')
print "Total No. of CPU : " + check_output('xm info | grep nr_cpus | cut -d: -f2')
#print "Used CPU : ", used_cpu
print "Free CPU : ", free_cpu
#print "Free CPU : " + check_output('xm info | grep free_cpus | cut -d: -f2')
print "Total Memory : " + check_output('xm info | grep total_memory | cut -d: -f2')
print "Free memory : " + check_output('xm info | grep free_memory | cut -d: -f2')
#print "Used CPU : ", check_output("""xm list | egrep -v "Name|Domain-0" | awk {'print $4'} | awk '{ sum += $1 } END { print sum }'""")


print "===================================================="

###############################
sc_name = os.path.basename(sys.argv[0]).replace('.py','')

###############################

###############################
print
print "===================================================="
print
print CGREEN + "      List of VM Running" + CEND
print "===================================================="
print

vm_find()
vm_dict()
#vm_search()

source_dom0
target_dom0

print "############################################"
dom0_model = check_output('dmidecode | grep -i prod | head -1 | cut -d: -f2').strip()
dom0_pool = check_output('df -kP -t nfs | grep _con | grep -v swap').split()[0].split('/')[2]
dom0_list = os.listdir("/mig-os/info")
cpu = 8
memory = 132001
#dom0_memory = check_output('xm info | grep free_memory | cut -d: -f2')
print "No. of Dom-0 avaialble in this Pool :"
print dom0_list
i = 0
mig_path = "/mig-os/info/"
os.chdir(mig_path)
while i < len(dom0_list):
#    if (hostName == dom0_list[i]):
#       continue
    print dom0_list[i]
    j = open(dom0_list[i],"r")
    for line in j:
        if re.match('^Model_Name',line):
           model_num = line.split(':')[1].strip()
           #if (model_num == dom0_model):
           #   print CGREEN + "hardware model is same" + CEND
           #else:
           #   print CRED + "Hardware model is not same:" + CEND
        if re.match('^Pool',line):
           pool_name = line.split(':')[1].strip()
           #if (pool_name == dom0_pool):
           #   print CGREEN + "Dom0's belong to same pool" + CEND
           #else:
           #   print CRED + "Dom0's belong to different pool" + CEND
        if re.match('^Free_CPU',line):
           cpu_ava = int(line.split(':')[1].strip())
           #print cpu
           #print cpu_ava
           #if (cpu_ava > cpu):
           #   print CGREEN + "Dom0's have free cpu's" + CEND
           #else:
           #   print CRED + "Dom0's don't have enough cpu's" + CEND
        if re.match('^Free_Memory',line):
           memory_ava = int(line.split(':')[1].strip())
           #print memory_ava
           #if (memory_ava > memory):
           #   print CGREEN + "Dom0's have enough memory" + CEND
           #else:
           #   print CRED + "Dom0's don't have enough memory" + CEND

           if model_num == dom0_model and pool_name == dom0_pool and cpu_ava >= cpu and memory_ava > memory:
              print
              print CGREEN + "VM can be live migrated to this Dom0" + CEND, dom0_list[i]
              print
              print "#####################################"
              print
              print CGREEN + " Check List :" + CEND
              print
              print "Target Dom0 is the same Hardware model :", model_num
              print
              print "Pool is same:", pool_name
              print
              print "Dom0's have free cpu's:", cpu_ava
              print
              print "Dom0's have enough memory:", memory_ava
              print
              print "#####################################"
              print
           else:
              print CRED + "This Dom0 don't have enough Capacity" + CEND

#print j.read()
    i += 1
#    f = open("data", 'w')
#    f1 = open(dom0_list[i], 'r')
#    data = json.loads(f1)
#    f.write(json.dumps(data, indent=1))
#    f.close()

#Model Comparison

print "############################################"
[root@rmc002oodhost701 kuksanje]#                                            