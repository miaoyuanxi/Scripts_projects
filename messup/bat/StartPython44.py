'''
Created on 2013-6-21

@author: enfuzion
'''
import sys
import os,time
import subprocess

def exe():
    while( 2 > 1):
        try:
            path = "\\\\10.60.96.200\\tools\\startup\\"
            files = os.listdir(path)
            for file in files:
                if(file.find('.py') > -1):
                    command2 = 'c:\\python27\\python.exe ' + path + file
                else:
                    command2 = path + file
                print command2
                subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p = subprocess.Popen(command2, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)         
                while True:
                    buff = p.stdout.readline() 
                    if buff == '' and p.poll() != None: 
                        break
                    else:
                        print buff,
            
        except Exception as e:
            print e
        time.sleep(3600*34)
    

if (__name__ == '__main__'):
    print sys.argv
    #python batchcmd.py  "ping 128.0.0.%key%" 1 100
    exe()