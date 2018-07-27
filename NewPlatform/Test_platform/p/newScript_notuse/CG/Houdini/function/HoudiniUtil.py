#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import os,sys,time,re
import subprocess
import socket
import shutil
import platform
import re


class HoudiniUtil():

    
    @classmethod
    def SysTemInfo(cls):
        this_hostname = socket.gethostname()
        this_plant = sys.platform
        this_ip_end = re.findall(r"\d+",this_hostname)
        _ip_a = this_ip_end[0]
        z_num = 0
        for i in range(0,len(_ip_a)):
            if not _ip_a[i]=="0":
                z_num=i
                break
        _ip_a =_ip_a[z_num:]
        this_ipList = socket.gethostbyname_ex(this_hostname)
        this_ip = ''
        for elm in this_ipList[-1]:
            _ip_ss = elm.split(".")
            if _ip_a in _ip_ss:
                this_ip = elm
                break
        return this_plant,this_hostname,this_ip


    @classmethod
    def CustomSetup(cls,cls_in=''):
        cls_in.LogsCreat("CustomSetup start...")
        try:
            cls_in._CustomSetup_run_info = ['CustomSetup']
        except Exception as e:
            cls_in._run_code_result = False
            cls_in._erorr_code = 'CustomSetup'
            cls_in._erorr_code_info = e


    @classmethod
    def PluginsSetup(cls,cls_in=''):
        cls_in.LogsCreat("PluginsSetup start...")
        try:
            returninfo = cls.SetRenderer(cls_in._hfs_version,cls_in._plugins,cls_in._houdini_PLuing_dirt,cls_in._plugins_surpose)
            cls_in._PluginsSetup_run_info = returninfo["info"]
            cls_in._Killapps.extend(returninfo["app"])
        except Exception as e:
            cls_in._run_code_result = False
            cls_in._erorr_code = 'HoudiniUtil.SetRenderer'
            cls_in._erorr_code_info = e


    @staticmethod
    def SetRenderer(houdiniversion='',plugin_adict={},plugins_dirt='',plugins_surpose=[]):

        if len(plugin_adict):
            _plugin_dirt = '%s/plugins'%plugins_dirt
            sys.path.append(_plugin_dirt)
            for key in plugin_adict:
                if key in plugins_surpose: # surpose
                    import Script
                    if os.path.exists('%s/Script/%s/%s_set.py'%(_plugin_dirt,key,key)):
                        hfs_ver = houdiniversion[:2]+"."+houdiniversion[2:3]+"."+houdiniversion[3:]
                        cmds_py = 'GetIfon = Script.%s.%s_set.SET_ENV(hfs_ver,plugin_adict[key])'%(key,key)
                        
                        exec(cmds_py)
                        return GetIfon


    @classmethod
    def HoudiniAppSetup(cls,cls_in=''):
        return
        if cls_in._run_code_result:
            cls_in.LogsCreat("HoudiniAppSetup start...")
            try:                
                path_adict = {'codebase':cls_in._code_base_path,'hfsbase':cls_in._houdini_client_dir,'plugingbase':cls_in._houdini_PLuing_dirt}
                path_adict['temp'] = '%s/temp'%cls_in._task_folder
                cls_in._HoudiniAppSetup_run_info = cls.SetHoudiniApp(cls_in._hfs_version,path_adict)
            except Exception as e:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'HoudiniUtil.SetHoudiniApp'
                cls_in._erorr_code_info = e


    @classmethod
    def SetHoudiniApp(cls,hfs_version='160600',path_adict={}):
        ## path_adict= {'codebase':'C:/script/CG/Houdini','hfsbase':'D:/plugins/houdini',
        ##              'plugingase':'B:/plugins/houdini','temp':'C:/work/render'}
        returncode = []
        plantfrom = platform.system()
        if plantfrom == "Windows":
            returncode = cls.SetHoudiniApp_win(hfs_version,path_adict)
        elif plantfrom == "Linux":
            returncode = cls.SetHoudiniApp_Linux(hfs_version,path_adict)
        return returncode

       
    @staticmethod
    def SetHoudiniApp_win(hfs_version='160600',path_adict={}):
        houdini_plugin_path = path_adict['plugingbase']       
        houdini_client_dir = path_adict['hfsbase']
        houdini_version = hfs_version
        temp_path = path_adict['temp']
        zip_tool = r'C:\7-Zip\7z.exe'
        ToCopyHfs = True
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)

        h_source = os.path.abspath("%s/apps/win/%s.7z"%(houdini_plugin_path,houdini_version))
        houdini_app_path_zip = os.path.abspath("%s/%s.7z"%(houdini_client_dir,houdini_version))
        if os.path.exists(houdini_app_path_zip):
            ToCopyHfs = False
        
        ## unzip houdini 
        cmd_un7z = zip_tool + " x -y -aos "
        cmd_un7z += "%s/%s.7z"%(houdini_client_dir,houdini_version) # D:/plugins/houdini
        cmd_un7z += " -o%s" % ("%s/%s"%(houdini_client_dir,houdini_version))        
        
        ## subprocess
        Uzi_Houdini_log = open(r'%s/Uzip_Houdini.txt'%temp_path,'wt')     
        if ToCopyHfs:
            copyhoudini = subprocess.Popen("copy %s %s" % (h_source, h_amd),shell=True)
            copyhoudini.wait()

        UzipHoudini = subprocess.Popen(cmd_un7z,stdout=Uzi_Houdini_log,shell=True)
        UzipHoudini.wait()

        # finish,close the handl
        Uzi_Houdini_log.close()
        _h_result = UzipHoudini.returncode

        if not _h_result:
            print("Houdini setup finished. ")
            return ["Houdini%s setup finished. "%houdini_version]
        else:
            return ["Faild!"]

    @staticmethod
    def SetHoudiniApp_Linux(hfs_version='160600',path_adict={}):
        pass

    @classmethod
    def HoudiniServerSetup(cls,cls_in=''):
        return
        if cls_in._run_code_result:
            cls_in.LogsCreat("HoudiniServerSetup start...")
            try:
                servers="10.60.96.203"
                cls_in._HoudiniServerSetup_run_info = HoudiniUtil.SetServer(cls_in._hfs_version,servers)
            except Exception as e:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'HoudiniUtil.SetServer'
                cls_in._erorr_code_info = e

    @classmethod
    def SetServer(cls,houdini_vis='',HS_ip=''):
        returncode = []
        hfs_version = houdini_vis[:2]
        plantfrom = platform.system()
        if plantfrom == "Windows":
            try_code = True
            cunt = 0
            while try_code:
                try:
                    returncode = cls.SetServer_win(hfs_version,HS_ip)
                    cunt =3 if returncode[0]==0 else cunt+1
                except Exception as e:
                    cunt +=1
                    returncode.append(e)
                if cunt>=3:
                    try_code = False

        elif plantfrom == "Linux":
            try_code = True
            cunt = 0
            while try_code:
                try:
                    returncode = cls.SetServer_Linux(hfs_version,HS_ip)
                    cunt =3 if returncode[0]==0 else cunt+1

                except Exception as e:
                    cunt +=1
                    returncode.append(e)
                if cunt>=3:
                    try_code = False

        return returncode

    @staticmethod
    def SetServer_win(houdini_vis='',HS_ip=''):
        not_install = "The specified service does not exist as an installed service"
        to_install = False
        not_start = "The service has not been started"
        sc = r'C:\Windows\System32\sc.exe'
        findstr = r'C:\Windows\System32\findstr.exe'

        # os.environ['PATH'] = os.environ.get('PATH') + r';C:\Windows\System32'

        print("HoudiniLicenseServer stop...")
        HLS_stop_cmd = '%s stop "HoudiniLicenseServer"'%sc
        HLS_popen = subprocess.Popen(HLS_stop_cmd, stdout=subprocess.PIPE, shell=1)
        HLS_popen.wait()
        HLS = HLS_popen.stdout.readlines()
        for elm in HLS:
            if not_install in elm.strip():
                to_install = True
                print not_install
            elif not_start in elm.strip():
                print not_start

        print("HoudiniServer stop...")
        HS_stop_cmd = '%s stop "HoudiniServer"'%sc
        HS_popen = subprocess.Popen(HLS_stop_cmd, stdout=subprocess.PIPE, shell=1)
        HS_popen.wait()
        HS = HS_popen.stdout.readlines()
        for elm in HLS:
            if not_install in elm.strip():
                to_install = True
                print not_install
            elif not_start in elm.strip():
                print not_start


        ## ctreat server
        # HoudiniLicenseServer
        print("HoudiniLicenseServer rebult...")
        HLS_src = os.path.join(r"b:\plugins\houdini\lic", houdini_vis, "sesinetd.exe")
        HLS_dst = os.path.join("C:\Windows\System32", "sesinetd.exe")    
        # HLS_creat_cmd = "sc create HoudiniLicenseServer binPath= " + HLS_dst + " START= auto " + " DISPLAYNAME= HoudiniLicenseServer " + " TYPE= own "
        HLS_creat_cmd = "%s create HoudiniLicenseServer binPath= C:\Windows\System32\sesinetd.exe START= auto DISPLAYNAME= HoudiniLicenseServer TYPE= own"%sc
        shutil.copy(HLS_src, HLS_dst)
        creat_popen = subprocess.Popen(HLS_creat_cmd, stdout=subprocess.PIPE, shell=1)
        creat_popen.wait()
        time.sleep(5)

        # HoudiniServer
        print("HoudiniServer rebult...")
        HS_src = os.path.join(r"b:\plugins\houdini\lic", houdini_vis, "hserver.exe")
        HS_dst = os.path.join("C:\Windows\System32", "hserver.exe")
        # HS_creat_cmd = "sc create HoudiniServer binPath= " + HS_dst + " START= auto " + " DISPLAYNAME= HoudiniServer " + " TYPE= own "
        HS_creat_cmd = "C:\Windows\System32\sc.exe create HoudiniLicenseServer binPath= C:\Windows\System32\hserver.exe START= auto DISPLAYNAME= HoudiniServer TYPE= own"
        creat_popen = subprocess.Popen(HS_creat_cmd, stdout=subprocess.PIPE, shell=1)
        creat_popen.wait()
        time.sleep(5)

        ## check the server whether installed
        # HoudiniLicenseServer
        print("HoudiniLicenseServer check install...")
        checkcmd = 'C:\Windows\System32\sc.exe query HoudiniLicenseServer|%s "STATE"'%findstr
        check_popen = subprocess.Popen(checkcmd, stdout=subprocess.PIPE, shell=1)
        check_popen.wait()
        check_info = check_popen.stdout.readlines()
        for elm in check_info:
            if "STOPPED" in elm.strip():
                to_install = False
                print elm.strip()
        # HoudiniServer
        print("HoudiniServer check install...")
        checkcmd = 'C:\Windows\System32\sc.exe query HoudiniServer|%s "STATE"'%findstr
        check_popen = subprocess.Popen(checkcmd, stdout=subprocess.PIPE, shell=1)
        check_popen.wait()    
        check_info = check_popen.stdout.readlines()
        for elm in check_info:
            if "STOPPED" in elm.strip():
                to_install = False
                print elm.strip()

        ## start sever
        if to_install==False:
            predone = 0
            print("HoudiniLicenseServer start...")
            start_cmd = 'C:\Windows\System32\sc.exe start "HoudiniLicenseServer"'
            start_popen = subprocess.Popen(start_cmd, stdout=subprocess.PIPE, shell=1)
            start_popen.wait()
            time.sleep(5)

            print("HoudiniServer start...")
            start_cmd = 'C:\Windows\System32\sc.exe start "HoudiniServer"'
            start_popen = subprocess.Popen(start_cmd, stdout=subprocess.PIPE, shell=1)
            start_popen.wait()
            time.sleep(5)
            
            ## check the state
            print("HoudiniLicenseServer check...")
            checkcmd = 'C:\Windows\System32\sc.exe query HoudiniLicenseServer|%s "STATE"'%findstr
            check_popen = subprocess.Popen(checkcmd, stdout=subprocess.PIPE, shell=1)
            check_popen.wait()
            check_info = check_popen.stdout.readlines()
            for elm in check_info:
                if "RUNNING" in elm.strip():
                    predone +=1
                    print elm.strip()

            print("HoudiniServer check...")
            checkcmd = 'C:\Windows\System32\sc.exe query HoudiniServer|%s "STATE"'%findstr
            check_popen = subprocess.Popen(checkcmd, stdout=subprocess.PIPE, shell=1)
            check_popen.wait()
            check_info = check_popen.stdout.readlines()
            for elm in check_info:
                if "RUNNING" in elm.strip():
                    predone +=1
                    print elm.strip()

            if predone >=2:
                ## change license
                change_ip_cmd = HS_dst + " -S " + HS_ip
                change_popen = subprocess.Popen(change_ip_cmd, stdout=subprocess.PIPE, shell=1)
                change_popen.wait()
                time.sleep(5)
                change_info=change_popen.stdout.readlines()
                returninfo = ''
                for elm in change_info:
                    print elm.strip()
                    if "changed to " in elm.strip():
                        returninfo = elm.strip()

        print("Server setup finished.")
        return [0,returninfo]

    @staticmethod
    def SetServer_Linux(houdini_vis='',HS_ip=''):
        pass


    @classmethod
    def AssetSetup(cls,cls_in=''):
        cls_in.LogsCreat("AssetSetup start...")
        try:
            cls_in._AssetSetup_run_info = ['AssetSetup']
        except Exception as e:
            cls_in._run_code_result = False
            cls_in._erorr_code = 'AssetSetup'
            cls_in._erorr_code_info = e


    @classmethod
    def print_times(cls,info="",file="",type=""):
        time_point=time.strftime("%b_%d_%Y %H:%M:%S", time.localtime())
        addpoint = "HTS"
        infos = "["+str(addpoint) + "] " + str(info)
        print (infos)

        if type=="w":
            if not os.path.exists(file):
                if not os.path.exists(os.path.dirname(file)):
                    os.makedirs(os.path.dirname(file))
                with open(file,"w") as f:
                    f.close()
            else:
                with open(file,"a") as f:
                    f.write(infos)
                    f.close()

    @classmethod
    def GetSaveHipInfo(cls,hipfile='',_app_path=''):
        with open(hipfile, 'rb') as src:
            Not_find = True
            search_elm = 2
            search_elm_cunt = 0
            while Not_find:
                line = src.readline()
                # Save version 
                if re.match('^set -g _HIP_SAVEVERSION = ', line):                    
                    _HV = re.search("\'.*\'", line).group()[1:-1]
                    _VS = _HV.split('.')
                    _hfs_save_version = int(_VS[0] + _VS[1] + _VS[2])
                    search_elm_cunt += 1

                # The $HIP val with this file saved
                if re.match('^set -g HIP = ', line):                    
                    _Hip = re.search("\'.*\'", line).group()[1:-1]
                    _hip_save_val = _Hip.replace("\\","/")
                    search_elm_cunt += 1
                if search_elm_cunt >= search_elm:
                    Not_find = False
        
        # get the bast version for running
        if not  Not_find:
            _files_name = []
            _ver_list = []            
            for (dirpath, dirnames, filenames) in os.walk(_app_path):
                _files_name.extend(filenames)
            if len(_files_name):
                for elm in _files_name:
                    ver = elm.split(".7z")[0] if ".7z" in elm else ''
                    try:
                        _ver_list.append(int(ver))
                    except:
                        pass

 
            if len(_ver_list):
                _ver_list = sorted(_ver_list)
                mid = len(_ver_list)
                if int(_hfs_save_version)>=_ver_list[mid/2]:
                    min_ver = _ver_list[mid/2]
                    max_ver = _ver_list[mid-1]
                    much_ver = 0
                    get_ver = 0
                    if int(_hfs_save_version)<max_ver:
                        for i in xrange(mid/2,len(_ver_list)):
                            if int(_hfs_save_version)==_ver_list[i]:
                                get_ver = _ver_list[i]
                                break
                            elif int(_hfs_save_version)>_ver_list[i]:
                                min_ver = _ver_list[i]
                            elif int(_hfs_save_version)<_ver_list[i] and much_ver==0:
                                much_ver = _ver_list[i]
                        _hfs_version = get_ver if get_ver else much_ver
                    else:
                        _hfs_version = max_ver
                else:
                    min_ver = _ver_list[0]
                    max_ver = _ver_list[(mid/2)-1]
                    much_ver = 0
                    get_ver = 0
                    if int(_save_version)<max_ver:
                        for i in xrange(0,mid/2):
                            if int(_save_version)==_ver_list[i]:
                                get_ver = _ver_list[i]
                                break
                            elif int(_save_version)>_ver_list[i]:
                                min_ver = _ver_list[i]
                            elif int(_save_version)<_ver_list[i] and much_ver==0:
                                much_ver = _ver_list[i]
                        _hfs_version = get_ver if get_ver else much_ver
                    else:
                        _hfs_version = max_ver
                _hfs_version = str(_hfs_version)

                return [_hfs_save_version,_hfs_version,_hip_save_val]

            else:
                _erorr_code_info = 'The app folder is emplty.'
                return [_erorr_code_info]
        else:
            _erorr_code_info = 'Bad hip file.'
            return [_erorr_code_info]


    @classmethod
    def KillApps(cls,Killapps=[],platform='win'):
        for app in Killapps:
            if not platform=='Linux':
                cmds = r'c:\windows\system32\cmd.exe /c c:\windows\system32\TASKKILL.exe /F /IM %s'%app
            elif platform=='Linux':
                cmds = ''
            subprocess.call(cmds,shell=True)

    @classmethod
    def SequenceCheck(cls,cls_in='',dirs='',file='',nodepath='',keyw="files"):

        if not file=="":
            in_adict,to_check,infos = cls.check_adict(dirs,file,cls_in.foler_adict)
            print in_adict,"00000000000000000000000000000000000000000"
            if in_adict:
                '''
                If folder dirt in the adict of this folder,try to find whether the file in it,
                if in it and had checked onece,passed 
                '''
                if to_check:
                    is_sequence,sequence_adict,dif_list = cls.issequence(dirs,file,infos)
                elif infos==False:
                    is_sequence=2
                    sequence_adict = file
                    dif_list = []
                elif infos==True:
                    is_sequence=1
                    dif_list = []

            else:
                is_sequence,sequence_adict,dif_list = cls.issequence(dirs,file)
            if is_sequence==0:
                ## exist , is sequence
                """
                sequence_adict:
                {"abc":[["abc.0001","abc.0002"..."abc.0010"],1,10,4,abc.$F3.exr]}
                """
                full_path = os.path.join(dirs,sequence_adict[sequence_adict.keys()[0]][4]).replace("\\","/")
                temp_list_n = [full_path,[sequence_adict[sequence_adict.keys()[0]][1],
                            sequence_adict[sequence_adict.keys()[0]][2]]]
                if "Normal" in cls_in.asset_adict:
                    ## {"Normal":{"file":{"nodepath":[filepath,[files]]} } }
                    if keyw in cls_in.asset_adict["Normal"]:
                        if not nodepath in cls_in.asset_adict["Normal"][keyw]:
                            copy_adict = cls_in.asset_adict["Normal"][keyw]  
                            copy_adict[nodepath] = temp_list_n
                            cls_in.asset_adict["Normal"][keyw] = copy_adict
                    else:
                        copy_adict = {nodepath:temp_list_n}
                        cls_in.asset_adict["Normal"][keyw] = copy_adict
                else:
                    copy_adict ={keyw:{nodepath:temp_list_n}}
                    cls_in.asset_adict["Normal"] = copy_adict

            ## ------------------------------------------------------------------------------
                """  get the miss files in sequence   """
                miss_adict,file_miss_adict = cls.getmiss_elm(sequence_adict)
                ## folder_adict
                if len(file_miss_adict):
                    if dirs in cls_in.foler_adict:
                        if "sequences" in cls_in.foler_adict[dirs]:
                            copy_adict = cls_in.foler_adict[dirs]["sequences"]
                            dictMerged=dict(copy_adict.items()+file_miss_adict.items())
                            cls_in.foler_adict[dirs]["sequences"]=dictMerged
                        else:
                            copy_adict = cls_in.foler_adict[dirs]
                            cls_in.foler_adict[dirs]["sequences"]=file_miss_adict
                    else:
                        copy_adict ={"sequences":file_miss_adict}
                        cls_in.foler_adict[dirs]=copy_adict
                
                ### information for the miss file adict
                if len(miss_adict):

                    full_path = os.path.join(dirs,miss_adict.keys()[0]).replace("\\","/")
                    temp_list_m = [full_path,miss_adict[miss_adict.keys()[0]]]

                    if "Miss" in cls_in.asset_adict:
                        ## {"Miss":{"file":{"nodepath":[filepath,[files]]} } }
                        if keyw in cls_in.asset_adict["Miss"]:
                            if not nodepath in cls_in.asset_adict["Miss"][keyw]:
                                copy_adict = cls_in.asset_adict["Miss"][keyw]  
                                copy_adict[nodepath] = temp_list_m
                                cls_in.asset_adict["Miss"][keyw] = copy_adict
                        else:
                            copy_adict = {nodepath:temp_list_m}
                            cls_in.asset_adict["Miss"][keyw] = copy_adict
                    else:
                        copy_adict ={keyw:{nodepath:temp_list_m}}
                        cls_in.asset_adict["Miss"] = copy_adict

            elif is_sequence==1:
                ## exist ,not sequence
                file=sequence_adict
                ## foler_adict
                if dirs in cls_in.foler_adict:
                    if "singles" in cls_in.foler_adict[dirs]:
                        copy_list = cls_in.foler_adict[dirs]["singles"]
                        if file not in copy_list:
                            copy_list_new = copy_list.append(file)
                            cls_in.foler_adict[dirs]["singles"]=copy_list_new
                    else:
                        copy_list = [file]
                        cls_in.foler_adict[dirs]["singles"]=copy_list
                else:
                    copy_list ={"singles":[file]}
                    cls_in.foler_adict[dirs]=copy_list

                ## asset_adict
                if "Normal" in cls_in.asset_adict:
                    if keyw in cls_in.asset_adict["Normal"]:
                        if not nodepath in cls_in.asset_adict["Normal"][keyw]:
                            copy_adict = cls_in.asset_adict["Normal"][keyw]  
                            copy_adict[nodepath] = [file]
                            cls_in.asset_adict["Normal"][keyw] = copy_adict
                    else:
                        copy_adict = {nodepath:[file]}
                        cls_in.asset_adict["Normal"][keyw] = copy_adict
                else:
                    copy_adict ={keyw:{nodepath:[file]}}
                    cls_in.asset_adict["Normal"] = copy_adict
                # print(info)

            elif is_sequence==2:
                ## not exist,single file
                file=sequence_adict
                if dirs in cls_in.foler_adict:
                    if "miss" in cls_in.foler_adict[dirs]:
                        copy_list = cls_in.foler_adict[dirs]["miss"]
                        cls_in.foler_adict[dirs]["miss"]=copy_list.append(file)
                    else:
                        copy_list = [file]
                        cls_in.foler_adict[dirs]["miss"]=copy_list
                else:
                    copy_list ={"miss":[file]}
                    cls_in.foler_adict[dirs]=copy_list

                ## asset_adict
                if "Miss" in cls_in.asset_adict:
                    ## {"Miss":{"file":{"nodepath":[filepath,[files]]} } }
                    if keyw in cls_in.asset_adict["Miss"]:
                        if not nodepath in cls_in.asset_adict["Miss"][keyw]:
                            copy_adict = cls_in.asset_adict["Miss"][keyw]  
                            copy_adict[nodepath] = [file]
                            cls_in.asset_adict["Miss"][keyw] = copy_adict
                    else:
                        copy_adict = {nodepath:[file]}
                        cls_in.asset_adict["Miss"][keyw] = copy_adict
                else:
                    copy_adict ={keyw:{nodepath:[file]}}
                    cls_in.asset_adict["Miss"] = copy_adict


            elif is_sequence==3:
                pass
            if len(dif_list):
                
                if not in_adict:
                    reset_adict = cls.GetBadFile(dif_list)
                else:
                    reset_adict=[{},dif_list]

                """  bad file in this folder """
                if len(reset_adict[0]):
                    if dirs in cls_in.foler_adict:
                        cls_in.foler_adict[dirs]["badfiles"]=reset_adict[0]
                    else:
                        copy_adict ={"badfiles":reset_adict[0]}
                        cls_in.foler_adict[dirs]=copy_adict
                    # print("-"*50)
                    # print("Bad file in : %s"%dirs)
                    # print(str(reset_adict[0]))
                    # print("-"*50)

                """  other file in this folder  """
                if len(reset_adict[1]):
                    if dirs in cls_in.foler_adict:
                        cls_in.foler_adict[dirs]["others"]=reset_adict[1]
                    else:
                        copy_adict ={"others":reset_adict[1]}
                        cls_in.foler_adict[dirs]=copy_adict
                    # print(reset_adict[1])
        else:
            """ Get all the sequence in this folder """
            pass

    @classmethod
    def issequence(cls,dirt='',filename='',adict_in={}):
        is_sequence = 1
        if filename != "":
            sequence_adict={}
            maby_sequence = True
            dif_list = []
            maby_sequence,split_str,num = cls.getnumber(filename)
            All_files = os.listdir(dirt) if not len(adict_in)else adict_in
            if maby_sequence:
                sequence_list = []
                for elm in All_files:
                    filename_list=filename.split(split_str)
                    if filename_list[0] in elm:
                        split_str_elm = cls.getnumber(elm)[1]
                        elm_split = elm.split(split_str_elm)
                        if elm_split[0]==filename_list[0] and elm_split[-1]==filename_list[-1]:
                            sequence_list.append(elm)
                        else:
                            dif_list.append(elm)
                    else:
                        dif_list.append(elm)

                if len(sequence_list)>3:
                    is_sequence = 0
                    i=0
                    seq_name = ''
                    seq_len = 0
                    min_num=0
                    max_num=0
                    file_replace_name = ''
                    end_with = ''
                    for elm in sequence_list:
                        split_result = cls.getnumber(elm)
                        num = split_result[2]
                        if i==0:
                            split_str_1 = split_result[1]
                            num_1 = split_result[2]
                            seq_name = elm.split(split_str_1)[0]
                            end_with = elm.split(split_str_1)[-1]
                            seq_len_bg = len(num)
                            min_num = int(num)
                        if i==len(sequence_list)-1:seq_len_end = len(num)
                        if int(num)<min_num:min_num=int(num)
                        if int(num)>max_num:max_num=int(num)
                        i +=1
                    # print("%s sequence from %d to %d"%(seq_name,min_num,max_num))
                    seq_len = seq_len_bg if seq_len_end == seq_len_bg else seq_len_end
                    file_replace_name = seq_name+split_str_1.replace(num_1,"$F%d"%seq_len)+end_with

                    """ put into adict """
                    """ {"abc":[["abc.0001","abc.0002"..."abc.0010"],1,10,4,abc.$F3.exr]} """
                    sequence_adict[seq_name]=[sequence_list,min_num,max_num,seq_len,file_replace_name]
                    return is_sequence,sequence_adict,dif_list
                else:
                    maby_sequence=False
            if not maby_sequence:
                file_path = os.path.abspath(os.path.join(dirt,filename))
                if os.path.exists(file_path):
                    ### exist , not a sequence
                    if len(adict_in):
                        adict_in.remove(filename)
                        dif_list.extend(adict_in)
                    else:
                        All_files.remove(filename)
                        dif_list.extend(All_files)
                    return is_sequence,filename,dif_list
                else:
                    # print("this file is not exist.")
                    return 2,filename,[]
        else:
            print("Please set the filename for this function.")
            return 3,"Please set the filename for this function.",[]

    @staticmethod
    def getmiss_elm(adictin={}):
        miss_adict = {}
        files_adict = {}
        for key in adictin.keys():
            num_list = []
            miss_list = []
            list_sequ = adictin[key][0]
            for elm in list_sequ:
                num_list.append(int(re.findall("\d+",elm)[-1]))
            num_list = sorted(num_list)
            min_num = adictin[key][1]
            max_num = adictin[key][2]
            for i in range(len(num_list)):
                if num_list[i] >=min_num and num_list[i]<=max_num:
                    if i==0 and num_list[i] == min_num:curent_val = min_num
                    if not curent_val in num_list:
                        miss_list.append(curent_val)
                    curent_val += 1
            miss_adict[adictin[key][4]] = miss_list
            files_adict[key] = {"start":min_num,"end":max_num,"miss":miss_list}
        return miss_adict,files_adict


    @classmethod
    def getnumber(cls,filename=''):
        maby_sequence = True
        split_str = ''
        num = ''
        with_num = re.findall("\d+",filename)
        if len(with_num)>0:
            num = with_num[-1]
            num_len = len(with_num[-1])
            if ("."+with_num[-1]+".") in filename:
                split_str = "."+with_num[-1]+"."
            elif (with_num[-1]+".") in filename:
                split_str = with_num[-1]+"."
            else:
                maby_sequence = False
                # print("Not sequence")
        else:
            maby_sequence = False
            # print("Without Numbers")
        return maby_sequence,split_str,num

    @classmethod
    def GetBadFile(cls,adict=''):
        bad_end = ['kkk','aspk']
        bad_list = []
        other_list = []
        bad_adict = {}
        if len(adict):
            for elm in adict:
                if elm.split(".")[-1] in bad_end:
                    bad_list.append(elm)
                else:
                    other_list.append(elm)
        if len(bad_list):
            for elm in bad_list:
                copy_list = []
                maby_sequence,split_str,num = cls.getnumber(elm)
                if maby_sequence:
                    filename = elm.split(split_str)[0]
                    if "sequence" in bad_adict.keys():
                        copy_adict = bad_adict["sequence"]
                        if filename in copy_adict.keys():
                            copy_list=copy_adict[filename]
                            copy_list.append(elm)
                            copy_adict[filename]=copy_list
                        else:
                            copy_list=[elm]
                            copy_adict[filename]=copy_list
                        bad_adict["sequence"]=copy_adict
                    else:
                        copy_list=[elm]
                        bad_adict["sequence"]={filename:copy_list}
                else:
                    filename = elm.split(".")[0]
                    if "single" in bad_adict.keys():
                        copy_list=bad_adict["single" ]
                        if not filename in copy_list:
                            copy_list.append(elm)
                        bad_adict["single"]=copy_list
                    else:
                        copy_list=[elm]
                        bad_adict["single" ]=copy_list
        return bad_adict,other_list

    @classmethod
    def check_adict(cls,dirt="",filename="",adict_in={}):
        ## adict_in={"sequences":{},"singles":[],"badfiles":{"single":[],"sequence":{}},"others":[]}
        in_adict = False
        check = True
        findit = False
        is_exist = True
        types = ''
        return_info = ''
        if dirt in adict_in:
            maby_sequence,split_str,num = cls.getnumber(filename)
            if maby_sequence:
                seq_name = filename.split(split_str)[0]
                if "sequences" in adict_in[dirt]:
                    if seq_name in adict_in[dirt]["sequences"]:
                        in_adict = True
                        check = False
                        findit = True
                        # return_info = [findit,"sequence",[seq_name,adict_in[dirt]["sequences"][seq_name]]]
                elif "badfiles" in adict_in[dirt]:
                    if "sequence" in adict_in[dirt]["badfiles"]:
                        if seq_name in adict_in[dirt]["badfiles"]["sequence"]:
                            in_adict = True
                            check = False
                            findit = True

            if findit==False:
                if "singles" in adict_in[dirt]:
                    if filename in adict_in[dirt]["singles"]:
                        in_adict = True
                        check = False
                        findit = True
                        # return_info = [findit,"single"]
                if "badfiles" in adict_in[dirt]:
                    if "single" in adict_in[dirt]["badfiles"]:
                        if filename in adict_in[dirt]["badfiles"]["single"]:
                            in_adict = True
                            check = False
                            findit = True
                            # return_info = [findit,"badfile"]
                if "others" in adict_in[dirt].keys():
                    if filename in adict_in[dirt]["others"]:
                        ## to check
                        in_adict = True
                        findit = True
                        # return_info = adict_in[dirt]["others"]

            if findit==False:
                if not os.path.exists(os.path.abspath(os.path.join(dirt,filename))):
                    is_exist = False
                    check = False
                    # return_info=[findit,is_exist]
                    # print("Not exist!")

        return in_adict,check,findit