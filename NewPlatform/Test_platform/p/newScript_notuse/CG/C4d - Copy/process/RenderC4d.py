#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys
from C4d import C4d
reload(sys)
sys.setdefaultencoding('utf-8')
class RenderC4d(C4d):
    def __init__(self,**paramDict):
        C4d.__init__(self,**paramDict)
        self.format_log('RenderC4d.init','start')
        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))
        self.format_log('done','end')