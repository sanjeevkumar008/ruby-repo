[root@vmohsplab03 kuksanje]# more postexec.py
#!/usr/bin/python
########################    Post Execution checkpoints   ##########################
# Verstion 1.0
# Created date  : 05-18-2018
# Last Modified : 06-23-2018

##############################################################################
###### Variable defination ####
########################################################

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

CBLACKBG  = '\33[40m'
CREDBG    = '\33[41m'
CGREENBG  = '\33[42m'
CYELLOWBG = '\33[43m'
CBLUEBG   = '\33[44m'
CVIOLETBG = '\33[45m'
CBEIGEBG  = '\33[46m'
CWHITEBG  = '\33[47m'

CGREY    = '\33[90m'
CRED2    = '\33[91m'
CGREEN2  = '\33[92m'
CYELLOW2 = '\33[93m'
CBLUE2   = '\33[94m'
CVIOLET2 = '\33[95m'
CBEIGE2  = '\33[96m'
CWHITE2  = '\33[97m'

CGREYBG    = '\33[100m'
CREDBG2    = '\33[101m'
CGREENBG2  = '\33[102m'
CYELLOWBG2 = '\33[103m'
CBLUEBG2   = '\33[104m'
CVIOLETBG2 = '\33[105m'
CBEIGEBG2  = '\33[106m'
######################################################
############### Imported Function ####################

import os, sys
import os.path
import subprocess
import errno
import smtplib
import getpass
from string import Template
import shlex
import glob
lines = []
######################################################
################# List Defined #######################

gen_list = ["CRS is closed (Yes/No/NA) : ","Blackout is closed (Yes/No/NA) : "]
list3 = ["Backup images taken if any are removed (Yes/No/NA): ","ITAS updated with OS (Yes/No/NA): "]
list4 = ["ITAS Updated (Yes/No/NA): ","Folder appended with DO_NOT_USE in 2.x (Yes/No/NA):","Source Dom0 empty (Yes/No/NA):","ITAS updated to -SAV for Dom0 (Yes/No/NA) : ","Sym-links removed from old Dom0 (Yes/No/NA) : ","Sym-links created on target Dom0 (Yes/No/NA) : ","oem1 old share expired (Yes/No/NA) : ","Swap share expired (Yes/No/NA) : ","Verify EM agent is working fine (Yes/No/NA) : "]
list5 = ["ITAS Updated (Yes/No/NA): ","Sym-links removed from old Dom0 (Yes/No/NA) : ","Sym-links created on target Dom0 (Yes/No/NA) : ","oem1 old share expired (Yes/No/NA) : ","Verify EM agent is working fine (Yes/No/NA) : "]
list6 = ["ITAS Updated (Yes/No/NA): ","Sym-links removed from old Dom0 (Yes/No/NA) : ","Sym-links created on target Dom0 (Yes/No/NA) : ","oem1 old share expired (Yes/No/NA) : ","Verify EM agent is working fine (Yes/No/NA) : "]
list7 = ["-n server destroyed (Yes/No/NA) : ","Renamed and expired iSCSI LUN (Yes/No/NA) : ","Verified agent is up and working after migration (Yes/No/NA) : ","Notified EM to remove monitoring for -n server (Yes/No/NA) : ","BESR configured and verified (Yes/No/NA) : ","ITAS Verified (Yes/No/NA) : "]
list8 = ["UUID restored after the swap (Yes/No/NA) : ","Hardware health is good (Yes/No/NA) : ","MTU is same as before (Yes/No/NA) : ","Server health good inOVMM (Yes/No/NA) : ","Verify ITAS update (Yes/No/NA) : ","Restore symlinks for VMs (Yes/No/NA) : ","ILOM upgraded to released (Yes/No/NA) : "]
list9 = ["Verify ITAS update  (Yes/No/NA) : ","Physical server to be renamed as -SAV (Yes/No/NA) : ","New record to be created for VM (Yes/No/NA) : ","CreateSymlink on Dom0 (Yes/No/NA) : ","oem1 old share expired (Yes/No/NA) : ", "Verify EM agent is working fine (Yes/No/NA) : "]
list10 = ["Hardware health is good  (Yes/No/NA) : ","MTU is same as before (Yes/No/NA) : ","Verify ITAS update (Yes/No/NA) : ","ILOM upgraded to latest (Yes/No/NA) : "]
list11 = ["ILOM upgraded  (Yes/No/NA) : ","Hardware health is good (Yes/No/NA) : "]
list12 = ["Network configs modified in firststart.img  (Yes/No/NA) : "]
list13 = ["Cleanup done of unnecessary mount points from source (Yes/No/NA) : ","Logarch removed from source crontab : "]
list14 = ["Verify ITAS update (Yes/No/NA) : ","Symlinks removed from source (Yes/No/NA) : ","Symlinks added to target (Yes/No/NA) : "]


#####################################################
# Function definition is here
def printme( str ):
   "This prints a passed string into this function"
   print ( str )
   return;

#path = '/home/kuksanje/mig-os/logs/postwork'
path = '/mig-os/logs/post_checklist/'


#######################################################
############# Main Function
def data(rfc,path,userid):
   if not os.path.exists(path + rfc):
      os.makedirs(path + rfc)
   save_path = path + rfc
   print save_path
   os.chdir(save_path)

########################################################
############## Email Function

def exam():
#   sender = 'sanjeev.kumar@oracle.com'
   sender = ''
   receivers = ['sanjeev.p.kumar@oracle.com']
#   receivers = ['pavithra.rajamohan@oracle.com']
   #cmd = "getent passwd userid | awk -F':' {'print $5'}"
   #ps = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   #sender = ps.communicate()[0]
   s = Template("""From:
To: sanjeev.p.kumar@oracle.com
Subject: CRT Extension $rfc
Hi Pavithra,

With reference to the RFC  $rfc, we have taken extension in CRT. Below are the details:

RFC Number :  $rfc
Execution Analyst :  $userid
Extension Time: $act2
Summary : ext.read()


Thanks and Regards,
$userid
   """)
   message = s.substitute(rfc=rfc, userid=userid, act2=act2, ext=ext)

   try:
      smtpObj = smtplib.SMTP('localhost')
      smtpObj.sendmail(sender, receivers, message)
      print "Successfully sent email"
   except SMTPException:
      print "Error: unable to send email"

########################################################
def yes_no():
# raw_input returns the empty string for "enter"
#   yes = {'yes', 'y', 'ye', 'YES', 'Y', 'YE', 'na', 'NA'}
#   no = {'no','n'}

   choice = raw_input().lower()
   if choice in yes:
     return True
   elif choice in no:
     return False
   else:
     sys.stdout.write("Please respond with 'yes' or 'no'")

#######################################################
def filepath():
   if os.path.exists("out.txt"):
    os.remove("out.txt")
   #os.rename("out.txt", "out.old.txt")
   if os.path.exists("ext.txt"):
    os.remove("ext.txt")
   if os.path.exists("OutFile.txt"):
    os.remove("OutFile.txt")
   file = open('out.txt','a+')
   file.write('\n')
   file.write('############################### Post Execution Checklist ###########################')
   file.write('\n')
   file.write('\n')
   print >> file, CRED + "Post execution is performed by : " + CEND, userid
   file.write('\n')
   file.close()

def generic(list):
   i = 0
   while i < len(list):
      ack = raw_input(CYELLOW + list[i] + CEND)
      file = open('out.txt','a+')
      file.write('\n')
      print >> file, CGREEN + list[i] + CEND, ack
      file.close()
      i += 1
      if ack == 'y' or ack == 'Y' or ack == 'Yes' or ack == 'yes' or ack == 'YES' or ack == 'NA' or ack == 'na' or ack == 'Na':
       print
      else:
       print CRED + "Please complete the task and re-run the script or re-run and enter the right value" + CEND
       #exit()
       #quit()
       sys.exit()

#########################################################

def activity():
   act = None
   act1 = None
   act = raw_input(CVIOLET + "Is there any other activity performed (y/n) : " + CEND)
   print
   while act != 'y' or act != 'n':
      if act == 'y': #or act == 'Y' or act == 'yes' or act == 'YES':
         menu()
         break
      elif act == 'n': #or act == 'N' or act == 'no' or act == 'NO':
         generic(gen_list)
         act1 = raw_input(CYELLOW + "Is activity has completed in CRT (y/n) : " + CEND)
         print
         if act1 == 'y': #or act1 == 'Y' or act1 == 'yes' or act1 == 'YES':
            print "Good"
            break
         elif act1 == 'n':
            global act2
            global act3
            global ext
            ext = open('ext.txt','a+')
            ext.write('\n')
            while True:
               act2 = raw_input(CYELLOW + "Please enter the extension time (minute) : " + CEND)
               try:
                  if(int(act2)):
                     print
                     print >> ext, CYELLOW + "Extension Time is : " + CEND, act2
                     break
               except ValueError:
                  print "This is not a number, Please try again."

            print
            #act3 = raw_input(CYELLOW + "Please enter the summary and press ENTER D to save : " + CEND)
            ext = open('ext.txt','a+')
            ext.write('\n')
            print CYELLOW + "Please enter the summary and press ENTER to save : " + CEND
            print >> ext, CYELLOW + "The Summary : " + CEND
            while True:
               try:
                  act3 = raw_input()
                  if act3:
                     lines.append(act3)
                  else:
                     break;
               except EOFError:
                  return
            ext = open('ext.txt','a+')
            for i in lines:
               print >> ext, (i)
            exam()
            break
          # else:
          #   sys.stdout.write("Please respond with 'yes' or 'no'. ")
      else:
         sys.stdout.write("Please respond with 'y' or 'n'. ")

######################################################## 

########################################################
def menu():
   #filepath()
   print CGREEN + "Welcome : " + CEND, userid

   print 30 * "-" ,CVIOLET +  "Maintenance Activity List" + CEND, 30 * "-"
   print "[01]. Kernel Upgrade                                    [09]. P2V Migration"
   print "[02]. VM Resize                                         [10]. Hardware Swap"
   print "[03]. OS Migration                                      [11]. OVMS Upgrade"
   print "[04]. 3.2.x Migration                                   [12]. Subnet move"
   print "[05]. VM Move                                           [13]. Instance Move"
   print "[06]. VM Move and Resize                                [14]. Live Migration"
   print "[07]. Windows Migration                                 [15]. Other"
   print "[08]. Dom0 Swap                                         "
   print 67 * "-"
   print 67 * "-"
   file = open('out.txt','a+')
   file.write('\n')
   loop=True
   while loop:          ## While loop which will keep going until loop = False
      choice = raw_input("Enter the activity : ")
      print
      if choice=='1':
         print >> file, CBOLD + CBLUE + "Kernel Upgrade : " + CEND
         file.write('\n')
         file.close()
         activity()
         break
      elif choice=='2':
         file.close()
         activity()
         break
      elif choice=='3':
         print >> file, CBOLD + CBLUE + "OS Migration : " + CEND
         file.write('\n')
         file.close()
         generic(list3)
         activity()
         break
      elif choice=='4':
         print >> file, CBOLD + CBLUE + "3.2.x Migration : " + CEND
         file.write('\n')
         file.close()
         generic(list4)
         activity()
         break
      elif choice=='5':
         print >> file, CGREEN + "VM Move : " + CEND
         file.write('\n')
         file.close()
         generic(list5)
         activity()
         break
      elif choice=='6':
         print >> file, CBOLD + CBLUE + "VM Move and Resize : " + CEND
         file.write('\n')
         file.close()
         generic(list6)
         activity()
         break
      elif choice=='7':
         print >> file, CBOLD + CBLUE + "Windows Migration : " + CEND
         file.write('\n')
         file.close()
         generic(list7)
         activity()
         break
      elif choice=='8':
         print >> file, CBOLD + CBLUE + "Dom0 Swap : " + CEND
         file.write('\n')
         file.close()
         generic(list8)
         activity()
         break
      elif choice=='9':
         print >> file, CBOLD + CBLUE + "P2V Migration : " + CEND
         file.write('\n')
         file.close()
         generic(list9)
         activity()
         break
      elif choice=='10':
         print >> file, CBOLD + CBLUE + "Hardware Swap : " + CEND
         file.write('\n')
         file.close()
         generic(list10)
         activity()
         break
      elif choice=='11':
         print >> file, CBOLD + CBLUE + "OVMS Upgrade : " + CEND
         file.write('\n')
         file.close()
         generic(list11)
         activity()
         break
      elif choice=='12':
         print >> file, CBOLD + CBLUE + "Subnet move : " + CEND
         file.write('\n')
         file.close()
         generic(list12)
         activity()
         break
      elif choice=='13':
         print >> file, CBOLD + CBLUE + "Instance Move : " + CEND
         file.write('\n')
         file.close()
         generic(list13)
         activity()
         break
      elif choice=='14':
         print >> file, CBOLD + CBLUE + "Live Migration : " + CEND
         file.write('\n')
         file.close()
         generic(list14)
         activity()
         break
      elif choice=='15':
         print >> file, CBOLD + CBLUE + "Other : " + CEND
         file.write('\n')
         file.close()
         activity()
         break
      elif choice=='q':
         print "[Q]. Quitting Program!!!!!"
         loop=False # This will make the while loop to end as not value of loop is set to False
      else:
         # Any inputs other than values A-P  we print an error message
         raw_input(CRED + "Wrong option selection. Press Enter key to try again.." + CEND)

########################################################
subprocess.call(["clear"])
fileDir = os.path.dirname(os.path.realpath('__file__'))
#print fileDir
#userid = getpass.getuser()
userid = os.getlogin()
#userid = "sanjeev"
print
rfc = raw_input(CYELLOW + "Please Enter The RFC Number : " + CEND)
print
print CYELLOW + "RFC Number Entered By You Is :" + CEND,  rfc
print
while True:
   input = raw_input("Is this Correct (y/n) :  ")
   if input.strip() == 'y':
      print "You have entered : ", rfc
      save_path = path + rfc
      data(rfc,path,userid)
      filepath()
      menu()
      break
   else:
         rfc = raw_input(CRED + "Please Enter The Correct RFC Number :  " + CEND)

#############################################################################

#############################################################################
file = open('out.txt','a+')
print
file.write('\n')
file.write('####################################################################################')
file.write('\n')
file.close()
file = open("out.txt","r")
print
print file.read()

file1 = open('ext.txt','a+')
print
file1.write('\n')
file = open('out.txt','a+')
os.system("cat out.txt ext.txt  >> OutFile.txt")
f = open('OutFile.txt', 'a+')
f.write('\n')
f.write('####################################################################################')


########################################################################
#print(CRED + "Error, does not compute!" + CEND)
print CBLUE + "Logs are saved into :", path + rfc  + CEND
os.chdir(fileDir)
print
[root@vmohsplab03 kuksanje]#                                                    