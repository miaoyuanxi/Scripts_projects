'''
from Enalyze script we v got these:
/out/mantra_ipr|1.0|240.0|1.0|-1
/obj/distribute_pyro/save_slices|1|240|1|0
/obj/distribute_pyro/save_slices|1|240|1|1
/obj/distribute_pyro/save_slices|1|240|1|2
/obj/distribute_pyro/save_slices|1|240|1|3

in this pattern:
ropname|startframe|endframe|byframe|marker, 5 sections seperated by '|'

use markers to identify a render or simulation
value '-1' identifies a render
positive value starts at 0~? identifies a simulation, 
which also mean the slice number of the simulation.

render script
_CID    customer id
_TID    task id
_SFM    startframe
_EFM    endframe
_BFM    byframe
_HIP    Houdini hip file name
_ROP    ropname
_RRD    output directory
_OPT    extra waste parameter

for example
B:\plugins\houdini\Erender.py 53 0 101 101 1 \\10.50.1.4\d\inputData\maya\0\53\chenzhong\cfh\3d_uboat_render_nc.hip /out/mantra2 d:/work/0 -1
'''

import sys,os,subprocess,string,re
import time
_PATH_ORG = os.environ.get('PATH')
os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";C:\Windows\system32"

# PARMS ORDER
_CID = sys.argv[1]
_TID = sys.argv[2]
_SFM = sys.argv[3]
_EFM = sys.argv[4]
_BFM = sys.argv[5]
_HIP = sys.argv[6]
_HIP = _HIP.replace("\\", "/")
_ROP = sys.argv[7]
_ROP = _ROP.replace("\\", "/")
_RRD = sys.argv[8]
_RRD = _RRD.replace("\\", "/")
_OPT = sys.argv[9]

print "_CID: %s" % _CID
print "_TID: %s" % _TID
print "_SFM: %s" % _SFM
print "_EFM: %s" % _EFM
print "_BFM: %s" % _BFM
print "_HIP: %s" % _HIP
print "_ROP: %s" % _ROP
print "_RRD: %s" % _RRD
print "_OPT: %s" % _OPT
#HS_ip = "10.60.96.203"
HS_ip = "10.50.10.231"
HS_ip = "10.60.96.203"

# GENERAL ENV SETUP
python_version = "%d.%d" % sys.version_info[:2]
python_version_no_dot = "%d%d" % sys.version_info[:2]
_PYTHON_V_WITH_DOT = str(python_version)
_PYTHON_V_NO_DOT = str(python_version_no_dot)
os.environ['PYTHONPATH'] = r"C:/Python%s" % _PYTHON_V_NO_DOT


# IMPORT RVLIB MODULE
#_SERVER_IP_ROOT = r"//10.50.242.1"
_SERVER_IP_ROOT = r"B:"
_HOU_LIB_NETWORK_PATH = _SERVER_IP_ROOT + r"/plugins/houdini/lib"
sys.path.append(_HOU_LIB_NETWORK_PATH)

print("---------------------------------------------------------\n")
print("HOUDINI RENDER SETUP")

import RVLIB
T_gpuid=None
_CID_ROOT = RVLIB._RV_retrieveUniqueUserRoot(_CID, _HIP)
if _CID_ROOT is None:
    _CID_ROOT = os.path.dirname(_HIP)
print "\nASSETS SEARCHING PATH: %s" % _CID_ROOT

#_HIP EXIST CHECK
if os.path.isfile(_HIP):
    # 00
    _HIP_BASENAME = os.path.splitext(os.path.basename(_HIP))[0]
    
    # 01 rd dir setup
    if not _RRD.endswith(('/')):
        _RRD += "/"
    if not os.path.exists(_RRD):
        os.makedirs(_RRD)
    
    # 02 otl path setup
    _PATH_USER_OTLS = RVLIB._RV_App_OTL_Path_Setup(_HIP)
    #print "_PATH_USER_OTLS=" + _PATH_USER_OTLS
    
    # 03 TOOLS 7z SETUP
    _TOOL_7Z_RUN_PATH = RVLIB._RV_Tool_7z_Setup(_SERVER_IP_ROOT)
    #print "_TOOL_7Z_RUN_PATH=" + _TOOL_7Z_RUN_PATH
    
    # 04 GET BEST HOU VERSION FORM HIP SAVE VERSION
    _HOU_BEST_VERSION_STR = RVLIB._RV_getBestFitHOUVersionFromHip(_SERVER_IP_ROOT, _HIP)
    print("GET _HOU_BEST_VERSION_STR: "+_HOU_BEST_VERSION_STR)
    
    '''
    _PLU_CUS_py_path= r"B:\plugins\houdini\plugins\custom_config"+'\\'+_CID
    print("CUSTOM SETUP FOLDER:  "+ _PLU_CUS_py_path)
    if os.path.exists(_PLU_CUS_py_path+"\\houdiniCustomConfig.py"):

        print _PLU_CUS_py_path+"\\houdiniCustomConfig.py"
        sys.path.append(_PLU_CUS_py_path)
        print sys.path
        cfg = __import__('houdiniCustomConfig')

        reload(cfg)

        print 'plugins custom RayvisionCustomConfig '
        T_gpuid=cfg.doConfigSetup()
        '''

### DO A CUSTOM SETUP (VERSION)
    setuptxt_path=r"B:\plugins\houdini\plugins\custom_config"+'\\'+_CID+"\\setup.txt"
    
    if os.path.exists(setuptxt_path):
        file=open(setuptxt_path,"r")
        elm_arr=file.readlines()
        file.close()
        if len(elm_arr)>1:
            arr_copy=[]
            for elm in elm_arr:
               arr_copy.append(elm.strip("\n"))
            elm_arr=arr_copy
            #print(elm_arr)
        
        ### SET THE HOUDINI VERSION BY HAND
        for elm in elm_arr:
            keyword=elm.split("=")[0]
            valuepath=elm.split("=")[1]
            if keyword=='version':
               _HOU_BEST_VERSION_STR=valuepath
               print("SET THE HOUDINI VERSION TO: "+valuepath)
               break

    #houdini lic start
    print "houdini lic open"
    RVLIB.hou_lic(_HOU_BEST_VERSION_STR[0:2],HS_ip)
    
    # 05 INSTALL/UPDATE HOU
    _HOU_RUN_PATH = RVLIB._RV_App_Hou_Setup(_SERVER_IP_ROOT, _HOU_BEST_VERSION_STR, True)
    print "\r\r_HOU_RUN_PATH=" + _HOU_RUN_PATH
    
    _PLU_CUS_py_path= r"B:\plugins\houdini\plugins\custom_config"+'\\'+_CID
    print("CUSTOM SETUP FOLDER:  "+ _PLU_CUS_py_path)
    if os.path.exists(_PLU_CUS_py_path+"\\houdiniCustomConfig.py"):

        print _PLU_CUS_py_path+"\\houdiniCustomConfig.py"
        sys.path.append(_PLU_CUS_py_path)
        print sys.path
        cfg = __import__('houdiniCustomConfig')

        reload(cfg)

        print 'plugins custom RayvisionCustomConfig '
        T_gpuid=cfg.doConfigSetup()
        
    # 06 ENV SETUP
    RVLIB._RV_App_Hou_Env_Setup(_HOU_RUN_PATH, _PYTHON_V_WITH_DOT, _PYTHON_V_NO_DOT)
    
    
    # 07 LOAD HOU AND RVHOU MODULES
    print "Importing libs ..."
    import hou
    import RVHOU
    import findfiles
    
    # 08 LOAD HIP FILE
    RVHOU._RV_loadHipFile(_HIP)
    # 09 UPDATE SOME INTERNAL ENVS
    _HIP_VAR = os.path.dirname(_HIP)
    hou.hscript("setenv HIP=" + str(_HIP_VAR))
    hou.hscript("varchange")
    if T_gpuid==0:
        hou.hscript("Redshift_setGPU -s 10")
        print ("Set GPU %s available" % T_gpuid)
    elif T_gpuid==1:
        hou.hscript("Redshift_setGPU -s 01")
        print ("Set GPU %s available" % T_gpuid)
    print "$HIP="+hou.getenv("HIP")

    ## SET CUSTOM ENV BY USER
    user_envset=r'B:\plugins\houdini\plugins\user_envset\custom_ID.txt'
    if os.path.exists(user_envset):
        file=open(user_envset,"r")
        id_arr=file.readlines()
        file.close()
        if len(id_arr)>1:
            arr_copy=[]
            for elm in id_arr:
               arr_copy.append(elm.strip("\n"))
            id_arr=arr_copy
            #print(id_arr)
        set_cutom=0
        for elm in id_arr:
            if _CID==elm:
               set_cutom=1 
               print("Addition env set by user! ")
               break
        if set_cutom==1:
            set_path=r'B:\plugins\houdini\plugins\user_envset\set_env_lib'
            sys.path.append(set_path)
            import set_user_env
            set_job=set_user_env.userEnv(_CID,_TID)
            set_job.setEnv()
        else:
            print("User did not use the  addition env ")

### SET ENV FOR USERS IN THE CUSTOM CONFIG FOLDER
    _PLU_CUS_env_txt_path= r"B:\plugins\houdini\plugins\custom_config"+'\\'+_CID+"\\env.txt"
    if os.path.exists(_PLU_CUS_env_txt_path):
        print("SET ENV FOR USERS IN THE CUSTOM CONFIG FOLDER\n")
        print "  _PLU_CUS_env_txt_path  " + _PLU_CUS_env_txt_path
        try:
            f=open(_PLU_CUS_env_txt_path,"r")
            env_lines=f.readlines()
            f.close()
            for env_line in env_lines:

                env_line =env_line.strip().replace('\\', '/')
                #print len(env_line)
                env_name=env_line.split("=")[0]
                env_val=env_line.split("=")[1]
                env_lines="setenv "+env_line
                print env_lines,env_name,env_val
                
                hou.hscript(env_lines)
                hou.hscript("varchange")
                print hou.getenv(env_name)
        except IOError,error:
            print error
    #### map 
    _PLU_CUS_env_txt_path= r"B:\plugins\houdini\plugins\custom_config"+'\\'+_CID+"\\mappath.txt"
    if os.path.exists(_PLU_CUS_env_txt_path):
        print("PATH MAPPING SIGNAL \n")
        print "  USING " + _PLU_CUS_env_txt_path
        try:
            f=open(_PLU_CUS_env_txt_path,"r")
            env_lines=f.readlines()
            f.close()
            for env_line in env_lines:
                env_line =env_line.strip("\n").replace('\\', '/')
                print(env_line)
                hou.hscript(env_line)
            hou.hscript("varchange")
            print '\n'
        except IOError,error:
            print error


#### SIMULATION SET WITH ROP CONNECT
    _ignore_opl=True
    print("set the _ignore_opl default to True")
    simulation_path = r"B:\plugins\houdini\plugins\custom_config\1821191\simulation.txt"
    if os.path.exists(simulation_path):
        print("SETUP SIMULATION SET WITH ROP CONNECT")
        file=open(simulation_path,"r")
        id_arr=file.readlines()
        file.close()
        if len(id_arr)>1:
            arr_copy=[]
            for elm in id_arr:
               arr_copy.append(elm.strip("\n"))
            id_arr=arr_copy
            #print(id_arr)
        for elm in id_arr:
            if _CID==elm:
               _ignore_opl=False
               print("Make the simulation active!")
               break
        
    print "_ignore_opl   final value"
    print  _ignore_opl
    # 10 MISSING CHECK
    #print "\nCHECK MISSING REFERENCE ASSET(S) ... /shop"
    #RVHOU._RV_missingReferenceCheckAndAutoFix(_CID_ROOT, "/shop")
    
    #print "\nCHECK MISSING REFERENCE ASSET(S) ... /out"
    #RVHOU._RV_missingReferenceCheckAndAutoFix(_CID_ROOT, "/out")
    
    # 11 MISSING SKIP
    #print "\nSKIP MISSING REFERENCE ASSET(S) ..."
    #RVHOU._RV_missingReferenceSkip()
    
    # 12 GET THE OBJ OBJECT
    obj = None
    if _OPT == '-1':
        obj = RVHOU._RV_renderSetup(_ROP, _SFM, _EFM, _BFM, _RRD, _HIP_BASENAME)
        print '    RENDER SETUP DONE @ %s' % _ROP
    else:
        if _OPT.isdigit():
            _this_Node = hou.node(_ROP)
            objPath = _this_Node.path()
            objPath = objPath.replace('\\','/')
            objTypeName = _this_Node.type().name()
            if objTypeName in ['geometry']:
                obj = RVHOU._RV_geometrySetup(_ROP, _SFM, _EFM, _BFM, _OPT, _HIP_BASENAME)
                print '\nGEOMETRY SETUP DONE @ %s' % _ROP
            else:
                obj = RVHOU._RV_simulationSetup(_ROP, _SFM, _EFM, _BFM, _OPT, _HIP_BASENAME)
                print '\nSIMULATION SETUP DONE @ %s' % _ROP
        else:
            print "\nFATAL ERROR: UNKNOWN MARKER:\'%s\', PLS ANALYZE IT BEFORE RENDER." % _OPT
            # kill rlm.exe
            os.system(r'wmic process where name="JGS_mtoa_licserver.exe" delete')
            os.system(r'wmic process where name="rlm.exe" delete')
            sys.exit(1)
    
    ### print the files in this scene
    filespath=r"D:/work/render/"+_TID
    print filespath
    print "-----------------------------------------------------------------"
    print "                           FILES                                 "
    print "-----------------------------------------------------------------"
    # if _CID="1843297":
    #     findfiles.DOFILES(filespath,0)
    findfiles.DOFILES(filespath,0)
    import cam_find
    cam_find.main()
    print "-----------------------------------------------------------------"
    
    time_render_at=time.time()
    cmdkillJGS=r'c:\windows\system32\cmd.exe /c c:\windows\system32\TASKKILL.exe /F /IM JGS_mtoa_licserver.exe '
    cmdkillrlm=r'c:\windows\system32\cmd.exe /c c:\windows\system32\TASKKILL.exe /F /IM rlm.exe '
    # 13 RENDER IT NOW
    if obj is None:
        print "\nFATAL ERROR: THE SPECIFIED ROP NOT FOUND."
        # kill rlm.exe
        os.system(cmdkillJGS)
        os.system(cmdkillrlm)
        sys.exit(1)
    else:
        print "\nALL SET, RENDERING ..."
        RVHOU._RV_renderRop(obj,frame_range=(float(_SFM),float(_EFM),float(_BFM)) ,ignore_inputs=_ignore_opl,ignore_bypass_flags=True)
        time_render_end=time.time()
        render_time='%.3f'% (time_render_end-time_render_at)
        print ("Rendered with %s s" % render_time)
        # kill rlm.exe
        os.system(cmdkillJGS)
        os.system(cmdkillrlm)
        sys.exit(0)
else:
    print "\nFATAL ERROR: THE SPECIFIED HIP FILE NOT FOUND."
    # kill rlm.exe
    #os.system(cmdkillJGS)
    #os.system(cmdkillrlm)
    sys.exit(1)





