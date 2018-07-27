
# /usr/bin/env python
import socket,os,shutil,sys
#os.environ['PIXAR_LICENSE_FILE'] =r'/opt/pixar/license/20/pixar.license'
#print '/opt/pixar/license/20/pixar.license*********' 
katana_com_id=sys.argv[1]
kantan_task_is=sys.argv[2]

katana_script  = sys.argv[3]
katana_scene  = sys.argv[4]
katana_ana_txt=sys.argv[5]
kantan_root = "/opt/foundry/katana"
#kantan_root = "/home/ladaojeiang/yes"
#PIXAR_LICENSE_FILE=/opt/pixar/license/20/pixar.license
def lic_set():
    if not os.environ.has_key('PIXAR_LICENSE_FILE'):
        print '/opt/pixar/license/20/pixar.license------888'  
        os.environ['PIXAR_LICENSE_FILE'] =r'/opt/pixar/license/20/pixar.license'
        #return lambda x: x+5
def copy_lic():
    prm_path="/mnt_rayvision/p5/script/katana/prm_lic/"
    print os.path.exists(prm_path)
    if os.path.exists(prm_path)==False:
        print 'mount mnt_rayvision is fail'
        #break

    localIP = socket.gethostbyname(socket.gethostname())
    print "local ip:%s "%localIP
    IP=localIP.split('.')

    #IP_node=IP[2]
    IP_num=IP[3]
    #IP_num='50'
    #print IP_node,IP_num

    if int(IP_num[-2:])>50 and int(IP_num)%50 != 0:
        fileId = (int(IP_num)-int(IP_num[-2:])+50)
    elif IP_num[-2:]=='00':
        fileId =  (int(IP_num)-int(IP_num[-2:])-50)
    else:
        fileId =  (int(IP_num)-int(IP_num[-2:])+1)

    fileId="%03d" %  fileId
    file_name=IP[0]+"_"+IP[1]+"_"+IP[2]+"_"+fileId

    prm_sou_path=prm_path+file_name+"/"+'pixar.license'
    print prm_sou_path
    prm_des_path="/opt/pixar/pixar.license"
    
    shutil.copy(prm_sou_path, prm_des_path)
    return True  

def kanana_analyse_sys(kantan_root,katana_script,katana_scene,katana_ana_txt):
   
    
    os.system(r'%s/katana --script %s %s  %s' % (kantan_root,katana_script,katana_scene,katana_ana_txt))
    if  os.path.exists(katana_ana_txt):
        return 1
    else:
        return 0
#os.environ['PIXAR_LICENSE_FILE'] =r'/opt/pixar/license/20/pixar.license'
#print '/opt/pixar/license/20/pixar.license-------' 

def katan_fenxi(kantan_root,katana_script,katana_scene,katana_ana_txt):
    if copy_lic():
        kanana_analyse_sys(kantan_root,katana_script,katana_scene,katana_ana_txt)
katan_fenxi(kantan_root,katana_script,katana_scene,katana_ana_txt)
