
'''
analyze script

_CID    customer id
_TID    task id
_HIP    Houdini hip file name
_INF    text file 

_INF text content will be in this pattern
ropname|startframe|endframe|byframe|marker, 5 sections seperated by '|'

eg.
/out/mantra_ipr|1.0|240.0|1.0|-1
/obj/distribute_pyro/save_slices|1|240|1|0
/obj/distribute_pyro/save_slices|1|240|1|1
/obj/distribute_pyro/save_slices|1|240|1|2
/obj/distribute_pyro/save_slices|1|240|1|3

markers identify a render or simulation
negative value '-1' indicates a render
while positive values starts at 0~? indicate a simulation, 
which also mean the slice number of the simulation.

4 lines represent 4 tasks can be fired to dispater which in our case is mumu.

for example
B:\plugins\houdini\Enalyze.py 53 0 \\10.50.1.4\d\inputData\maya\0\53\chenzhong\cfh\3d_uboat_render_nc.hip d:/work/0/info.txt
'''

import sys,os,subprocess,string,re
_PATH_ORG = os.environ.get('PATH')
os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";C:\Windows\system32"

# PARMS ORDER
_CID = sys.argv[1]
_TID = sys.argv[2]
_HIP = sys.argv[3]
_HIP = _HIP.replace("\\", "/")
_INF = sys.argv[4]
_INF = _INF.replace("\\", "/")

print "_CID: %s" % _CID
print "_TID: %s" % _TID
print "_HIP: %s" % _HIP
print "_INF: %s" % _INF
#HS_ip = "10.60.96.203"
HS_ip = "10.50.10.231"
HS_ip = "10.60.96.203"
w2sesinetdpath=os.path.join(r"\\",HS_ip,"c$\Windows\System32\sesinetd.exe")
if not os.path.exists(w2sesinetdpath):
    HS_ip = "10.50.4.91"
    print("CHANGED SERVER TO WF FOR RIGHT NOW")
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
print sys.path


import RVLIB
_CID_ROOT = RVLIB._RV_retrieveUniqueUserRoot(_CID, _HIP)
if _CID_ROOT is None:
    _CID_ROOT = os.path.dirname(_HIP)
print "\nASSETS SEARCHING PATH: %s" % _CID_ROOT

#_HIP EXIST CHECK
if os.path.isfile(_HIP):
    # maybe, before everything, make a copy of the hip
    # and run with it
    # but not just yet
    
    # 00
    _HIP_BASENAME = os.path.splitext(os.path.basename(_HIP))[0]
    
    # 01 rd dir setup
    # 02 otl path setup
    _PATH_USER_OTLS = RVLIB._RV_App_OTL_Path_Setup(_HIP)
    #print "_PATH_USER_OTLS=" + _PATH_USER_OTLS
    
    # 03 TOOLS 7z SETUP
    _TOOL_7Z_RUN_PATH = RVLIB._RV_Tool_7z_Setup(_SERVER_IP_ROOT)
    #print "_TOOL_7Z_RUN_PATH=" + _TOOL_7Z_RUN_PATH
    
    # 04 GET BEST HOU VERSION FORM HIP SAVE VERSION
    _HOU_BEST_VERSION_STR = RVLIB._RV_getBestFitHOUVersionFromHip(_SERVER_IP_ROOT, _HIP)
    print("GET _HOU_BEST_VERSION_STR: "+_HOU_BEST_VERSION_STR)

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
    print "_HOU_RUN_PATH=" + _HOU_RUN_PATH
    
    _PLU_CUS_py_path= r"B:\plugins\houdini\plugins\custom_config"+'\\'+_CID
    print("CUSTOM SETUP FOLDER:  "+ _PLU_CUS_py_path)
    if os.path.exists(_PLU_CUS_py_path+"\\houdiniCustomConfig.py"):

        print _PLU_CUS_py_path+"\\houdiniCustomConfig.py"
        sys.path.append(_PLU_CUS_py_path)
        print sys.path
        cfg = __import__('houdiniCustomConfig')

        reload(cfg)

        print 'plugins custom RayvisionCustomConfig '
        gpuid = cfg.doConfigSetup()
        try:
            print "del  _PLU_CUS_py_path "
            sys.path.remove(_PLU_CUS_py_path)
        except:
            pass
    
    # 06 ENV SETUP
    RVLIB._RV_App_Hou_Env_Setup(_HOU_RUN_PATH, _PYTHON_V_WITH_DOT, _PYTHON_V_NO_DOT)
    
    # 07 LOAD HOU AND RVHOU MODULES
    import hou
    import RVHOU
    
    # 08 LOAD HIP FILE
    RVHOU._RV_loadHipFile(_HIP)
    
    _PLU_CUS_env_txt_path= r"B:\plugins\houdini\plugins\custom_config"+'\\'+_CID+"\\env.txt"
    if os.path.exists(_PLU_CUS_env_txt_path):
        print "  _PLU_CUS_env_txt_path  " + _PLU_CUS_env_txt_path
        try:
            f=open(_PLU_CUS_env_txt_path,"r")
            env_lines=f.readlines()
            for env_line in env_lines:

                env_line =env_line .strip().replace('\\', '/')
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
   

    # 09 UPDATE SOME INTERNAL ENVS
    _HIP_VAR = os.path.dirname(_HIP)
    hou.hscript("setenv HIP=" + str(_HIP_VAR))
    hou.hscript("varchange")
    
    # 10 WRITE TO FILE
    RVHOU._RV_write_ROPS_Frame_Info(_INF, _HIP_BASENAME)
    # kill rlm.exe
    os.system(r'wmic process where name="JGS_mtoa_licserver.exe" delete')
    os.system(r'wmic process where name="rlm.exe" delete')
    # 11 exit
    sys.exit(0)

else:
    print "\nFATAL ERROR: THE SPECIFIED HIP FILE NOT FOUND."
    # kill rlm.exe
    os.system(r'wmic process where name="JGS_mtoa_licserver.exe" delete')
    os.system(r'wmic process where name="rlm.exe" delete')
    sys.exit(1)