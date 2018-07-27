#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import time
import shutil
import codecs
import ConfigParser
import threading
import time
import json
import socket
import re
import multiprocessing

reload(sys)
sys.setdefaultencoding('utf-8')
from Maya import Maya
from MayaPlugin import MayaPlugin                             

from CommonUtil import RBCommon as CLASS_COMMON_UTIL
from MayaUtil import RBMayaUtil as CLASS_MAYA_UTIL








class RenderMaya(Maya):
    def __init__(self,**paramDict):
        Maya.__init__(self,**paramDict)
        self.format_log('RenderMaya.init','start')
        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))
        self.format_log('done','end')
        
        
    def RB_CONFIG(self):
        self.format_log('渲染配置','start')
        self.G_DEBUG_LOG.info('[RenderMaya.RB_CONFIG.start.....]')
        
        CLASS_MAYA_UTIL.killMayabatch(self.G_DEBUG_LOG)  #kill mayabatch.exe
        

        
        #----------------load maya plugin-------------------
        self.G_DEBUG_LOG.info('插件配置')

        if self.G_CG_CONFIG_DICT:
            sys.stdout.flush()

            if "gpu_card_no" in os.environ:
                print "gpu_card_no: " + os.environ["gpu_card_no"]
            else:
                print "gpu_card_no variable is not exists."
            sys.stdout.flush()

            # print "MAYA_SCRIPT_PATH: " + os.environ["MAYA_SCRIPT_PATH"]
            plginLd = MayaPlugin()
            sys.stdout.flush()
            if self.G_PLUGIN_PATH:
            
                # self.G_NODE_MAYAFUNCTION=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Maya/function'))
                
                custom_file=os.path.join(self.G_NODE_MAYAFUNCTION,'MayaPluginPost.py').replace('\\','/')               

                
                sys.stdout.flush()
                print "custom_config is: " + custom_file
                sys.stdout.flush()
            print "plugin path:"
            print self.G_CG_CONFIG_DICT
            sys.stdout.flush()
            plginLd.MayaPlugin(self.G_CG_CONFIG_DICT, [custom_file])
            # print "MAYA_SCRIPT_PATH: " + os.environ["MAYA_SCRIPT_PATH"]
            sys.stdout.flush()
       
        
        if self.G_CG_CONFIG_DICT:
            renderSoftware = self.G_CG_CONFIG_DICT['cg_name']
            softwareVer = self.G_CG_CONFIG_DICT['cg_version']
            plugis_list_dict = self.G_CG_CONFIG_DICT['plugins']
            print plugis_list_dict
       

        
        self.G_DEBUG_LOG.info('[RenderMaya.RB_CONFIG.end.....]')
        self.format_log('done','end')        
        
        
        
        
        
        
    '''
        渲染
    '''
    def RB_RENDER(self):#5
        self.format_log('渲染','start')
        self.G_DEBUG_LOG.info('[RenderMaya.RB_RENDER.start.....]')
        

        
        #------------get render cmd----------
        render_cmd = self.get_render_cmd()
        
        self.G_DEBUG_LOG.info(render_cmd)
        


        #------------render----------
        render_cmd=render_cmd.encode(sys.getfilesystemencoding())
        self.G_KAFKA_MESSAGE_BODY_DICT['startTime']=str(int(time.time()))

        self.G_DEBUG_LOG.info("\n\n-------------------------------------------Start maya program-------------------------------------\n\n")
        
        CLASS_COMMON_UTIL.cmd(render_cmd,my_log=self.G_DEBUG_LOG,continue_on_error=True,my_shell=True)
        
        CLASS_MAYA_UTIL.kill_lic_all(my_log=self.G_DEBUG_LOG)
        
        self.G_KAFKA_MESSAGE_BODY_DICT['endTime']=str(int(time.time()))

        
        self.G_DEBUG_LOG.info('[RenderMaya.RB_RENDER.end.....]')
        self.format_log('done','end')
        
        
        
    def get_render_cmd(self):
        renderSettings = {}
        mappings = ''

        
        renderSettings["start"] = self.G_CG_START_FRAME
        renderSettings["end"] = self.G_CG_END_FRAME
        renderSettings["by"] = self.G_CG_BY_FRAME
        renderSettings["renderableLayer"] = self.G_CG_LAYER_NAME
        renderSettings["renderableCamera"] = self.G_CG_OPTION
        renderSettings["projectPath"] = self.G_INPUT_PROJECT_PATH
        renderSettings["output"] = self.G_WORK_RENDER_TASK_OUTPUT
        
        renderSettings["width"] = self.G_TASK_JSON_DICT['scene_info_render']['common']['width']
        renderSettings["height"] = self.G_TASK_JSON_DICT['scene_info_render']['common']['height']

        renderSettings["maya_file"] = self.G_INPUT_CG_FILE

        renderSettings["render.exe"] = "C:/Program Files/Autodesk/" \
            "maya%s/bin/render.exe" % (self.G_CG_CONFIG_DICT['cg_version'])

        if self.G_CG_CONFIG_DICT:
            renderSoftware = self.G_CG_CONFIG_DICT['cg_name']
            softwareVer = self.G_CG_CONFIG_DICT['cg_version']
            plugis_list_dict = self.G_CG_CONFIG_DICT['plugins']
            print plugis_list_dict        
        
        
        # self.G_NODE_MAYASCRIPT=os.path.normpath(os.path.join(self.G_NODE_PY,'CG/Maya/script'))
        
        G_RN_MAYA_FILE=os.path.join(self.G_NODE_MAYASCRIPT,'Render.py').replace('\\','/')
    
        if renderSettings["projectPath"]:
            if os.path.exists(renderSettings["projectPath"]):
                os.chdir(renderSettings["projectPath"])
                
                

                
                
        #"-----------------------------cmd--------------------------------"
        cmd = "\"%(render.exe)s\" -s %(start)s -e %(end)s -b %(by)s " \
            "-proj \"%(projectPath)s\" -rd \"%(output)s\"" \
            % renderSettings

        if renderSettings["renderableCamera"]:
            if not "," in renderSettings["renderableCamera"] and \
                not "{rayvision}" in renderSettings["renderableCamera"]:
                cmd += " -cam \"%(renderableCamera)s\"" % renderSettings

        if renderSettings["renderableLayer"]:
            if not "," in renderSettings["renderableLayer"]:
                cmd += " -rl \"%(renderableLayer)s\"" % renderSettings
                
        # cmd += " -preRender \"python \\\"user_id=%s;mapping=%s;plugins=%s;taskid=%s;rendersetting=%s;execfile(\\\\\\\"%s\\\\\\\")\\\"\"" % (self.G_USER_ID,mappings,plugis_list_dict,self.G_TASK_ID,renderSettings,G_RN_MAYA_FILE)        
          

            
            
        #---------------render cmd-------------------------  
        if "RenderMan_for_Maya" in plugis_list_dict:
            cmd += " -r rman"

                
        elif "mtoa" in plugis_list_dict:
            cmd += " -r arnold -ai:lve 1"
        
        
        
        elif "redshift_GPU" in plugis_list_dict:

            cmd += " -preRender \"python \\\"user_id=%s;mapping=%s;plugins=%s;taskid=%s;rendersetting=%s;execfile(\\\\\\\"%s\\\\\\\")\\\"\" -r redshift -logLevel 2 " % (self.G_USER_ID,mappings,plugis_list_dict,self.G_TASK_ID,renderSettings)


            # cmd += " -preRender \"_RV_RSConfig;\" -r redshift -logLevel 2"
            if "gpuid" in os.environ:
                gpu_n= int(os.environ["gpuid"]) - 1
            else :
                gpu_n="0"

            gpu_n="0,1"
            cmd += " -gpu {%s}" % (gpu_n)
            
        elif "vrayformaya" in plugis_list_dict:
            pass
        #-------mentalray---------------    
        
        max_threads_number = int(multiprocessing.cpu_count())
        
        elif " -r " not in cmd and float(softwareVer) < 2017:
            cmd += " -mr:art -mr:aml"



        if "-r rman" in cmd:
            cmd += " -setAttr Format:resolution \"%(width)s %(height)s\" \"%(maya_file)s\"" % renderSettings
        else:
            cmd += " -x %(width)s -y %(height)s \"%(maya_file)s\"" % renderSettings                
                
        # cmd += " \"%(maya_file)s\"" % renderSettings    
        
        render_cmd = cmd
        print "render cmd info:"
        print render_cmd
        sys.stdout.flush()        
        
        # G_JOB_NAME=os.environ.get('G_JOB_NAME')
        # render_log_path = "d:/log/render"
        # render_log = "%s/%s/%s_render.log" % (render_log_path,self.G_TASK_ID,G_JOB_NAME)
        # print render_log
        # with open(render_log,"ab+") as l:
            # l.write('render cmd info: \n')
            # #l.write(cmd)
            # l.flush()
            # if isinstance(cmd, list):
                # for i in cmd:
                    # print "render cmd info:"
                    # print i
                    # sys.stdout.flush()
                    
                    # for line in RvOs.run_command(i):
                        # l.write(line)
                        # l.flush()
                        # line_str = line.strip()
                        # if line_str:
                            # pass
                            # print line_str
            # else:
                # # subprocess.call(cmd)
                # is_complete = 0
                # re_complete = re.compile(r'Scene.+completed\.$', re.I)
                # for line in RvOs.run_command(cmd):
                    # l.write(line+"\n")
                    # l.flush()
                    # line_str = line.strip()
                    # if line_str:
                        # pass
                        # print line_str
                        # if re_complete.findall(line_str):
                            # RvOs.kill_children()
                            # is_complete = 1
                            # break

                # if not is_complete:
                    # exit(1)



        
        return render_cmd        
        
        
            