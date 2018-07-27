#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import os.path
import sys
import subprocess
#import _subprocess
import string
import logging
import time
import shutil
import codecs
import ConfigParser
import json
from RenderBase import RenderBase
class MayaPre(RenderBase):
    def __init__(self,**paramDict):
        RenderBase.__init__(self,**paramDict)

    def readRenderCfg(self):
        self.G_PROCESS_LOG.info('[maya.readRenderCfg.start.....]'+self.G_RENDER_WORK_TASK_CFG)
        renderCfg=os.path.join(self.G_RENDER_WORK_TASK_CFG,'render.cfg').replace('/','\\')
        print renderCfg
        self.RENDER_CFG_PARSER = ConfigParser.ConfigParser()
        
        try:
            self.G_PROCESS_LOG.info('read rendercfg by utf16')
            self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r", "UTF-16"))
            
        except Exception, e:
            self.G_PROCESS_LOG.info(e)
            try:
                self.G_PROCESS_LOG.info('read rendercfg by  utf8')
                self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r", "UTF-8"))
                
            except Exception, e:
                self.G_PROCESS_LOG.info(e)
                self.RENDER_CFG_PARSER.readfp(codecs.open(renderCfg, "r"))
                self.G_PROCESS_LOG.info('read rendercfg by default')
        #self.RENDER_CFG_PARSER.read(renderCfg)
        
        self.G_PROCESS_LOG.info('[maya.readRenderCfg.end.....]')

    def getPackFile(self):
        if self.RENDER_CFG_PARSER.has_option('common','cgFile'):
            self.packFile=self.RENDER_CFG_PARSER.get('common','render_file').replace("/","\\")
            self.cgFileName=os.path.basename(self.RENDER_CFG_PARSER.get('common','cgFile'))
            self.cgFilePath=os.path.dirname(self.packFile)
            self.cgFile=os.path.join(self.cgFilePath,self.cgFileName)
            self.G_PROCESS_LOG.info('[maya.readRenderCfg.end.....]')

    def mountFrom(self):
        mountFrom=self.RENDER_CFG_PARSER.get('common','mountFrom')
        s=eval(mountFrom)
        projectPath = self.G_PATH_INPUTPROJECT[0:self.G_PATH_INPUTPROJECT.index(self.G_USERID_PARENT)-1]
        for key in s.keys():
            if not os.path.exists(s[key]):
                # cmd='net use '+s[key]+' '+projectPath.replace('/','\\')+key.replace('/','\\')
                mnt_value = projectPath.replace('/','\\') + key.replace('/','\\')
                if os.path.exists(mnt_value):
                    cmd='net use '+s[key]+' "'+mnt_value+'"'
                    self.G_PROCESS_LOG.info(cmd)
                    self.RBTry3cmd(cmd)
                else:
                    self.G_PROCESS_LOG.info('[warn]The path is not exist:%s' % mnt_value)

    def RBrender(self):#7
        self.G_PROCESS_LOG.info('[MayaPre.RBrender.start.....]')
        filePath = ""
        result = 0
        self.exe = "C:\\7-Zip\\7z.exe"
        if not os.path.exists("C:\\7-Zip"):
            self.exe = "C:\\Program Files\\7-Zip\\7z.exe"
        self.G_PROCESS_LOG.info('[MayaPre.file.....]'+self.packFile)
        if self.packFile.endswith(".ma") or self.packFile.endswith(".mb"):
            sys.exit(0)
        if os.path.exists(self.cgFile):
            result = self.is_same(self.packFile,self.cgFile)
        if result==0:
            unpackCmd=self.exe +' e "'+self.packFile+'" -o"'+self.cgFilePath+'" -y'    

            self.RBTry3cmd(unpackCmd,False,False)
        else:
            self.G_PROCESS_LOG.info('[fileExist.....]')

        self.G_PROCESS_LOG.info('[MayaPre.RBrender.end.....]')

    def run_command(self,cmd,count=4):
        count=count-1
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, startupinfo=startupinfo)

        while 1:
            #returns None while subprocess is running
            return_code = p.poll()
            if return_code == 0:
                break
            # elif return_code == 1:
            #     raise Exception(cmd + " was terminated for some reason.")
            elif return_code != None:
                if count>0:
                    time.sleep(1)
                    self.run_command(cmd,count)
                print "exit return code is: " + str(return_code)
                break
                # raise Exception(cmd + " was crashed for some reason.")
            line = p.stdout.readline()
            yield line

    def get_zip_info(self, zip_file):
        {'Attributes': 'A',
        'Block': '0',
        'Blocks': '1',
        'CRC': '836CB95D',
        'Encrypted': '-',
        'Headers Size': '138',
        'Method': 'LZMA2:20',
        'Modified': '2015-03-28 15:59:26',
        'Packed Size': '29191866',
        'Path': 'M02_P04_S046.mb',
        'Physical Size': '29192004',
        'Size': '138382876',
        'Solid': '-',
        'Type': '7z'}

        cmd = "\"%s\" l -slt \"%s\"" % (self.exe, zip_file)
        print cmd
        result = {}
        for line in self.run_command(cmd):
            if "=" in line:
                line_split = [i.strip() for i in line.strip().split("=")]
                result[line_split[0]] = line_split[1]

        return result

    def is_same(self, zip_file, src):
        if os.path.exists(zip_file) and os.path.exists(src):
            zip_info = self.get_zip_info(zip_file)
            z_time = zip_info["Modified"]
            z_size = zip_info["Size"]

            f_time = time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(os.path.getmtime(src)))
            f_size = str(os.path.getsize(src))

            print str(f_time)+"----"+str(f_size)+"---"+str(z_time)+"----"+str(z_size)
            if z_time == f_time and z_size == f_size:
                print "-----"
                return 1
            else:
                return 0
    
    def waitting(self):
        self.G_PROCESS_LOG.info('waitting---start')
        # time.sleep(60)
        self.G_PROCESS_LOG.info('waitting---end')

    def cfg_to_json(self):
        """
        The requirement from yuanli for linux rendering that submit from the windows client
        render.cfg, py.cfg, plugin.cfg  -->  render.json, plugins.json
        The script is executed in the windows environment
        """
        self.G_PROCESS_LOG.info('[MayaPre.cfg_to_json.start.....]')
        json_list = []
        
        local_render_json_path = self.generate_render_json()
        local_plugins_json_path = self.generate_plugins_json()
        
        json_list.append(local_render_json_path)
        json_list.append(local_plugins_json_path)
        
        self.copy_json_to_server(json_list)
        self.G_PROCESS_LOG.info('[MayaPre.cfg_to_json.end.....]')
        
    def generate_render_json(self):
        """
        render.cfg, py.cfg, server.cfg --> render.json
        """
        if not os.path.exists(self.G_RENDER_WORK_TASK_CFG):
            os.makedirs(self.G_RENDER_WORK_TASK_CFG)
        render_json_path = os.path.join(self.G_RENDER_WORK_TASK_CFG, 'render.json')
        
        server_info = eval(open(os.path.join(self.G_RENDER_WORK_TASK_CFG, "server.cfg")).read())
        
        render_json_dict = {}
        common_dict = {}
        mntMap_dict = {}
        renderSettings_dict = {}
        
        # common
        common_dict['renderType'] = self.G_RENDERTYPE
        common_dict['multiPass'] = ''
        common_dict['outputLabel'] = self.G_OUTPUT_LABEL
        common_dict['cgv'] = str(server_info['maya_version'])
        common_dict['iformat'] = ''
        common_dict['cgSoftName'] = self.RENDER_CFG_PARSER.get('common','cgSoftName')
        common_dict['projectId'] = self.RENDER_CFG_PARSER.get('common','projectId')
        common_dict['costPath'] = self.G_PATH_COST
        common_dict['smallPath'] = self.G_PATH_SMALL
        common_dict['userOutputPath'] = self.G_PATH_USER_OUTPUT
        common_dict['inputCgFile'] = '{}{}'.format(self.G_PATH_INPUTPROJECT, self.G_PATH_INPUTFILE).replace('\\', '/')
        common_dict['userId'] = str(server_info['user_id'])
        common_dict['taskId'] = self.RENDER_CFG_PARSER.get('common','taskId')
        common_dict['submitFrom'] = 'api'
        common_dict['imageHeight'] = self.RENDER_CFG_PARSER.get('renderSettings','height')
        common_dict['denoise'] = '0'
        common_dict['renderModel'] = '1'
        common_dict['singelFrameCheck'] = self.G_SINGLE_FRAME_CHECK
        common_dict['analyseTxt'] = ''
        common_dict['outputFileName'] = ''
        common_dict['inputUserPath'] = self.G_PATH_INPUTPROJECT
        common_dict['inputFile'] = '{}{}'.format(self.G_PATH_INPUTPROJECT, self.G_PATH_INPUTFILE).replace('\\', '/')
        common_dict['cgFile'] = self.RENDER_CFG_PARSER.get('common','render_file')
        common_dict['noOutput'] = '0'
        common_dict['cgVersion'] = str(server_info['maya_version'])
        common_dict['projectSymbol'] = self.RENDER_CFG_PARSER.get('common','projectSymbol')
        common_dict['imageWidth'] = self.RENDER_CFG_PARSER.get('renderSettings','width')
        common_dict['zone'] = self.G_ZONE
        common_dict['inputProject'] = self.G_PATH_INPUTPROJECT
        common_dict['tilesPath'] = self.G_PATH_TILES
        
        # mntMap
        for key, value in server_info['mounts'].items():
            mntMap_dict[key] = '{}{}'.format(self.G_PATH_INPUTPROJECT, value).replace('\\', '/')
        mntMap_dict['/B'] = self.PLUGINPATH.replace('\\', '/')
        
        # renderSettings
        renderSettings_dict['renderType'] = 'render'
        renderSettings_dict['renderableLayer'] = self.RENDER_CFG_PARSER.get('renderSettings','renderableLayer')
        renderSettings_dict['renderableCamera'] = self.RENDER_CFG_PARSER.get('renderSettings','renderableCamera')
        renderSettings_dict['projectPath'] =  server_info['project'] if server_info['project'] is not None else ''
        renderSettings_dict['width'] = self.RENDER_CFG_PARSER.get('renderSettings','width')
        renderSettings_dict['height'] = self.RENDER_CFG_PARSER.get('renderSettings','height')
        
        
        render_json_dict['pluginPathList'] = self.PLUGINPATHLIST  # py.cfg
        render_json_dict['customize'] = ''
        render_json_dict['common'] = common_dict
        render_json_dict['mntMap'] = mntMap_dict
        render_json_dict['mappings'] = server_info['mappings']
        render_json_dict['renderSettings'] = renderSettings_dict
        
        with codecs.open(render_json_path, 'w', 'utf-8') as render_json_obj:
            json.dump(render_json_dict, render_json_obj, ensure_ascii=False, indent=4)
            
        return render_json_path
        
        
        
    def generate_plugins_json(self):
        """
        plugin.cfg --> plugins.json
        """
        if not os.path.exists(self.G_RENDER_WORK_TASK_CFG):
            os.makedirs(self.G_RENDER_WORK_TASK_CFG)
        plugins_json_path = os.path.join(self.G_RENDER_WORK_TASK_CFG, 'plugins.json')
        plugin_cfg_dict = self.RBgetPluginDict()
        
        with codecs.open(plugins_json_path, 'w', 'utf-8') as plugins_json_obj:
            json.dump(plugin_cfg_dict, plugins_json_obj, ensure_ascii=False, indent=4)
            
        return plugins_json_path
        
        
    def copy_json_to_server(self, json_list):
        """
        Copy json files to server path.
        """
        json_dict = dict.fromkeys(json_list, True)  # performance optimization
        copy_exe = r'c:\fcopy\FastCopy.exe'
        server_dir = os.path.join(self.G_POOL, 'config', self.G_USERID_PARENT, self.G_USERID, self.G_TASKID)
        
        if not os.path.exists(server_dir):
            try:
                os.makedirs(server_dir)  # Multiple tasks at the same time creating the directory may be wrong
            except Exception as e:
                self.G_PROCESS_LOG.info(e)
                if not os.path.exists(server_dir):
                    os.makedirs(server_dir)
        
        for json_file in json_dict:
            copy_cmd = r'{exe} /cmd=force_copy /speed=full /force_close /no_confirm_stop /force_start "{src}" /to="{dest}"'.format(
                exe=copy_exe,
                src=json_file.replace('/', '\\'),
                dest=server_dir.replace('/', '\\'),
            )
            self.RBcmd(copy_cmd, myLog=True)
    
        
    def RBexecute(self):#Render
        #self.RBBackupPy()
        self.RBinitLog()
        self.G_RENDER_LOG.info('[MayaPre.RBexecute.start.....]')
        
        self.RBprePy()
        self.RBcopyTempFile()  # copy cfg

        self.RBreadCfg()  # read py.cfg
        #self.RBhanFile()
        self.RBrenderConfig()  # empty
        self.readRenderCfg()  # read render.cfg
        self.delNetUse()
        # self.mountFrom()  # net use
        # self.waitting()
        # self.getPackFile()
        self.cfg_to_json()
        # self.RBrender()
        

        #self.RBresultAction()
        #self.RBpostPy()
        self.G_RENDER_LOG.info('[MayaPre.RBexecute.end.....]')