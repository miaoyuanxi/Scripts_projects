#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys
from RenderBase import RenderBase
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

reload(sys)
sys.setdefaultencoding('utf-8')
class Houdini(RenderBase):
    def __init__(self,**paramDict):
        print("Houdini class")
        RenderBase.__init__(self,**paramDict)
        self.format_log('Houdini.init','start')
        self.G_RENDER_OPTIONS = {"render_rop":self.G_CG_OPTION} if self.G_CG_OPTION !=''else {} 
        
        #global variable
        # self.G_WORK_RENDER_TASK_BLOCK=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'block'))
        # self.G_WORK_RENDER_TASK_GRAB=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'grab'))
        # self.G_WORK_RENDER_TASK_MAX=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'max'))
        # self.G_WORK_RENDER_TASK_MAXBAK=os.path.normpath(os.path.join(self.G_WORK_RENDER_TASK,'maxbak'))
        dir_list=[]
        # dir_list.append(self.G_WORK_RENDER_TASK_BLOCK)
        # dir_list.append(self.G_WORK_RENDER_TASK_GRAB)
        # dir_list.append(self.G_WORK_RENDER_TASK_MAX)
        # dir_list.append(self.G_WORK_RENDER_TASK_MAXBAK)
        CLASS_COMMON_UTIL.make_dirs(dir_list)
        self.format_log('done','end')


    def LogsCreat(self,info='',render=False,debug=True):
        if render and debug:
            self.G_RENDER_LOG.info(str(info))
            self.G_DEBUG_LOG.info(str(info))
        elif render and not debug:
            self.G_RENDER_LOG.info(str(info))
        else:
            self.G_DEBUG_LOG.info(str(info))

    def Updata(self):
        pass