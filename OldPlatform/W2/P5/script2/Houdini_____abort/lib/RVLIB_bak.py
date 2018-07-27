
import sys,os,glob,subprocess,string,re,fnmatch,win32com.client,itertools


def AutoFloatProperties(*props):
    '''metaclass'''
    class _AutoFloatProperties(type):
        # Inspired by autoprop (http://www.python.org/download/releases/2.2.3/descrintro/#metaclass_examples)
        def __init__(cls, name, bases, cdict):
            super(_AutoFloatProperties, cls).__init__(name, bases, cdict)
            for attr in props:
                def fget(self, _attr='_'+attr): return getattr(self, _attr)
                def fset(self, value, _attr='_'+attr): setattr(self, _attr, float(value))
                setattr(cls, attr, property(fget, fset))
    return _AutoFloatProperties

class Vector(object):
    '''Creates a Maya vector/triple, having x, y and z coordinates as float values'''
    __metaclass__ = AutoFloatProperties('x','y','z')
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z # values converted to float via properties

def _RV_retrieveUniqueUserRoot(userid, fullfilename):
    root = _RV_getUserRootFromFileName(userid, fullfilename)
    if root is None:
        buff = _RV_getUserRootFromMapDrive(userid)
        if len(buff)>0:
            for r in buff:
                if os.path.exists(r):
                    root = r
    else:
        if not os.path.exists(root):
            root = None
    return root

def _RV_getUserRootFromFileName(userid, filename):
    root = None
    filedir = os.path.dirname(filename)
    buff = filedir.split(userid)
    if len(buff)>1:
        root = buff[0] + userid
    return root

def _RV_getUserRootFromMapDrive(userid):
    _USER_ROOTS = []
    _DICT_DRIVE_MAPPED_PATHS = getDriveMappings()
    for k in _DICT_DRIVE_MAPPED_PATHS:
        PATH = _DICT_DRIVE_MAPPED_PATHS[k]
        _L_PATH = []
        _L_PATH = PATH.split(userid)
        if len(_L_PATH)>1:
            _User_Root =  _L_PATH[0] + userid
            if _User_Root not in _USER_ROOTS:
                _USER_ROOTS.append(_User_Root)
    return _USER_ROOTS

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.izip_longest(fillvalue=fillvalue, *args)

def getDriveMappings():
    """
    Return a dictionary of drive letter to UNC paths as mapped on the
    system.
    """
    network = win32com.client.Dispatch('WScript.Network')
    # http://msdn.microsoft.com/en-us/library/t9zt39at%28VS.85%29.aspx
    drives = network.EnumNetworkDrives()
    # EnumNetworkDrives returns an even-length array of drive/unc pairs.
    # Use grouper to convert this to a dictionary.
    result = dict(grouper(2, drives))
    # Potentially several UNC paths will be connected but not assigned
    # to any drive letter. Since only the last will be in the
    # dictionary, remove it.
    if '' in result: del result['']
    return result

def getUNCForDrive(drive):
    """
    Get the UNC path for a mapped drive.
    Throws a KeyError if no mapping exists.
    """
    return getDriveMappings()[drive.upper()]

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

def _RV_findAllWithPattern(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def _RV_findAllWithFileName(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result

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
    if skip_flag is not None:
        os.system ("robocopy /S /NDL /NFL %s %s %s" % (fromdir, todir, vname))
        subprocess.call(r"7z x -y -aos " + todir + r"/" + vname + " -o" + runpath)
        os.remove(todir + r"/" + vname)
    return runpath

def _RV_Tool_7z_Setup(_SERVER_IP_ROOT):
    localpath = r"D:/plugins/tools/7z"
    fromdir = _SERVER_IP_ROOT + r"/tools/7-Zip"
    runpath = fromdir
    if not os.path.exists(localpath):
        os.makedirs(localpath)
    os.system ("robocopy /S /NDL /NFL %s %s %s" % (fromdir, localpath, "*"))
    if os.path.exists((localpath+"/7z.exe")) and os.path.exists((localpath+"/7z.dll")):
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
    with open(hip_file, 'r') as src:
        newline = []
        for line in src.readlines():
            if re.match('^set -g _HIP_SAVEVERSION = ', line):
                _HV = re.search("\'.*\'", line).group()[1:-1]
                _VS = _HV.split('.')
                _HV = int(_VS[0] + _VS[1] + _VS[2])

    return _HV