#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os 

class Custom():
    def __init__(self,log):
        self.PROCESS_LOG=log
        print ('init')
        
    def run(self):
        print 'do custom'
        self.PROCESS_LOG.info('--------------custom----------------')
        os.system(r'xcopy /y /v /e "B:\plugins\max\maxwell\maxwell3.2.7\3ds Max 2016" "C:\Program Files\Autodesk\3ds Max 2016"')
        os.system(r'xcopy /y  /e "B:\plugins\max\maxwell\maxwell3.2.7\3ds Max 2016\rlm" "C:\ProgramData\Next Limit\Maxwell\licenses\logs"')
        os.system(r'start "" "C:\ProgramData\Next Limit\Maxwell\licenses\logs\rlm.exe"')
        self.PROCESS_LOG.info('--------------custom.end----------------')
        
        
