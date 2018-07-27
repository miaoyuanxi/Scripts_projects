#coding=utf-8
# 2017/12/25-18:00-2017
import os,sys,re
import argparse
import shutil
def copy_vrmap(**kwargs):
    render_log =kwargs['render_log']
    vrmap_list = []
    with open(render_log,"r") as l:
        for line in l:
            if line.strip() and "irradiance map" in line:
                p1 = re.compile(r"(?<=Saving irradiance map to file \").+(?=[\',\"])", re.I)
                vrmap_path = p1.findall(line)
                if vrmap_path:
                    vrmap_list.append(vrmap_path[0])
    if vrmap_list:
        for vrmap_path in vrmap_list:
            layer_name = vrmap_path.split("/")[-2]
            p = re.compile(r"Prepass",re.I)
            r = p.findall(layer_name)
            if not r:
                layer_name = layer_name + "_Prepass"
            p = re.compile(r"BOFB(?:_(?:\d)+){3}",re.I)
            r = p.findall(vrmap_path)
            if r:
                shot_num = r[0]
                copy_path ="{}/{}/{}".format("GIMAP",shot_num,layer_name)
            else:
                if ":" in vrmap_path:
                    copy_path = vrmap_path.rsplit(":")[1].rsplit("/",1)[0]
                else:
                    copy_path = vrmap_path.rsplit("/",1)[0]   
        
            copy_path =  kwargs['output']+"/"+copy_path
            print "the vramp copy path is %s " % copy_path
            if not os.path.exists(copy_path):
                os.makedirs(copy_path)
            
            shutil.copy2(vrmap_path, copy_path)
            
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='copy vrmap ')
    parser.add_argument("--ti", dest="task_id", type=int)
    parser.add_argument("--ot", dest="output", type=str)
    parser.add_argument("--rlog", dest="render_log", type=str)
    kwargs = parser.parse_args().__dict__
    copy_vrmap(**kwargs)