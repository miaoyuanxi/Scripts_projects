#!/usr/bin/env python   
#coding=utf-8   
import os
import shutil
import sys
import time
import subprocess

#获取机器名 
def getHostName():   
        sys = os.name 
        hostname=""  
        if sys == 'nt':   
                hostname = os.getenv('computername')   
                #return hostname   
        elif sys == 'posix':   
                host = os.popen('echo $HOSTNAME')   
                try:   
                        hostname = host.read()   
                        #return hostname   
                finally:   
                        host.close()   
        print hostname
        return hostname
       
    
def changeEnfuzionCfg():
    hostname = getHostName()
    if len(hostname)==4:
        if(hostname.startswith('B')):
            last=int(hostname[1:])
            if(last >= 0 and last <= 100):
                #读取host文件
                lineNum=0
                path=r'C:\EnFuzion\enfuzion.options.txt'
                #要查找的字符
                findStr="property Windows,analyseNode"
                #要替换的字符
                replaceStr="property analyseNode,oversea\n"
                input = open(path, 'r')
                try:
                    flist = input.readlines() 
                    for line in  flist: 
                        lineNum +=1
                        if findStr in line:
                        #给这一行赋值
                            flist[lineNum-1]=replaceStr
                            f=open(path,'w')
                            f.writelines(flist)
                            break      
                finally:
                    input.close()
def changeHost():
    hostname = getHostName()
    if len(hostname)==4:
        last=int(hostname[-1])
        ip = ''
        if(last % 2 == 0):
            ip = '10.60.96.200'
        else:
            ip = '10.60.96.200'
        #读取host文件
        lineNum=0
        path=r'C:\WINDOWS\system32\drivers\etc\hosts'
        #要查找的字符
        findStr="poolIp"
        #要替换的字符
        replaceStr=ip + ' poolIp\n'
        exist = 0
        input = open(path, 'r')
        try:
            flist = input.readlines() 
            for line in  flist: 
                lineNum +=1
                if findStr in line:
                #给这一行赋值
                    exist = 1
                    flist[lineNum-1]=replaceStr
                    f=open(path,'w')
                    f.writelines(flist)
                    f.close()
                    break
            if(exist == 0):
                 output = open(path, 'a') 
                 replaceStr="\n"+replaceStr 
                 output .write(replaceStr)  
                 output .close( )              
        finally:
            input.close()
        

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
        time.sleep(3600*24)

#main方法   当执行python文件时从这里开始执行
if __name__ == '__main__':
    changeHost()
    changeEnfuzionCfg()
    exe()
   

    
    
