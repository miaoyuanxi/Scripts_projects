import os,sys
import hou

def changeval(pathin =''):
    path_arr=pathin.split("/")
    arr_elm=[]
    returnpath=''
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
    else:
        returnpath=pathin
    return returnpath

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
        fileval=changeval(fileval)
        if not os.path.exists(fileval):
            info=fileval.split("/")
            if len(info)>3:
                if not info[1]=="":
                    print("\nWarning: %s" %fileval)
                    print elm 
                    print adict_files[elm]
                    fileinfo+="\nWarning: %s" %fileval+"\n"
            elif len(info)>1:
                print("\nWarning: %s" %fileval)
                print elm 
                print adict_files[elm]
                fileinfo+="\nWarning: %s" %fileval+"\n"
        if visible:
            print elm 
            print adict_files[elm]
            print fileval
        fileinfo+=elm.name()+"\n"+adict_files[elm]+"\n"+fileval+"\n"

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
        fileval=changeval(fileval)
        if not os.path.exists(fileval):
            print("\nWarning: %s" %fileval)
            print elm 
            print abc_adict[elm]
            fileinfo+="\nWarning: %s" %fileval+"\n"
        if visible:
            print elm 
            print abc_adict[elm]
            print fileval
        fileinfo+=elm.name()+"\n"+abc_adict[elm]+"\n"+fileval+"\n"
    for elm in abc_ipt_ad:
        fileval=elm.evalParm("fileName")
        fileval=changeval(fileval)
        if not os.path.exists(fileval):
            print("\nWarning: %s" %fileval)
            print elm 
            print abc_ipt_ad[elm]
            fileinfo+="\nWarning: %s" %fileval+"\n"
        if visible:
            print elm 
            print abc_ipt_ad[elm]
            print fileval
        fileinfo+=elm.name()+"\n"+abc_ipt_ad[elm]+"\n"+fileval+"\n"
    with open(F_path,"w") as f:
        f.write(fileinfo)
        f.close()
# DOFILES()
if __name__=="__main__":
    DOFILES()