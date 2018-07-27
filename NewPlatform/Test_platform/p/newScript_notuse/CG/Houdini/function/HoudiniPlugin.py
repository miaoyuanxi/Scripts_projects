import os,sys,time
import re
import subprocess
import shutil
from HoudiniUtil import HoudiniUtil


class HoudiniPlugin(object):
    """docstring for HoudiniPlugin"""
    def __init__(self, arg):
        super(HoudiniPlugin, self).__init__()
        self.arg = arg

    @classmethod
    def BaseDataSetup(cls,cls_in=''):
        cls_in.LogsCreat("BaseDataSetup start...")
        cls_in.LogsCreat("...")
        cls_in._hip_file = cls_in.G_INPUT_CG_FILE.replace("\\","/") if len(cls_in.G_INPUT_CG_FILE) else ''
        cls_in._output = cls_in.G_WORK_RENDER_TASK_OUTPUT.replace("\\","/")
        cls_in._task_folder = cls_in.G_WORK_RENDER_TASK.replace("\\","/")

        if cls_in.G_RENDER_OS=='Linux':
            cls_in._houdini_client_dir = '/D/plugins/houdini'
            cls_in._houdini_PLuing_dirt = '/B/plugins/houdini' if os.path.exists("/B/plugins/houdini") else "%s/plugins/houdini"%cls_in.G_PLUGIN_PATH.replace("\\","/")
            app_path = "%s/apps/Linux"%cls_in._houdini_PLuing_dirt
        else:
            cls_in._houdini_client_dir = 'D:/plugins/houdini'
            cls_in._houdini_PLuing_dirt = 'B:/plugins/houdini' if os.path.exists("B:/plugins/houdini") else "%s/plugins/houdini"%cls_in.G_PLUGIN_PATH.replace("\\","/")
            app_path = "%s/apps/win"%cls_in._houdini_PLuing_dirt

        cls_in._code_base_path = os.path.join(cls_in.G_NODE_PY,"CG/Houdini").replace("\\","/")         
        cls_in.hfs_save_version = ''
        cls_in._hfs_version = ''
        cls_in._hip_save_val = ''
        cls_in.hip_val = os.path.dirname(cls_in._hip_file)
        cls_in._plugins = cls_in.G_CG_CONFIG_DICT["plugins"]

        # get imformation from the .hip file
        # version && $HIP
        if os.path.isfile(cls_in._hip_file):

            hip_file_info = HoudiniUtil.GetSaveHipInfo(cls_in._hip_file,app_path)
            if len(hip_file_info)==3:
                cls_in.hfs_save_version = hip_file_info[0]
                cls_in._hfs_version = hip_file_info[1]
                cls_in._hip_save_val = hip_file_info[2]
            else:
                cls_in._run_code_result = False
                cls_in._erorr_code = 'HoudiniUtil.GetSaveHipInfo'
                cls_in._erorr_code_info = hip_file_info[0]
        else:
            cls_in._run_code_result = False
            cls_in._erorr_code = 'HoudiniPlugin.BaseDataSetup'
            cls_in._erorr_code_info = 'The .hip file is not exist.'

        cls_in.LogsCreat("BaseDataSetup end.")
        cls_in.LogsCreat("")

    @classmethod
    def FramesAnalyse(cls,frames=''):
        all_frames = frames
        types = 0
        renderjobs = {}
        ## 5 5 1  /  1,3,6  /  1,2-5,9   /  3,2-10[3],5
        k = 0
        if "," in all_frames:
            frames_list = all_frames.split(",")
            for i in range(len(frames_list)):
                if "-" in frames_list[i]:
                    if "[" in frames_list[i]: ## 2-10[3]
                        frame_sp = frames_list[i].split("]")[0].split("[")
                        frame_ah = frame_sp[0].split("-")
                        renderjobs[str(k)] = [frame_ah[0],frame_ah[-1],frame_sp[-1]]
                        k +=1
                    else: ## 2-5
                        frame_ah = frames_list[i].split("-")
                        renderjobs[str(k)] = [frame_ah[0],frame_ah[-1],str(1)]
                        k +=1
                else:  ## 1
                    renderjobs[str(k)] = [frames_list[i],frames_list[i],str(1)]
                    k +=1
        else:
            frames_arr_s=all_frames.split(" ")
            renderjobs[str(k)] = [frames_arr_s[0],frames_arr_s[1],frames_arr_s[2]]

        return renderjobs

    @classmethod
    def setframes(cls,cls_in=''):
        HoudiniUtil.print_times("setframes start...")
        SF = float(cls_in.ropnode.evalParm('f1'))
        EF = float(cls_in.ropnode.evalParm('f2'))
        BF = float(cls_in.ropnode.evalParm('f3'))
        HoudiniUtil.print_times("FRAME RANGE IN THIS FILE's SET: "+str(SF)+"-"+str(EF)+"["+str(BF)+"]")

        if cls_in.ropnode.evalParm("trange")!=1:
            cls_in.ropnode.parm("trange").set(1)

        if cls_in.ropnode.parm('f1').isLocked():
            cls_in.ropnode.parm('f1').lock(False)
        if cls_in.ropnode.parm('f2').isLocked():
            cls_in.ropnode.parm('f2').lock(False)
        if cls_in.ropnode.parm('f3').isLocked():
            cls_in.ropnode.parm('f3').lock(False)
        cls_in.ropnode.parm('f1').deleteAllKeyframes()
        cls_in.ropnode.parm('f2').deleteAllKeyframes()
        cls_in.ropnode.parm('f3').deleteAllKeyframes()

        frames_arr=cls_in.frame
        HoudiniUtil.print_times (frames_arr)
        Fr1=float(frames_arr[0].strip())
        Fr2=float(frames_arr[1].strip())
        Fr3=float(frames_arr[2].strip())
        cls_in.ropnode.parm("f1").set(Fr1)
        cls_in.ropnode.parm("f2").set(Fr2)
        cls_in.ropnode.parm("f3").set(Fr3)

        SF = float(cls_in.ropnode.evalParm('f1'))
        EF = float(cls_in.ropnode.evalParm('f2'))
        BF = float(cls_in.ropnode.evalParm('f3'))
        HoudiniUtil.print_times("NEW FRAME RANGE TO RENDER: "+str(SF)+"-"+str(EF)+"["+str(BF)+"]")
        HoudiniUtil.print_times("setframes end.")

    @classmethod
    def CreatOutput(cls,valparm="",cls_in=''):

        HoudiniUtil.print_times("ROP output parm: %s" % valparm)
        
        cls_in.outfile_hip=cls_in.ropnode.evalParm(valparm)
        HoudiniUtil.print_times("Output values: %s" % cls_in.outfile_hip)
        if cls_in.outfile_hip=='(not set)' or cls_in.outfile_hip=='':
            cls_in.outfile_hip=os.path.join(cls_in.args.HIP,'out/default.0001.exr')

        HIP_val = ''
        HIP_val = cls_in.args.HIP.replace("\\","/")if "\\" in cls_in.args.HIP else cls_in.args.HIP
        if HIP_val.endswith('/'): HIP_val = HIP_val[:-1]
        # HoudiniUtil.print_times("$Hip_Save_Val: %s" % HIP_val)
        
        outfile_hip=cls_in.outfile_hip.replace("\\","/")   ### $HIP/aa/aa/aa.$F4.exr
        if HIP_val in outfile_hip:
            outfile_arr_main=outfile_hip.split(HIP_val+"/")[-1]   ### aa/aa/aa.$F4.exr  aa.$F4.exr
        elif cls_in._hip_val in outfile_hip:
            outfile_arr_main=outfile_hip.split(cls_in._hip_val+"/")[-1]   ### aa/aa/aa.$F4.exr  aa.$F4.exr
        elif ":/" in outfile_hip:
            outfile_arr_mains=outfile_hip.split("/")   ### aa/aa/aa.$F4.exr  aa.$F4.exr
            outfile_arr_main = (outfile_arr_mains[-2]+"/"+outfile_arr_mains[-1]) if len(outfile_arr_mains)>2 else outfile_arr_mains[-1]
        else:
            outfile_arr_main = outfile_hip
        
        outfile_arr=outfile_arr_main.split("/") if "/" in outfile_arr_main else [outfile_arr_main]

        FFs=re.findall(r"\d+",outfile_arr[-1])
        FF = FFs[-1] if len(FFs) else '001'
        dotF="$F%d" % len(FF)
        namepart=outfile_arr[-1].split(".")
        name_s = ''
        if len(namepart)>2:
            for i in range(len(namepart)):
                if i == len(namepart)-2:
                    break
                name_s += namepart[i] + "."
        else:
            name_s = namepart[0]
        outname = name_s+dotF+"."+namepart[-1]  ### aa.$F4.exr
        outfile_M=outfile_arr_main.split("/"+outfile_arr[-1])[0] if "/" in outfile_arr_main else ''

        # $HIP/aaa/aass/aaa.$F3.exr
        out_dir=os.path.join(cls_in.args.outdir,outfile_M)
        out_dir=out_dir.replace("\\","/")
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        outputFiles=os.path.join(cls_in.args.outdir,outfile_M,outname)
        outputFiles=outputFiles.replace("\\","/")
        # HoudiniUtil.print_times("outputFiles .../%s/%s" % (outfile_M,outname))
        HoudiniUtil.print_times("OutputFiles changed to: %s" % outputFiles)
        
        return outputFiles

    @classmethod
    def SetMantra(cls,cls_in=''):
        HoudiniUtil.print_times("Output_Mantra set start...")
        
        ropTypeName = cls_in.ropnode.type().name()
        HoudiniUtil.print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['ifd']:
            outputFiles = cls.CreatOutput("vm_picture",cls_in)
            cls_in.ropnode.parm("vm_picture").set(outputFiles)
            HoudiniUtil.print_times("Output check:")
            HoudiniUtil.print_times(cls_in.ropnode.evalParm("vm_picture"))
            
            ### set aov pass
            out_aovs = cls_in.ropnode.parm("vm_numaux").eval()
            if out_aovs > 0:
                HoudiniUtil.print_times("Output_Mantra aov set start...")
                aovs_list = []
                for i in range(out_aovs):
                    parm_k = "vm_disable_plane%d"%(i+1)
                    if not cls_in.ropnode.parm(parm_k).eval():
                        parm_f_use = "vm_usefile_plane%d"%(i+1)
                        if cls_in.ropnode.parm(parm_f_use).eval():
                            parm_f_val = "vm_filename_plane%d"%(i+1)
                            aovs_list.append(parm_f_val)
                if len(aovs_list) > 0:
                    for elm in aovs_list:
                        _outputFiles = cls.CreatOutput(elm,cls_in)
                        cls_in.ropnode.parm(elm).set(_outputFiles)

        HoudiniUtil.print_times("Output_Mantra set end.")

    @classmethod
    def render_Mantra(cls,cls_in=''):

        HoudiniUtil.print_times("Render_Mantra start...")
        #root_take = hou.takes.rootTake()
        #curt_take = hou.takes.currentTake()
        _ifd = cls_in.ropnode.parm("soho_outputmode").eval()
        if _ifd:
            cls_in.ropnode.parm("soho_outputmode").set(0)

        # set the Log level to 5 
        _level = cls_in.ropnode.parm("vm_verbose").eval()
        if int(_level) != 5:
            _level = cls_in.ropnode.parm("vm_verbose").set(5)

        cls_in.ropnode.render(verbose=cls_in._verbose_s,quality=cls_in._quality, ignore_inputs=cls_in._ignore_inputs, method=cls_in._method, ignore_bypass_flags=cls_in._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        HoudiniUtil.print_times("Render_Mantra end.")

    @classmethod
    def SetRedshift(cls,clas=''):
        HoudiniUtil.print_times("Output_RS set start...")
        
        if cls_in.args.GPU==0:
            hou.hscript("Redshift_setGPU -s 10")
            HoudiniUtil.print_times('Set GPU %d avilable' % cls_in.args.GPU)
        elif cls_in.args.GPU==1:
            #hou.hscript("Redshift_setGPU -s 01")
            HoudiniUtil.print_times('Set GPU avilable' )
            #HoudiniUtil.print_times('Set GPU %d avilable' % cls_in.args.GPU)
        else:
            HoudiniUtil.print_times ("ERROR WITH GPU ID: %d [0 TO 1 FOR RIGHT NOW(17/3/2017)]" % cls_in.args.GPU)
            sys.exit(1)

        ropTypeName = cls_in.ropnode.type().name()
        HoudiniUtil.print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['Redshift_ROP']:
            outputFiles = cls_in.CreatOutput("RS_outputFileNamePrefix")
            if not cls_in.ropnode.evalParm("RS_outputEnable"):
                cls_in.ropnode.parm("RS_outputEnable").set(True)
            cls_in.ropnode.parm("RS_outputFileNamePrefix").set(outputFiles)
            HoudiniUtil.print_times("Output check:")
            HoudiniUtil.print_times(cls_in.ropnode.evalParm("RS_outputFileNamePrefix"))
        
        HoudiniUtil.print_times("Output_RS set end.")

    @classmethod
    def render_RS(cls,cls_in=''):
        HoudiniUtil.print_times("Render_RS start...")
        root_take = hou.takes.rootTake()
        curt_take = hou.takes.currentTake()
        n_parm = cls_in.ropnode.parmTuple("RS_renderToMPlay") if cls_in.ropnode.type().name()=="Redshift_ROP" else ""
        if not n_parm == "":
            if curt_take != root_take:
                if not curt_take.hasParmTuple(n_parm):
                    curt_take.addParmTuple(n_parm)
                    #curt_take.removeParmTuple(n_parm
            if cls_in.ropnode.parm("RS_renderToMPlay").eval()==1:
                cls_in.ropnode.parm("RS_renderToMPlay").set(0)

        cls_in.ropnode.render(verbose=cls_in._verbose_s,quality=cls_in._quality, ignore_inputs=cls_in._ignore_inputs, method=cls_in._method, ignore_bypass_flags=cls_in._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        HoudiniUtil.print_times("Render_RS end.")

    @classmethod
    def SetArnold(cls,cls_in=''):
        HoudiniUtil.print_times("Output_AR set start...")

        ropTypeName = cls_in.ropnode.type().name()
        HoudiniUtil.print_times("ROP output type %s" % ropTypeName)
        if ropTypeName in ['arnold']:
            outputFiles = cls_in.CreatOutput("ar_picture")
            cls_in.ropnode.parm("ar_picture").set(outputFiles)
            HoudiniUtil.print_times("Output check:")
            HoudiniUtil.print_times(cls_in.ropnode.evalParm("ar_picture"))
            
            ### set aov pass
            out_aovs = cls_in.ropnode.parm("ar_aovs").eval()
            if out_aovs > 0:
                HoudiniUtil.print_times("Output_Arnold aov set start...")
                aovs_list = []
                for i in range(out_aovs):
                    parm_k = "ar_enable_aov%d"%(i+1)
                    if cls_in.ropnode.parm(parm_k).eval():
                        parm_f_use = "ar_aov_separate%d"%(i+1)
                        if cls_in.ropnode.parm(parm_f_use).eval():
                            parm_f_val = "ar_aov_separate_file%d"%(i+1)
                            aovs_list.append(parm_f_val)
                if len(aovs_list) > 0:
                    for elm in aovs_list:
                        _outputFiles = cls_in.CreatOutput(elm)
                        cls_in.ropnode.parm(elm).set(_outputFiles)
        
        HoudiniUtil.print_times("Output_AR set end.")

    @classmethod
    def render_AR(cls,cls_in=''):

        HoudiniUtil.print_times("Render_AR start...")
        # root_take = hou.takes.rootTake()
        # curt_take = hou.takes.currentTake()
        cls_in.ropnode.render(verbose=cls_in._verbose_s,quality=cls_in._quality, ignore_inputs=cls_in._ignore_inputs, method=cls_in._method, ignore_bypass_flags=cls_in._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        HoudiniUtil.print_times("Render_AR end.")

    @classmethod
    def RenderSimulate(cls,cls_in=''):
        print_times("Render_sml start...")
        sml_out = cls_in.ropnode.parm("sopoutput").eval()
        print_times("Simulation output: %s" % sml_out)

        cls_in.ropnode.render(verbose=cls_in._verbose_s,quality=cls_in._quality, ignore_inputs=cls_in._ignore_inputs, method=cls_in._method, ignore_bypass_flags=cls_in._ignore_bypass_flags, ignore_lock_flags=False, output_progress=False)
        print_times("Render_sml end.")

    @classmethod
    def DataInfo(cls,cls_in=''):
        # --------------------------------------------------------------------------------
        #                           JOB INFORMATION PRINT
        # --------------------------------------------------------------------------------
        cls_in.LogsCreat(" ")
        cls_in.LogsCreat("JOB INFORMATION")
        cls_in.LogsCreat("Function: %s"% (cls_in.G_ACTION if not cls_in.G_ACTION=='' else 'Analyze'))
        cls_in.LogsCreat("File saved with Houdini %s"%cls_in.hfs_save_version)
        cls_in.LogsCreat("File saved with $HIP val %s"%cls_in._hip_save_val)
        cls_in.LogsCreat("...")
        cls_in.LogsCreat("Final Houdini version to run this Job : %s"%cls_in._hfs_version)
        cls_in.LogsCreat("Hip file: %s"%cls_in._hip_file)
        cls_in.LogsCreat("Final $HIP val to run this Job : %s"%cls_in.hip_val)
        cls_in.LogsCreat('...')
        cls_in.LogsCreat("Plugins Info: %s"%cls_in._plugins)
        # --------------------------------------------------------------------------------                          
        # ----------------------------RENDER LOG INFORMATION PRINT------------------------

        cls_in.LogsCreat("Log start...\n"+"-"*150+"\n"+"/"*150+"\n"+"-"*150+"\n",True,False)
        houdini_verser_full = cls_in._hfs_version[:2]+"."+cls_in._hfs_version[2:3]+"."+cls_in._hfs_version[3:]
        cls_in.LogsCreat("Software: Houdini %s\n\n"%houdini_verser_full,True,False)

    @classmethod
    def CameraCkeck(cls,cls_in=''):
        HoudiniUtil.print_times("CameraCheck...")
        import hou
        AllNode = hou.node("/").allSubChildren()
        if len(AllNode)>0:
            for elm in AllNode:
                if elm.type().name() in cls_in.render_node_type:
                    cam_node = elm.parm("camera").eval()
                    if hou.node(cam_node):
                        returns=cls.abc_find(cam_node)
                        if returns==False:
                            HoudiniUtil.print_times("RenderNode: %s" % elm.path())
                            HoudiniUtil.print_times("Camera: %s"%cam_node)
                            HoudiniUtil.print_times("")
                    else:
                        HoudiniUtil.print_times("The camera donot exist!")
                        HoudiniUtil.print_times("RenderNode: %s" % elm)
                        HoudiniUtil.print_times("Camera:\t%s" % cam_node)
                        HoudiniUtil.print_times("")

    
    @classmethod
    def FilesCheck(cls,cls_in=''):
        from HoudiniThread import HoudiniThread
        ## All_node_adict={"file":{ },"abcs":{ },"tex":{ }}
        All_node_adict = cls.node_adict_fite()
        function_all = {"file":[cls.file_check,[cls_in,All_node_adict]],"abc":[cls.abc_ckeck,[cls_in,All_node_adict]],
        "tex":[cls.textur_ckeck,[cls_in]]}
        HoudiniThread.JoinThread(HoudiniThread.StartThread(HoudiniThread.CreatThread(function_all)))

        print("-"*50)
        print ("Folder adict:")
        print cls_in.foler_adict
        print("-"*50)
        print ("Asset adict:")
        print cls_in.asset_adict
        print("-"*50)
        print("Check history: %s"%str(cls_in.check_history))
        print("-"*50)

    @classmethod
    def file_check(cls,cls_in='',adict_in=''):
        # HoudiniUtil.print_times("FileCheck...")
        # return
        import hou
        file_adict = adict_in["file"]
        final_adict = {}
        filte_type = ['filemerge','filecache','cam','ropnet','dopio','output','particlefluidobject']
        print len(file_adict)
        for elm in file_adict:
            if cls.node_type_filte(file_adict[elm],filte_type):
                final_adict[elm] = file_adict[elm]
        if len(final_adict):
            print ("All import files: %d"%len(final_adict))
            for nodes in final_adict:
                if not nodes.path() in cls_in.check_history:
                    upnode = os.path.dirname(final_adict[nodes])
                    if hou.node(upnode).type().name()=="cop2net":
                        files_path=nodes.evalParm("filename2")
                        with_out_dot_list = cls.change_dot_val(files_path)
                        old_node_val = cls.node_deep_val(nodes,"filename2")
                    else:
                        files_path=nodes.evalParm("file")
                        with_out_dot_list = cls.change_dot_val(files_path)
                        old_node_val = cls.node_deep_val(nodes,"file")
                    # print(with_out_dot_list)
                    
                    """  old values in this parm  """
                    # file_name = with_out_dot_list[1].split(HoudiniUtil.getnumber(with_out_dot_list[1])[1])[0]
                    print 888888888888888888888888888888888888
                    print HoudiniUtil.getnumber(with_out_dot_list[1])
                    if not old_node_val[1] in cls_in.check_history:
                        cls_in.check_history[old_node_val[1]] = old_node_val[0]

                        ## dir/name /new_path
                        HoudiniUtil.SequenceCheck(cls_in,with_out_dot_list[0],with_out_dot_list[1],nodes.path())
                    cls_in.check_history[nodes.path()] = old_node_val[0]


    @classmethod
    def abc_ckeck(cls,cls_in='',adict_in=''):
        # HoudiniUtil.print_times("AbcCheck...")
        return
        import hou
        abc_adict = adict_in["abc"]
        abc_inp_adict = adict_in["abc_ipt"]
        final_adict = {}
        filte_type = ['ropnet']
        print len(abc_adict)
        for elm in abc_adict:
            if cls.node_type_filte(abc_adict[elm],filte_type):
                final_adict[elm] = abc_adict[elm]

        if len(final_adict): 
            print ("All import alembic: %d"%len(final_adict))
            for nodes in final_adict:
                if not nodes.path() in cls_in.check_history:
                    upnode = os.path.dirname(final_adict[nodes])
                    files_path=nodes.evalParm("fileName")
                    with_out_dot_list = cls.change_dot_val(files_path)
                    old_node_val = cls.node_deep_val(nodes,"fileName")
                    # print(with_out_dot_list)
                    
                    """  old values in this parm  """
                    if not old_node_val[1] in cls_in.check_history:
                        cls_in.check_history[old_node_val[1]] = old_node_val[0]

                        ## dir/name /new_path
                        HoudiniUtil.SequenceCheck(cls_in,with_out_dot_list[0],with_out_dot_list[1],nodes.path(),"ABCs")
                    cls_in.check_history[nodes.path()] = old_node_val[0]


    @staticmethod
    def textur_ckeck(cls_in=''):
        # HoudiniUtil.print_times("TexturCheck...")
        time.sleep(3)



    @staticmethod
    def abc_find(path=""):
        import hou
        result = True
        if path != "":
            cam_pl = path.split("/")
            if len(cam_pl)>0:
                node_pre = ""
                i=0
                n_types = ["alembicarchive","alembicxform","cam"]
                pathval = {}
                index = 1
                type_abc = False
                first_key = ""          
                for elm in cam_pl:
                    if not elm=="" and not elm=="..":
                        node_pre += "/"+elm             
                        if hou.node(node_pre).type().name() in n_types:
                            if index==1:
                                if hou.node(node_pre).type().name()=="alembicarchive":
                                    type_abc = True
                                    first_key = elm
                            if type_abc==True:                          
                                p_val = hou.node(node_pre).parm("fileName").eval()
                                pathval[elm] = p_val                          
                            index+=1
                  
                if len(pathval)>2:                     
                    vals = pathval[first_key]
                    same_p = True
                    keys = None
                    for elm in pathval:                          
                        if not pathval[elm] == vals:
                            same_p =False
                            keys = elm
                    if same_p==True:
                        if not os.path.exists(vals):
                            HoudiniUtil.print_times("The cam donot exist on the server!")
                            HoudiniUtil.print_times("Cam: %s" % vals)
                            result = False
                    else:
                        HoudiniUtil.print_times("ABC cam with diffrenct path val")
                        HoudiniUtil.print_times("Base path:\t")
                        HoudiniUtil.print_times("\t> %s" % vals)
                        HoudiniUtil.print_times("\tNode:\t%s\t" % keys)
                        HoudiniUtil.print_times("\t\t> %s" % pathval[keys])
                        result = False
        else:
            result=False
        return result

    
    @staticmethod
    def node_adict_fite():
        import hou
        type_name = ["file","alembic","alembicarchive","tex"]
        file_adict={}
        abc_adict={}
        abc_ipt_adict={}
        tex_adict={}
        for nodes in hou.node("/").allSubChildren():
            nodePath = nodes.path()
            nodePath = nodePath.replace('\\','/')
            nodename=nodes.type().name()
            if nodename in type_name:
                if nodename=="file":
                    file_adict[nodes]=nodePath
                elif nodename=="alembic":
                    abc_adict[nodes]=nodePath
                elif nodename=="alembicarchive":
                    abc_ipt_adict[nodes]=nodePath
                elif nodename=="tex":
                    tex_adict[nodes]=nodePath
        returns = {"file":file_adict,"abc":abc_adict,"abc_ipt":abc_ipt_adict,"tex":tex_adict}
        return returns

    @staticmethod
    def change_dot_val(pathin =''):
        path_arr=pathin.split("/")
        arr_elm=[]
        returnpath=''
        file_exit=True
        get_info = ''
        for i in range(0,len(path_arr)):
            if path_arr[i]=="..":
                arr_elm.append(i)
        if len(arr_elm)>0:
            bigen=arr_elm[0]-len(arr_elm)
            end=arr_elm[-1]
            for i in range(0,len(path_arr)):
                if i==0:
                    returnpath=path_arr[i]
                elif i<bigen or i>end:
                    returnpath+="/"+path_arr[i]
            file_folder = os.path.dirname(returnpath)
            file_base_name = os.path.basename(returnpath)
        else:
            file_folder = os.path.dirname(pathin)
            file_base_name = os.path.basename(pathin)

        return file_folder,file_base_name,returnpath

    @classmethod
    def node_deep_val(cls,node=None,parm='file'):
        check_str = ["ch(","chs("]
        val = node.parm(parm).unexpandedString()
        node_deep_path = node.path()
        # print val
        for elm in check_str:
            if elm in val:
                import hou
                this_path = node.path()
                aim_path_list = cls.change_dot_val(this_path+"/"+val.split('"')[1])
                node_deep = hou.node(aim_path_list[0])
                parm=aim_path_list[1]
                val,node_deep_path=cls.node_deep_val(node_deep,parm)
        return val,node_deep_path


    @classmethod
    def node_type_filte(cls,nodepath='',types=[]):
        import hou
        result = True
        F_node = os.path.dirname(nodepath)
        if not F_node == "/":
            # print F_node
            if hou.node(F_node).type().name() in types:
                # print "pass pass pass pass pass pass..."
                passit = False
                if hou.node(F_node).type().name()=="filecache":
                    if hou.node(F_node).parm("loadfromdisk").eval():
                        passit = True
                if not passit:
                    result = False
            else:
                ## remove bypass node
                bypass = False
                if hasattr(hou.node(F_node),'isBypassed'):
                    if hou.node(F_node).isBypassed():
                        bypass = True
                if bypass:
                    result = False
                else:
                    result = cls.node_type_filte(F_node,types)
        return result