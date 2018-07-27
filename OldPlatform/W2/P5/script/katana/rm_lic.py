import socket,os,shutil
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
    else:
        fileId =  (int(IP_num)-int(IP_num[-2:])+1)
    fileId="%03d" %  fileId
    file_name=IP[0]+"_"+IP[1]+"_"+IP[2]+"_"+fileId
    prm_sou_path=prm_path+file_name+"/"+'pixar.license'
    print prm_sou_path
    prm_des_path="/opt/pixar/pixar.license"
    
    shutil.copy(prm_sou_path, prm_des_path)
    return lambda x: x+20
lambda_test=copy_lic()
lambda_test(1)

