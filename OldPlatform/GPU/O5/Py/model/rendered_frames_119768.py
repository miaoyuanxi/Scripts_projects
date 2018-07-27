# ! /usr/bin/env python
# coding=utf-8
import os,sys
import re
import time
import shutil
import collections
try:
    import pymel.core as pm
    #reload(pm)
except Exception as e:
    pass
print "post render"
def set_rendered_frame(save_path,task_id="",rd="",use_id=""):
    print "the cfg path ++++++++++> %s " % save_path
    print "the task id is ============> %s"  % task_id
    print "the rd_path is ============> %s"  % rd

    pycfg =r"//10.90.100.101/p5/temp/{}_render/cfg/py.cfg".format(task_id)
    print "the pycfg_path is ============> %s"  % pycfg
    
    #pycfg="d:/py.cfg"
    currentTime = str(int(pm.currentTime()))
    
    G_JOB_NAME=os.environ.get('G_JOB_NAME')

    fee_file_name = "{}-{}-{}.txt".format(use_id,task_id,G_JOB_NAME)
    fee_file = "c:/work/render/{}/{}".format(task_id,fee_file_name)
    print fee_file
    if os.path.exists(pycfg):
        print "pycfg"
        pycfg_dict = {}
        with open(pycfg,"r") as pycfg:
            for line in pycfg:
                    if "=" in line:
                        exec(line)
    print G_PATH_COST
    p  = re.compile(r"[0-9]+(?=[^0-9]*$)" ,re.I)               
    if rd:
        copy_image_list=[]      
        rd = rd.replace('\\',"/")
        
        for parent,dirnames,filenames in os.walk(rd):
            for filename in filenames:
                print filename
                r= p.findall(filename)
                if r:
                    #print r
                    frame= r[-1]
                    strs = "nume = '{}'.zfill({})".format(currentTime,len(frame))
                    exec("%s" % strs)
                    #print nume
                    fr = re.findall(nume,filename)
                    if fr and not filename.endswith(".lock"):
                        #print fr              
                        copy_image_list.append(os.path.join(parent,filename))
        print copy_image_list
        if len(copy_image_list) > 0:
            for image in copy_image_list:            
                copy_image(image,rd,G_PATH_USER_OUTPUT)
            write_fee(fee_file,G_PATH_COST)
            with open(save_path + "/" + currentTime, "w"):
                ''
        else:
            sys.exit(1)
    else:
        copy_image(image,rd,G_PATH_USER_OUTPUT)
        write_fee(fee_file,G_PATH_COST)
        with open(save_path + "/" + currentTime, "w"):
            ""

def write_fee(fee_file,G_PATH_COST):
    if not os.path.exists(G_PATH_COST):
        print "G_PATH_COST donot exists {}  ".format(G_PATH_COST)
        os.makedirs(G_PATH_COST)
        
    endTime = int(time.time())
    print  "the end tiime is {}".format(endTime)
    # G_PATH_COST+="\\"
    # G_PATH_COST = G_PATH_COST.replace("\\","/")
    print G_PATH_COST
    
    fee_dict = collections.OrderedDict()
    with open(fee_file,"r") as l:
        for line in l:
            if "=" in line:
                line_split = line.split("=")
                fee_dict[line_split[0].strip()] = line_split[1].strip()

    if 'endTime' in fee_dict:
        print "endTime"
        #print os.path.exists(r'C:/work/munu_client/munu_agent/gpu/script')
          
        shutil.copy2(fee_file, G_PATH_COST)
        fee_dict.pop('endTime')
        fee_dict['startTime'] = endTime
        with open(fee_file,"w") as l:
            for i in fee_dict:
                l.write("{}={}\n".format(i,fee_dict[i]))
    else:
        print "startTime"                
        fee_dict['endTime'] = endTime
        with open(fee_file,"w") as l:
            for i in fee_dict:
                l.write("{}={}\n".format(i,fee_dict[i]))
        shutil.copy2(fee_file, G_PATH_COST)
        fee_dict.pop('endTime')
        fee_dict['startTime'] = endTime
        with open(fee_file, "w") as l:
            for i in fee_dict:
                l.write("{}={}\n".format(i, fee_dict[i]))        

def copy_image(image,rd,G_PATH_USER_OUTPUT):
    image = os.path.normpath(image)
    rd = os.path.normpath(rd)
    G_PATH_USER_OUTPUT = os.path.normpath(G_PATH_USER_OUTPUT)
    G_PATH_USER_OUTPUT = image.replace(rd,G_PATH_USER_OUTPUT).rsplit('\\',1)[0]  
    
    if not os.path.exists(G_PATH_USER_OUTPUT):
        print "donot "
        os.makedirs(G_PATH_USER_OUTPUT)        
    
    print "copy_image"
    print "copy image {} to {} " .format(image,G_PATH_USER_OUTPUT)
    
    shutil.copy2(image, G_PATH_USER_OUTPUT)

def get_rendered_frames(save_path):
    # "C:\Program Files\Autodesk\Maya2014\bin\render.exe" -rd "c:\test" -postFrame "python \"execfile(\\\"C:/Users/admin/Documents/GitHub/rayvision-websubmit/rendered_frames.py\\\");set_rendered_frame(\\\"C:/test/rendered_frames\\\")\"" E:\test_files\2014_ball.ma
    if os.path.exists(save_path):
        return [int(i) for i in os.listdir(save_path) if i.isalnum()]
    return []


def get_retry_frames(start, end, save_path):
    # execfile("C:/Users/admin/Documents/GitHub/rayvision-websubmit/rendered_frames.py")
    # get_retry_frames(1, 10, save_path)
    rendered = get_rendered_frames(save_path)
    return [i for i in range(int(start), int(end) + 1) if i not in rendered]
def del_frames(start, end, save_path):
    if os.path.exists(save_path):
        for i in os.listdir(save_path):
            if i.isalnum() and int(i) in range(int(start), int(end) + 1):
                os.remove(save_path + "/" + i)
