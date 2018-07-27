#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys,time
import subprocess
from Houdini import Houdini
from HoudiniUtil import HoudiniUtil
from HoudiniPlugin import HoudiniPlugin
from CommonUtil import RBCommon as CLASS_COMMON_UTIL

reload(sys)
sys.setdefaultencoding('utf-8')
class RenderHoudini(Houdini):
    def __init__(self,**paramDict):
        Houdini.__init__(self,**paramDict)
        self.format_log('RenderHoudini.init','start')
        for key,value in self.__dict__.items():
            self.G_DEBUG_LOG.info(key+'='+str(value))


        # --------------------------------------------------------------------

        self._run_code_result = True
        self._erorr_code = ''
        self._erorr_code_info = ''
        self._plugins_surpose = ['Redshift','Arnold']
        self._Killapps =[]
        self._render_frame = 1 # 1: normal,2: mult

        # --------------------------------------------------------------------

        self.format_log('done','end')        


    def BaseDataSetup(self):
        self.LogsCreat("BaseDataSetup start...")
        self.LogsCreat("...")
        
        self._hip_file = self.G_INPUT_CG_FILE.replace("\\","/") if len(self.G_INPUT_CG_FILE) else ''
        self._output = self.G_WORK_RENDER_TASK_OUTPUT.replace("\\","/")
        self._task_folder = self.G_WORK_RENDER_TASK.replace("\\","/")

        self._frames = [self.G_CG_START_FRAME,self.G_CG_END_FRAME,self.G_CG_BY_FRAME]
        self._rop_node = self.G_RENDER_OPTIONS['render_rop']if 'render_rop' in self.G_RENDER_OPTIONS.keys()else ''
        if self._rop_node == '': ## call errors 
            self._run_code_result = False
            self._erorr_code = 'RenderHoudini.BaseDataSetup.rop call'
            self._erorr_code_info = 'The rop is not set!.'

        if self.G_RENDER_OS=='Linux':
            self._houdini_client_dir = '/D/plugins/houdini'
            self._houdini_PLuing_dirt = '/B/plugins/houdini' if os.path.exists("/B/plugins/houdini") else "%s/plugins/houdini"%self.G_PLUGIN_PATH.replace("\\","/")
            app_path = "%s/apps/Linux"%self._houdini_PLuing_dirt
        else:
            self._houdini_client_dir = 'D:/plugins/houdini'
            self._houdini_PLuing_dirt = 'B:/plugins/houdini' if os.path.exists("B:/plugins/houdini") else "%s/plugins/houdini"%self.G_PLUGIN_PATH.replace("\\","/")
            app_path = "%s/apps/win"%self._houdini_PLuing_dirt

        self._code_base_path = os.path.join(self.G_NODE_PY,"CG/Houdini").replace("\\","/")
         
        hfs_save_version = ''
        hip_val = os.path.dirname(self._hip_file)

        self._hfs_version = ''
        self._hip_save_val = ''
        self._plugins = self.G_CG_CONFIG_DICT["plugins"]


        # get imformation from the .hip file
        # version && $HIP
        if os.path.isfile(self._hip_file):
            hip_file_info = HoudiniUtil.GetSaveHipInfo(self._hip_file,app_path)
            if len(hip_file_info)==3:
                hfs_save_version = hip_file_info[0]
                self._hfs_version = hip_file_info[1]
                self._hip_save_val = hip_file_info[2]
            else:
                self._run_code_result = False
                self._erorr_code = 'RenderHoudini.GetSaveHipInfo.HoudiniUtil.GetSaveHipInfo'
                self._erorr_code_info = hip_file_info[0]

        # --------------------------------------------------------------------------------
        #                           JOB INFORMATION PRINT
        # --------------------------------------------------------------------------------
            self.LogsCreat("JOB INFORMATION")
            self.LogsCreat("Function: %s"% (self.G_ACTION if not self.G_ACTION=='' else 'Render'))
            self.LogsCreat("File saved with Houdini %s"%hfs_save_version)
            self.LogsCreat("File saved with $HIP val %s"%self._hip_save_val)
            self.LogsCreat("...")
            self.LogsCreat("Final Houdini version to run this Job : %s"%self._hfs_version)
            self.LogsCreat("Hip file: %s"%self._hip_file)
            self.LogsCreat("Final $HIP val to run this Job : %s"%hip_val)
            self.LogsCreat('...')
            self.LogsCreat("Plugins Info: %s"%self._plugins)
            self.LogsCreat("Frames: %s"%self._frames)
            self.LogsCreat("Rop: %s"%self._rop_node)
        # --------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------
        #                             RENDER LOG INFORMATION PRINT
        # --------------------------------------------------------------------------------
            
            self.LogsCreat("Log start...\n"+"-"*150+"\n"+"/"*150+"\n"+"-"*150+"\n",True,False)
            houdini_verser_full = self._hfs_version[:2]+"."+self._hfs_version[2:3]+"."+self._hfs_version[3:]
            self.LogsCreat("Software: Houdini %s\n\n"%houdini_verser_full,True,False)
        else:
            self._run_code_result = False
            self._erorr_code = 'RenderHoudini.BaseDataSetup'
            self._erorr_code_info = 'The .hip file is not exist.'

        self.LogsCreat("BaseDataSetup end.")
        self.LogsCreat("")

    def PluginsSetup(self):
        self.LogsCreat("PluginsSetup start...")
        try:
            returninfo = HoudiniPlugin.SetRenderer(self._hfs_version,self._plugins,self._houdini_PLuing_dirt,self._plugins_surpose)

            self._PluginsSetup_run_info = returninfo["info"]
            self._Killapps.extend(returninfo["app"])
                
        except Exception as e:
            self._run_code_result = False
            self._erorr_code = 'HoudiniPlugin.SetRenderer'
            self._erorr_code_info = e


    def AssetSetup(self):
        self.LogsCreat("AssetSetup start...")
        try:
            self._AssetSetup_run_info = ['AssetSetup']
        except Exception as e:
            self._run_code_result = False
            self._erorr_code = 'AssetSetup'
            self._erorr_code_info = e

    def CustomSetup(sefl):
        self.LogsCreat("CustomSetup start...")
        try:
            self._CustomSetup_run_info = ['CustomSetup']
        except Exception as e:
            self._run_code_result = False
            self._erorr_code = 'CustomSetup'
            self._erorr_code_info = e

    def ConfigSetup(self):
        self.LogsCreat("ConfigSetup start...")
        try:
            self._ConfigSetup_run_info = ['ConfigSetup']
        except Exception as e:
            self._run_code_result = False
            self._erorr_code = 'ConfigSetup'
            self._erorr_code_info = e

    def HoudiniAppSetup(self):
        if self._run_code_result:
            self.LogsCreat("HoudiniAppSetup start...")
            try:                
                path_adict = {'codebase':self._code_base_path,'hfsbase':self._houdini_client_dir,'plugingbase':self._houdini_PLuing_dirt}
                path_adict['temp'] = self._task_folder
                self._HoudiniAppSetup_run_info = HoudiniUtil.SetHoudiniApp(self._hfs_version,path_adict)
            except Exception as e:
                self._run_code_result = False
                self._erorr_code = 'HoudiniUtil.SetHoudiniApp'
                self._erorr_code_info = e

    def HoudiniServerSetup(self):
        if self._run_code_result:
            self.LogsCreat("HoudiniServerSetup start...")
            try:
                servers="10.60.96.203"
                self._HoudiniServerSetup_run_info = HoudiniUtil.SetServer(self._hfs_version,servers)
            except Exception as e:
                self._run_code_result = False
                self._erorr_code = 'HoudiniUtil.SetServer'
                self._erorr_code_info = e


    def Function(self):
        # to Render 
        self.LogsCreat("HoudiniMain.Function start...")
        if not self.G_ACTION == "Render":
            self._Killapps.append("hython.exe")
            self._run_code_result = False
            self._erorr_code = 'HoudiniFunction process'
            self._erorr_code_info = "Only for render."            

        # cmds 
        softCmd=self._houdini_client_dir+"/"+self._hfs_version+"/bin/hython.exe"
        renderPy=r' %s/script/render.py '% self._code_base_path
        renderproject='-project "%s"' % self._hip_file
        renderrop=' -rop %s'%self._rop_node
        renderGPU=' -GPU 1'
        if self._render_frame == 1:
            frames="\""+str(self._frames[0])+" "+str(self._frames[1])+" "+str(self._frames[2])+"\""
        elif self._render_frame == 2:
            frames="\""+str(self._frames[0])+"\""
            # frames="\""+"1,3-7[3],15"+"\""
        renderFrame=' -frame %s' % frames
        renderout=' -outdir "%s"' % self._output
        renderHIP=' -HIP "%s"' % self._hip_save_val
        rendertask = ' -taskbase "%s"'%self._task_folder

        renderCmd=softCmd+renderPy+renderproject+renderrop+renderGPU+renderFrame+renderout+renderHIP+rendertask
        # self.LogsCreat("Cmds: %s"%renderCmd)

        self.LogsCreat("Houdini Function process start...")
        self.LogsCreat("...")
        self.LogsCreat(" ")
        self.LogsCreat("Loading Houdini software...")
        # Anacmdcode=subprocess.Popen(renderCmd,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        returncode,final_info = CLASS_COMMON_UTIL.cmd(renderCmd,None,1,True,True,self.FiltLog)


        if not returncode==0:
            self._Killapps.append("hython.exe")
            self._run_code_result = False
            self._erorr_code = 'HoudiniFunction process'
            self._erorr_code_info = final_info

        self.LogsCreat("[Finished.]",True,False)
        self.LogsCreat("RenderChildren return:"+str(returncode))

        self.LogsCreat("Function end.")


    def FiltLog(self,my_popen='',pid=''):
        while my_popen.poll()==None:
            info = my_popen.stdout.readline().strip()
            if info!='':
                torenderlog,todebug = (True,False) if "[HTS]" not in info.strip() else (False,True)
                self.LogsCreat(info,torenderlog,todebug)
  
    def Execute_Hfs(self):
        self.BaseDataSetup()
        if self._run_code_result:
            from HoudiniThread import HoudiniThread
            function_all = {"PluginsSetup":[self.PluginsSetup,''],'AssetSetup':[self.AssetSetup,''],
            'ConfigSetup':[self.ConfigSetup,''],'HoudiniAppSetup':[self.HoudiniAppSetup,''],
            "HoudiniServerSetup":[self.HoudiniServerSetup,'']}
            threads = HoudiniThread.StartThread(HoudiniThread.CreatThread(function_all))
            # HoudiniThread.JoinThread(threads)
        ## -----------------------------------------------------------
        ## ------------- wait to the threads to finish ---------------
            self.LogsCreat(" ")
            for thr in threads[0]:
                thrnmae = thr.name
                self.LogsCreat("%s information:"%thrnmae)
                self.LogsCreat("...")
                thr.join()
                try:
                    exec("info_list =self._%s_run_info"%thrnmae)
                    for info in info_list: self.LogsCreat(info)
                    self.LogsCreat("%s end.\n"%thrnmae)
                except Exception, e:
                    break
                
        sys.stdout.flush()
        time.sleep(1)

        if not self._run_code_result:
            self.LogsCreat('')
            self.LogsCreat("Eroor Information: %s"%self._erorr_code_info)
            self.LogsCreat("Eroor Called Code: %s"%self._erorr_code)
            self.LogsCreat('')
            self.LogsCreat('')


    '''
        Rebult 
    '''
    def RB_CONFIG(self):#4
        self.format_log('渲染配置','start')
        self.G_DEBUG_LOG.info('[BASE.RB_CONFIG.start.....]')

        ## setup Houdini software and plugins for analysis
        self.Execute_Hfs()

        if not self._run_code_result:
            self.LogsCreat("Errors calls,try to kill apps...")
            print(self._Killapps)
            if len(self._Killapps):
                mainapp = []
                self._Killapps.extend(mainapp)
                try:
                    CLASS_COMMON_UTIL.kill_app_list(self._Killapps)
                except:
                    pass
                self.G_DEBUG_LOG.info('[BASE.RB_RENDER.end.....]')
            CLASS_COMMON_UTIL.error_exit_log(self.G_DEBUG_LOG,"Execute_Hfs()",123)

        self.G_DEBUG_LOG.info('[BASE.RB_CONFIG.end.....]') 
        self.format_log('done','end')
        
    '''
        Rebult
    '''
    def RB_RENDER(self):#5
        self.format_log('渲染','start')
        self.G_DEBUG_LOG.info('[BASE.RB_RENDER.start.....]')

        self.Function()
        if not self._run_code_result:
            self.LogsCreat("Errors calls,try to kill apps...")
        else:
            self.LogsCreat("Job finished,try to kill apps...")
        if len(self._Killapps):
            mainapp = []
            self._Killapps.extend(mainapp)
            try:
                CLASS_COMMON_UTIL.kill_app_list(self._Killapps)
            except:
                pass
            self.LogsCreat("[kill apps done]")

        # if errors
        if not self._run_code_result:
            CLASS_COMMON_UTIL.error_exit_log(self.G_DEBUG_LOG,"Function()",456)

        self.G_DEBUG_LOG.info('[BASE.RB_RENDER.end.....]')
        self.format_log('done','end')