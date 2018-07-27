import os,sys
import hou
sys.path.append("B:\plugins\houdini\lib")
import sequence_job

def changeval(pathin ='',node=None,parm="file"):
    path_arr=pathin.split("/")
    arr_elm=[]
    returnpath=''
    file_exit=True
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
        old_base_name = os.path.basename(node.parm(parm).unexpandedString())
        new_path = os.path.join(file_folder,old_base_name)
        #print(old_base_name)
        if os.path.exists(file_folder):
            do=sequence_job.main(file_folder,file_base_name,False)
            if not do=="":
                new_path=new_path.replace("\\","/")
                node.parm(parm).set(new_path)
            else:
                file_exit=False
            returnpath = new_path
        else:
            file_exit=False
    else:
        file_folder = os.path.dirname(pathin)
        file_base_name = os.path.basename(pathin)
        if os.path.exists(file_folder):
            do=sequence_job.main(file_folder,file_base_name,False)
            if do=="":
                file_exit=False
        else:
            print("The file's dirt is not exit!")
            file_exit=False
        returnpath=node.parm(parm).unexpandedString()
    return file_exit,returnpath

def DOFILES(filepath='',visible=0):
    fileinfo=''    
    if not filepath=="":
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        F_path=filepath+"/filesinfo.txt"
    else:
        F_path="D:/"+"filesinfo.txt"
    allnode=hou.node("/obj/").allSubChildren()
    file_adict={}
    abc_adict={}
    abc_ipt_ad={}
    cam_adict={}
    cache_adict={}
    meger_adict={}
    ropnet_adict={}
    ropnet_adict={}
    output_adict={}
    dopio_adict={}
    for nodes in allnode:
        nodePath = nodes.path()
        nodePath = nodePath.replace('\\','/')
        nodename=nodes.type().name()
        if nodename in ["file","alembic","alembicarchive","cam","filecache","filemerge","ropnet",
                        "dopio","output"]:
            if nodename=="file":
                file_adict[nodes]=nodePath
            if nodename=="alembic":
                abc_adict[nodes]=nodePath
            if nodename=="alembicarchive":
                abc_ipt_ad[nodes]=nodePath
            if nodename=="cam":
                cam_adict[nodes]=nodePath
            if nodename=="filecache":
                cache_adict[nodes]=nodePath
            if nodename=="filemerge":
                meger_adict[nodes]=nodePath
            if nodename=="ropnet":
                ropnet_adict[nodes]=nodePath
            if nodename=="output":
                output_adict[nodes]=nodePath
            if nodename=="dopio":
                dopio_adict[nodes]=nodePath

    ### do files
    adict_files={}
    ### remove depth files
    if len(file_adict)>0:
        adict_copy={}
        for elm in file_adict:
            path_a=file_adict[elm].split("/")            
            if not len(path_a)>6:
                adict_copy[elm]=file_adict[elm]
        file_adict=adict_copy
    ### remove abc
    if len(abc_ipt_ad)>0:
        adict_copy={}
        for elm in file_adict:
            path_a=file_adict[elm].split("/")
            for aim in abc_ipt_ad:
                if not aim.name() in path_a:
                    adict_copy[elm]=file_adict[elm]
        file_adict=adict_copy
    ### remove cam
    if len(cam_adict)>0:
        adict_copy={}
        for elm in file_adict:
            path_a=file_adict[elm].split("/")
            for aim in cam_adict:
                if not aim.name() in path_a:
                    adict_copy[elm]=file_adict[elm]
        file_adict=adict_copy
    ### remove cache
    if len(cache_adict)>0:
        adict_copy={}
        for elm in file_adict:
            path_a=file_adict[elm].split("/")
            for aim in cache_adict:
                if not aim.name() in path_a:
                    adict_copy[elm]=file_adict[elm]
        file_adict=adict_copy
    ### remove merge
    if len(meger_adict)>0:
        adict_copy={}
        for elm in file_adict:
            path_a=file_adict[elm].split("/")
            for aim in meger_adict:
                if not aim.name() in path_a:
                    adict_copy[elm]=file_adict[elm]
        file_adict=adict_copy
    ### remove output
    if len(output_adict)>0:
        adict_copy={}
        for elm in file_adict:
            path_a=file_adict[elm].split("/")
            for aim in output_adict:
                if not aim.name() in path_a:
                    adict_copy[elm]=file_adict[elm]
        file_adict=adict_copy

    ### remove dopio
    if len(dopio_adict)>0:
        adict_copy={}
        for elm in file_adict:
            path_a=file_adict[elm].split("/")
            for aim in dopio_adict:
                if not aim.name() in path_a:
                    adict_copy[elm]=file_adict[elm]
        file_adict=adict_copy

    adict_files=file_adict
    print "Files with %d" % len(adict_files)
    fileinfo+="Files with %d" % len(adict_files)+"\n"
    for elm in adict_files:
        fileval=elm.evalParm("file")
        fileval=changeval(fileval,elm,"file")
        if not fileval[0]:
            info=fileval[1].split("/")
            if len(info)>3:
                if not info[1]=="":
                    print("Warning: %s" %fileval[1])
                    print elm 
                    print adict_files[elm]
                    print("\n")
                    fileinfo+="\nWarning: %s" %fileval[1]+"\n"
            elif len(info)>1:
                print("Warning: %s" %fileval[1])
                print elm 
                print adict_files[elm]
                print("\n")
                fileinfo+="\nWarning: %s" %fileval[1]+"\n"
        if visible:
            print elm 
            print adict_files[elm]
            print fileval[1]
        fileinfo+=elm.name()+"\n"+adict_files[elm]+"\n"+fileval[1]+"\n"

    ### do abc
    if len(ropnet_adict)>0:
        adict_copy={}
        for elm in abc_adict:
            path_a=abc_adict[elm].split("/")
            for aim in ropnet_adict:
                if not aim.name() in path_a:
                    adict_copy[elm]=abc_adict[elm]
        abc_adict=adict_copy
    print "\nThe abc files: %d " % (len(abc_adict)+len(abc_ipt_ad))
    fileinfo+="\nThe abc files: %d " % (len(abc_adict)+len(abc_ipt_ad))+"\n"
    for elm in abc_adict:
        fileval=elm.evalParm("fileName")
        fileval=changeval(fileval,elm,"fileName")
        if not fileval[0]:
            print("Warning: %s" %fileval[1])
            print elm 
            print abc_adict[elm]
            print("\n")
            fileinfo+="\nWarning: %s" %fileval[1]+"\n"
        if visible:
            print elm 
            print abc_adict[elm]
            print fileval[1]
        fileinfo+=elm.name()+"\n"+abc_adict[elm]+"\n"+fileval[1]+"\n"
    for elm in abc_ipt_ad:
        fileval=elm.evalParm("fileName")
        fileval=changeval(fileval,elm,"fileName")
        if not fileval[0]:
            print("Warning: %s" %fileval[1])
            print elm 
            print abc_ipt_ad[elm]
            print("\n")
            fileinfo+="\nWarning: %s" %fileval[1]+"\n"
        if visible:
            print elm 
            print abc_ipt_ad[elm]
            print fileval[1]
        fileinfo+=elm.name()+"\n"+abc_ipt_ad[elm]+"\n"+fileval[1]+"\n"
    with open(F_path,"w") as f:
        f.write(fileinfo)
        f.close()
# DOFILES()
if __name__=="__main__":
    DOFILES()