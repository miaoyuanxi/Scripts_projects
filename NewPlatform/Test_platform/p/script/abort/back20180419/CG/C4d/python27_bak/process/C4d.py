#!/usr/bin/python  
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from RenderBase import *
from C4dPluginManager import C4dPlugin, C4dPluginMgr
from CommonUtil import RBCommon as CLASS_COMMON_UTIL


class C4d(RenderBase):
    def __init__(self, **param_dict):
        RenderBase.__init__(self,**param_dict)
        self.format_log('C4d.init','start')
        #global variable
        #self.G_SCENE_INFO = self.G_TASK_JSON_DICT['scene_info']
        self.format_log('done','end')

    def get_node(self, node):
        node=sys.argv[5]
        if "A" in node or "B" in node or "C" in node or "D" in node or "E" in node or "F" in node:
            return "ABCDEF"
        if "K" in node:
            return "K"
        if "L" in node or "M" in node or "N" in node or "O" in node or "P" in node or "Q" in node:
            return "LNOPQ"
        if "G" in node or "H" in node or "J" in node:
            return "GHJ"
        return "ABCDEF"  


    def plugin_config(self):
        if self.G_CG_CONFIG_DICT.has_key('plugins'):
            print (self.G_CG_CONFIG_DICT)
            plugin_dict = self.G_CG_CONFIG_DICT['plugins']
            
            for plugins_key in plugin_dict.keys():
                plugin_str = plugins_key + plugin_dict[plugins_key]
                node = self.get_node(self.G_NODE_NAME)

                plugin_mgr = C4dPluginMgr(self.G_USER_ID, self.G_PLUGIN_PATH)
                #plugin_mgr.copy_R18_exe(self.G_CG_VERSION)
                #self.G_DEBUG_LOG.info('copy_R18_exe was done!!!')
                for key, value in self.G_CG_CONFIG_DICT['plugins'].items():
                    print (key, value, self.G_CG_VERSION)
                    plugin = C4dPlugin()
                    plugin.plugin_name = key
                    plugin.plugin_version = value
                    plugin.soft_version = self.G_CG_VERSION
                    plugin.node = node
                    
                    c4d_plugin_config = '[ python = "' + self.G_NODE_PY + r'\CG\C4d\function\C4dPluginManager.py" "%s" "%s" "%s" "%s" ]' % (plugin.plugin_name, \
                                                                                plugin.plugin_version, \
                                                                                plugin.soft_version, \
                                                                                plugin.node)
                    #print c4d_plugin_config
                    self.G_DEBUG_LOG.info(c4d_plugin_config)

                    result = plugin_mgr.set_custom_env(plugin)

        else:
            print ('There is no key with plugins in the task.json')
        


        