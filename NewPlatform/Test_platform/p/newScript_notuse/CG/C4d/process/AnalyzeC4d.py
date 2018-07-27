#!/usr/bin/env python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

""" C4d analyzer """

import os
import sys
import subprocess
import logging

reload(sys)
sys.setdefaultencoding('utf-8')

from C4d import C4d
from C4dLoader import C4dLoader
from C4dPluginManager import C4dPlugin, C4dPluginMgr
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

class AnalyzeC4d(C4d):
    def __init__(self, **paramDict):
        C4d.__init__(self, **paramDict)
        self.format_log('AnalyzeC4d.init', 'start')
        
        self.G_TIPS_TXT_NODE=os.path.join(self.G_WORK_RENDER_TASK_CFG, 'tips.json').replace('\\','/')

        for key, value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key + '=' + str(value))
            
        self.format_log('done','end')

    def RB_CONFIG(self):
        self.G_DEBUG_LOG.info('[C4d.Plugin.config.begin......]')

        self.plugin_config()

        self.G_DEBUG_LOG.info('[C4d.Plugin.config.end......]')

    def RB_RENDER(self):
        self.G_DEBUG_LOG.info('[c4d.RBanalyse.start.....]')

        cg_ver = self.G_CG_VERSION
        task_id = self.G_TASK_ID
        cg_file = self.G_INPUT_CG_FILE
        task_json = self.G_TASK_JSON
        asset_json = self.G_ASSET_JSON
        tips_json = self.G_TIPS_TXT_NODE

        c4d_loader = C4dLoader(cg_ver, task_id, cg_file, task_json, asset_json, tips_json)
        c4d_loader.execute()

        self.G_DEBUG_LOG.info('[c4d.RBanalyse.end.....]')

