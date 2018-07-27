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
        
        
