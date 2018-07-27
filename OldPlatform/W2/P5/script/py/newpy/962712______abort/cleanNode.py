#coding=utf-8
#!/usr/bin/env python
'''
Created on 2014-09-25 14:44:22
modified 2015-7-13 18:54:19
@author: hyc

'''



import os,time,shutil
import threading,sys


keepTime = 1       # day
logKeepTime = 10   # day

removeTargets = []
removeTargets.append( '409577' )


keepId = ''
args = sys.argv
if args > 1:
    keepId = args[1]


class threadJob(threading.Thread):
    def __init__(self,DataPath,delFile):
        threading.Thread.__init__(self)
        self.DataPath = DataPath       
        self.delFile = delFile        
    def run(self):
        try:
            shutil.rmtree(os.path.join( self.DataPath, self.delFile), ignore_errors = True )
            print (os.path.join( self.DataPath, self.delFile)),' is cleared'
        except:
            os.remove(os.path.join( self.DataPath, self.delFile) )


def cleanEnfwork():
    try:
        DataPath = 'd:\\enfwork'
        delFiles = {}
        stayTime = 0.0
        files = []
        if os.path.isdir(DataPath):
            files = os.listdir(DataPath)
        if files:
            for file in files:
                if(os.path.isdir(os.path.join(DataPath,file))):
                    stayTime = (time.time() - os.stat(os.path.join(DataPath,file)).st_mtime) / 3600 /24 
                    # store the old files with their modified times to 'delFiles'(dict)
                    if( stayTime>keepTime or file in removeTargets):
                        delFiles[file] = stayTime
            # delete all the old folder except keepId folder
            for item in delFiles.keys():
                try:
                    if not item == keepId:
                        job = threadJob(DataPath,item)
                        job.start()
                        print('Enfwork folder \' %s \' is cleared.' % os.path.join(DataPath,item) )                        
                except Exception as e:    
                     print e
                     continue
          

    except Exception as e:
        print e



def deleteStuffInFolder(DataPath,stayTime):
    if os.path.isdir(DataPath):            
        files = os.listdir(DataPath)
        if DataPath == 'd:/log':
            dgtNames = []
            for i in files:
                if i.isdigit():
                    dgtNames.append( i )
            files = dgtNames
        for file in files:
            try:
                if( ( time.time() - os.stat( os.path.join ( DataPath,file ) ).st_mtime ) / 3600 /24 > stayTime ):
                    if not file == keepId:
                        job = threadJob( DataPath, file )
                        job.start()
                        print('The folder \' %s \' is cleared.' % DataPath )
            except Exception as e:
                print e
                continue
        





def main():
    print('\n\n\n>>>>>>>>>>>>>>> clean.py is now working >>>>>>>>>>>>>>>>\n')  
    print 'keep taskId: %s \n' % keepId          
    cleanEnfwork()
    deleteStuffInFolder( 'd:/log/hardware' , keepTime )
    deleteStuffInFolder( 'd:/work/helper' , keepTime )
    deleteStuffInFolder( 'd:/work/render' , keepTime )
    deleteStuffInFolder( 'd:/renderwork' , keepTime )
    deleteStuffInFolder( 'd:/log' , logKeepTime )
            
    print ('\n>>>>>>>>>> clean.py finish running in : %s  >>>>>>>>>>>\n\n\n' % time.strftime('%Y-%m-%d %H:%M:%S') ) 
    

                
if __name__ == '__main__':
    main()
    
    
    
    
    
