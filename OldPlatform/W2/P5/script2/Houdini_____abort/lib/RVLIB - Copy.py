import sys,os,subprocess,string,re,time,shutil
_PATH_ORG = os.environ.get('PATH')
os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";C:\Windows\system32"

def _RV_retrieveUniqueUserRoot(userid, fullfilename):
    root = _RV_getUserRootFromFileName(userid, fullfilename)
    return root

def _RV_getUserRootFromFileName(userid, filename):
    root = None
    filedir = os.path.dirname(filename)
    buff = filedir.split(userid)
    if len(buff)>1:
        root = buff[0] + userid
    return root

def _RV_filePath_Dir_Match_Counts(src_dir, tar_dir):
    # file path dir match count
    # be aware that file path dir order is not taken into consideration
    i = 0
    src_dir = src_dir.replace("\\","/")
    src_dirs = src_dir.split("/")
    tar_dir = tar_dir.replace("\\","/")
    tar_dirs = tar_dir.split("/")
    
    for d in src_dirs:
        if d in tar_dirs:
            i += 1
    
    return i

def _RV_fileName_Dir_Match_Counts(pmv_bn_no_ext, pmv_ext, pmv_dir, this_ffileName):
    # file base has to be the same
    # if yes, check file path dir match count
    # be aware that file path dir order is not taken into consideration
    # case ignore
    
    i = -1
    f_dir = os.path.dirname(this_ffileName)
    f_dir = f_dir.replace("\\","/")
    f_dirs = f_dir.split("/")
    pmv_dir = pmv_dir.replace("\\","/")
    pmv_dirs = pmv_dir.split("/")
    f_bn_ext = os.path.basename(this_ffileName)
    f_bn_no_ext = os.path.splitext(os.path.basename(this_ffileName))[0]
    f_ext = os.path.splitext(os.path.basename(this_ffileName))[1]
    if f_bn_no_ext == pmv_bn_no_ext and f_ext == pmv_ext:
        i = 0
        for d in f_dirs:
            if d in pmv_dirs:
                i += 1
    return i

def _RV_App_Hou_Env_Setup(runpath, pyvd, pyvnd):
    os.environ['HFS'] = runpath
    _PATH_ORG = os.environ.get('PATH')
    os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";" + runpath + "/bin"
    libpath = "%s/houdini/python%slibs" % (runpath, pyvd)
    _PATH_New = os.environ.get('PATH')
    print _PATH_New
    sitepath = "%s/python%s/lib/site-packages" % (runpath, pyvnd)
    if libpath not in sys.path:
        sys.path.append(libpath)
    if sitepath not in sys.path:
        sys.path.append(sitepath)

def _RV_App_Hou_Setup(_SERVER_IP_ROOT, vers, skip_flag):
    fromdir = _SERVER_IP_ROOT + r"/plugins/houdini/apps/7z"
    vname = vers + ".7z"
    todir = r"D:/plugins/houdini"
    runpath = todir + r"/" + vers
    z7 = "D:/plugins/tools/7z/7z.exe"

    if skip_flag is not None:
        os.system ("robocopy /S /NDL /NFL %s %s %s" % (fromdir, todir, vname))
        cmd_un7z = z7 + " x -y -aos " + todir + r"/" + vname + " -o" + runpath
        subprocess.check_output(cmd_un7z, shell=True)
        #os.system("\"" + cmd_un7z + "\"")
        os.remove(todir + r"/" + vname)
    return runpath

def _RV_Tool_7z_Setup(_SERVER_IP_ROOT):
    localpath = r"D:/plugins/tools/7z"
    z7 = "D:/plugins/tools/7z/7z.exe"
    fromdir = _SERVER_IP_ROOT + r"/tools/7-Zip"
    runpath = fromdir
    os.system ("robocopy /S /NDL /NFL %s %s %s" % (fromdir, localpath, "*"))
    runpath = localpath
    _PATH_ORG = os.environ.get('PATH')
    os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";" + runpath
    return runpath

def _RV_App_OTL_Path_Setup(hip_file):
    hipvar = os.path.dirname(hip_file)
    otlpath = r"@/otls"
    for (dirpath, dirname, filename) in os.walk(hipvar):
        dir = dirpath.replace("\\", "/")
        if re.search('otl', dir, re.IGNORECASE):
            otlpath += r";" + dir
    otlpath_included = os.environ.get('HOUDINI_OTLSCAN_PATH')
    os.environ['HOUDINI_OTLSCAN_PATH'] = (otlpath_included if otlpath_included else "") + r";" + otlpath
    otlpath_included = os.environ.get('HOUDINI_OTLSCAN_PATH')
    return otlpath_included

def _RV_getBestFitHOUVersionFromHip(_SERVER_IP_ROOT, hip_file):
    fromdir = _SERVER_IP_ROOT + r"/plugins/houdini/apps/7z"
    localpath = r"D:/plugins/houdini"
    ver = 0
    ver_str = r"NULL"
    ver = _RV_getHOUSaveVersion(hip_file)
    print "ver _____"
    print ver
    avs = _RV_getHOUAvailableVersion(fromdir)
    if ver not in avs:
        MD = 999999999
        VV = 0
        for V in avs:
            d = V - ver
            if d>0 and d < MD:
                MD = d
                VV = V
        ver = VV
    ver_str = str(ver)
    print "ver_str _____"
    print ver_str
    return ver_str

def _RV_getHOUAvailableVersion(thisPath):
    _L_FileName = []
    _V_Int_FileName = []
    for (dirpath, dirnames, filenames) in os.walk(thisPath):
        _L_FileName.extend(filenames)
    for F in _L_FileName:
        V = os.path.splitext(os.path.basename(F))[0]
        if V not in _V_Int_FileName:
            _V_Int_FileName.append(int(V))
    return _V_Int_FileName

def _RV_getHOUSaveVersion(hip_file):

    _HV = 0
    with open(hip_file, 'rb') as src:
        newline = []
        for line in src.readlines():
            if re.match('^set -g _HIP_SAVEVERSION = ', line):
                _HV = re.search("\'.*\'", line).group()[1:-1]
                _VS = _HV.split('.')
                _HV = int(_VS[0] + _VS[1] + _VS[2])

    return _HV
    
def hou_lic(houdini_vis,HS_ip):
    strcmd = 'sc query HoudiniLicenseServer|findstr "STATE"'
    HLS_popen = subprocess.Popen(strcmd, stdout=subprocess.PIPE, shell=1)
    HLS = HLS_popen.stdout.read()
    HLS_popen.wait()
    
    HLS_src = os.path.join(r"b:\plugins\houdini\lic", houdini_vis, "sesinetd.exe")
    HLS_dst = os.path.join("C:\Windows\System32", "sesinetd.exe")
    HLS_stop_cmd = 'SC STOP "HoudiniLicenseServer"'
    HLS_start_cmd = 'SC start "HoudiniLicenseServer"'
    HLS_creat_cmd = "sc create HoudiniLicenseServer binPath= " + HLS_dst + " START= auto " + " DISPLAYNAME= HoudiniLicenseServer " + " TYPE= own "
    
    if len(HLS) > 5 and HLS.find("STATE"):
        print "the HoudiniLicenseServer is exist"
        HLS_stop_popen = subprocess.Popen(HLS_stop_cmd, stdout=subprocess.PIPE, shell=1)
        HLS_stop_popen.wait()
        time.sleep(5)
        shutil.copy(HLS_src, HLS_dst)
    else:
        print "the HoudiniLicenseServer is not  exist"
        shutil.copy(HLS_src, HLS_dst)
        HLS_creat_popen = subprocess.Popen(HLS_creat_cmd, stdout=subprocess.PIPE, shell=1)
        HLS_creat_popen.wait()
        time.sleep(3)
    HLS_start_popen = subprocess.Popen(HLS_start_cmd, stdout=subprocess.PIPE, shell=1)
    HLS_start_popen.wait()
    time.sleep(3)
    
    HS_strcmd = 'sc query HoudiniServer|findstr "STATE"'
    HS_popen = subprocess.Popen(HS_strcmd, stdout=subprocess.PIPE, shell=1)
    HS = HS_popen.stdout.read()
    HS_popen.wait()
    
    HS_src = os.path.join(r"b:\plugins\houdini\lic", houdini_vis, "hserver.exe")
    HS_dst = os.path.join("C:\Windows\System32", "hserver.exe")
    
    HS_stop_cmd = 'SC STOP "HoudiniServer"'
    HS_start_cmd = 'SC start "HoudiniServer"'
    HS_creat_cmd = "SC create HoudiniServer binPath= " + HS_dst + " START= auto " + " DISPLAYNAME= HoudiniServer " + " TYPE= own "
    HS_s_ip_cmd = HS_dst + " -S " + HS_ip
    
    if len(HS) > 5 and HS.find("STATE"):
        print "the HoudiniServer is exist"
        HS_stop_popen = subprocess.Popen(HS_stop_cmd, stdout=subprocess.PIPE, shell=1)
        HS_stop_popen.wait()
        time.sleep(10)
        shutil.copy(HS_src, HS_dst)
    else:
        print "the HoudiniServer is not  exist"
        shutil.copy(HS_src, HS_dst)
        HS_creat_popen = subprocess.Popen(HS_creat_cmd, stdout=subprocess.PIPE, shell=1)
        HS_creat_popen.wait()
        time.sleep(10)
    
    HS_start_popen = subprocess.Popen(HS_start_cmd, stdout=subprocess.PIPE, shell=1)
    print "HS_start_popen     " +  HS_start_popen.stdout.read()
    HS_start_popen.wait()
    time.sleep(15)
    
    HS_s_ip_cmd_popen = subprocess.Popen(HS_s_ip_cmd, stdout=subprocess.PIPE, shell=1)
    print "HS_s_ip_cmd_popen     " +  HS_s_ip_cmd_popen.stdout.read()
    HS_s_ip_cmd_popen.wait()
    time.sleep(15)
    os.system(HS_s_ip_cmd)
    time.sleep(15)
    #print "the houdini  hserver is 10.50.10.231"