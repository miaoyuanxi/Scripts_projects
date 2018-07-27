#!/usr/bin/env python
# author : lynne
# create date : 2017-09-15
# -*- coding: utf-8 -*-

import os,sys
import logging
from C4d import C4d
reload(sys)
sys.setdefaultencoding('utf-8')

class AnalyzeC4d(C4d):
    def __init__(self, **paramDict):
        C4d.__init__(self, **paramDict)
        self.format_log('AnalyzeC4d.init', 'start')
        
        for key, value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key + '=' + str(value))
            
        self.format_log('done','end')
        