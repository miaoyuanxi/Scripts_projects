'''
Created on 2013-7-20

@author: Administrator
'''
#!/usr/bin/env python
#coding=utf-8
import os,sys,time,shutil


def main():
        try:
            DataPath = 'd:\\enfwork'
            files = os.listdir(DataPath)
            mtarrs = []
            for file in files:
                if(os.path.isdir(os.path.join(DataPath,file))):
                    #print os.stat(os.path.join(DataPath,file)).st_mtime
                    #print time.time()
                    #print (time.time() - os.stat(os.path.join(DataPath,file)).st_mtime) / 3600 /24
                    if((time.time() - os.stat(os.path.join(DataPath,file)).st_mtime) / 3600 /24 > 1):
                        print os.path.join(DataPath,file)
                        try:
                            shutil.rmtree(os.path.join(DataPath,file))
                        except Exception as e:
                             print e
            
            DataPath = 'd:\\'
            for file in files:
                 if(os.path.isfile(os.path.join(DataPath,file)) and file.find('.Cache')):
                     try:
                            os.remove(os.path.join(DataPath,file))
                     except Exception as e:
                             print e
                     
                      
            DataPath = 'd:\\log\\hardware'
            files = os.listdir(DataPath)
            mtarrs = []
            for file in files:
                if(os.path.isfile(os.path.join(DataPath,file))):
                    #print os.stat(os.path.join(DataPath,file)).st_mtime
                    #print time.time()
                    #print (time.time() - os.stat(os.path.join(DataPath,file)).st_mtime) / 3600 /24
                    if((time.time() - os.stat(os.path.join(DataPath,file)).st_mtime) / 3600 /24 > 2):
                        print os.path.join(DataPath,file)
                        try:
                            os.remove(os.path.join(DataPath,file))
                        except Exception as e:
                             print e
            print 'finished.....'
        except Exception as e:
            print e
                
if __name__ == '__main__':
    main()