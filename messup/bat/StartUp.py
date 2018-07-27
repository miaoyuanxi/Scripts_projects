'''
Created on 2013-6-21

@author: enfuzion
'''
import sys
import os,time
import subprocess
import threading

class CycleThread(threading.Thread):
    def __init__(self,path,scriptType,sleepTime):
        threading.Thread.__init__(self)
        self.path = path
        self.scriptType = scriptType
        self.sleepTime = sleepTime
    def run(self):
        while 2 > 1:
            DataPath = os.path.join(self.path,self.scriptType) 
            if(os.path.exists(DataPath) == True):
#                os.makedirs(DataPath)
                files = os.listdir(DataPath)
                for file in files:
                    if(os.path.isfile(os.path.join(DataPath,file))):
                        try:
                            if(file.find('.py') > -1):
                                command2 = 'c:\\python27\\python.exe ' + os.path.join(DataPath,file)
                            else:
                                command2 = os.path.join(DataPath,file)
                            print command2
                            p = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)         
                            while True:
                                buff = p.stdout.readline() 
                                if buff == '' and p.poll() != None: 
                                    break
                                else:
                                    print buff,
                        except Exception as e:
                            print e
            if(self.scriptType == 'once'):
                break;
            time.sleep(self.sleepTime)


class Cycle5MinuteThread(threading.Thread):
    def __init__(self,path,sleepTime):
        threading.Thread.__init__(self)
        self.path = path
        self.sleepTime = sleepTime
    def run(self):
        # check the disk space, if still low, keep deleting except the last one.
        usedRate = getDiskUsedRate()
        if usedRate:
            if usedRate > 0.85:
                command2 = 'c:\\python27\\python.exe ' + self.path
                print "clean "+command2
                p = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                while True:
                    buff = p.stdout.readline() 
                    if buff == '' and p.poll() != None: 
                        break
                    else:
                        print buff,
            time.sleep(self.sleepTime)


def getDiskUsedRate():
    cmd = "fsutil volume diskfree D:"
    p = subprocess.Popen(cmd, shell=True,stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    (child_stdin, child_stdout) = (p.stdin, p.stdout)
    lines = child_stdout.readlines()
    child_stdin.close()
    child_stdout.close()
    try:
        nums = [ float( line.strip().partition(":")[2] ) for line in lines if line.strip() ]
        return 1-nums[2]/nums[1]
    except:
        print( "RV_Error: Cannot get the disk info correctly by executing \"%s\", please check if the disk is exist or not." % cmd )


def exe():
        path = r"\\10.60.96.200\tools\startup\\"
        cleanpath=path+"halfday\\clean.py"
        
        CycleThread(path,'daily',3600*24).start();
        CycleThread(path,'halfday',3600*12).start();
        CycleThread(path,'once',1).start();
        Cycle5MinuteThread(cleanpath,300).start();



if (__name__ == '__main__'):
    print sys.argv
    exe()