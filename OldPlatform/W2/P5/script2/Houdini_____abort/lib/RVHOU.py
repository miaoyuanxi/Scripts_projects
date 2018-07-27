import sys,os,string,re
import hou
import RVLIB
_PATH_ORG = os.environ.get('PATH')
os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";C:\Windows\system32"

def _RV_write_ROPS_Frame_Info(INF, _HIP_BASENAME):
    info = ''
    i = 0
    print "\nSEARCHING GEOMETRY ROPS ..."
    for obj in hou.node('/').allSubChildren():
        objPath = obj.path()
        objPath = objPath.replace('\\','/')
        objTypeName = obj.type().name()
        if objTypeName in ['geometry','rop_geometry']:
            render_rop_Node = hou.node(objPath)
            if render_rop_Node.parm("execute"):
                print "    GEOMETRY ROP: %s" % render_rop_Node
                if i>0: info += '\n'
                info += objPath
                info += '|' + str(obj.evalParm('f1'))
                info += '|' + str(obj.evalParm('f2'))
                info += '|' + str(obj.evalParm('f3'))
                info += '|' + '0'
                i+=1
    
    
    print "\nSEARCHING RENDER ROPS ..."
    rop_cunt=0
    for obj in hou.node('/').allSubChildren():        
        objPath = obj.path()
        objPath = objPath.replace('\\','/')
        objTypeName = obj.type().name()
        #print objTypeName
        if objTypeName in ['ifd', 'arnold','Redshift_ROP']:
            render_rop_Node = hou.node(objPath)
            print "    RENDER ROP: %s" % render_rop_Node
            if i>0: info += '\n'
            info += objPath
            info += '|' + str(obj.evalParm('f1'))
            info += '|' + str(obj.evalParm('f2'))
            info += '|' + str(obj.evalParm('f3'))
            info += '|' + '-1'
            i+=1
            rop_cunt+=1
    print("Total ROPs: %s" % rop_cunt)
    
    print "\nSEARCHING SIMULATION ROPS ..."
    for obj in hou.node('/').allSubChildren():
        objPath = obj.path()
        objPath = objPath.replace('\\','/')
        objTypeName = obj.type().name()
        if objTypeName in ['hq_sim']:
            hq_sim_Node = hou.node(objPath)
            print "    SIMULATION ROP: %s" % hq_sim_Node
            
            #hq_sim_controls
            hq_sim_ctrl_path = str(obj.evalParm('hq_sim_controls'))
            hq_sim_ctrl_Node = hou.node(hq_sim_ctrl_path)
            print "    SIMULATION CTRL: %s" % hq_sim_ctrl_Node
            
            #hq_driver
            hq_driver_path = str(obj.evalParm('hq_driver'))
            hq_driver_Node = hou.node(hq_driver_path)
            sf,ef,bf = _getFrameRangeFromRop(hq_driver_Node)
            
            '''
            output = hq_driver_Node.evalParm('sopoutput')
            file_extension = os.path.splitext(output)[-1]
            hq_driver_nodeName = hq_driver_Node.name()
            cache_name = '$HIP/__sim_cache/' + _HIP_BASENAME + '__' + str(hq_driver_nodeName) + '.$SLICE.$F' + file_extension
            hq_driver_Node.parm('sopoutput').set(cache_name)
            '''
            
            #slice_type
            n_slice_type = str(obj.evalParm('slice_type'))
            slice_type_name = '-1'
            if n_slice_type == '0':
                slice_type_name = 'Volume Slice'
            if n_slice_type == '1':
                slice_type_name = 'Particle Slice'
            print "    PARTITONING_TYPE: %s" % slice_type_name
            
            if n_slice_type in ['0', '1']:
                nof_slices = 0
                if n_slice_type=='1':
                    nof_slices = int(obj.evalParm('num_slices'))
                    print ("here print the numner of slices")
                    print (nof_slices)
                else:
                    #slicediv1 slicediv2 slicediv3
                    slice_div_1 = int(obj.evalParm('slicediv1'))
                    slice_div_2 = int(obj.evalParm('slicediv2'))
                    slice_div_3 = int(obj.evalParm('slicediv3'))
                    nof_slices = slice_div_1 * slice_div_2 * slice_div_3
                print "    TOTAL SLICE: %s" % str(nof_slices)
                if nof_slices>0:
                    for j in range(nof_slices):
                        if i>0: info += '\n'
                        info += hq_driver_path
                        info += '|' + str(sf)
                        info += '|' + str(ef)
                        info += '|' + str(bf)
                        info += '|' + str(j)
                        i+=1
                        print "    %s @ %s" % (hq_driver_path, str(j))

    if info is not None:
        _inf_handler = file(INF, 'w')
        _inf_handler.write(info)
        _inf_handler.close()
    else:
        print("Warning: there is not any rop in this file!")

def _RV_geometrySetup(_ROP, _SFM, _EFM, _BFM, _SLICE_NUM, _HIP_BASENAME):
    print '\nGEOMETRY SETUP ...'
    _geometry_Node = hou.node(_ROP)
    return _geometry_Node

def _RV_simulationSetup(_ROP, _SFM, _EFM, _BFM, _SLICE_NUM, _HIP_BASENAME):
    print '\nSIMULATION SETUP ...'
    hq_driver_Node = hou.node(_ROP)
    print "    ROP: %s" % hq_driver_Node
    
    sf = int(_SFM)
    ef = int(_EFM)
    bf = int(_BFM)
    #frame_range = _getFrameRangeFromRop(hq_driver_Node)
    _setParmInROPChain(hq_driver_Node, "trange", 1)
    _setParmInROPChain(hq_driver_Node, "f", (sf, ef, bf))
    
    hou.hscript("setenv SLICE=" + str(_SLICE_NUM))
    hou.hscript("varchange")
    print "    SLICE NUMBER: %s" % _SLICE_NUM
    sf,ef,bf = _getFrameRangeFromRop(hq_driver_Node)
    print "    FRAME RANGE: %s~%s-%s" % (str(sf), str(ef), str(bf))
    output = hq_driver_Node.evalParm('sopoutput')
    print "    OUTPUT AS: %s" % output
    
    return hq_driver_Node

def _RV_renderSetup(_ROP, _SFM, _EFM, _BFM, _RRD, _HIP_BASENAME):
    print '\nRENDER SETUP ...'
    _rop_Node = None
    for obj in hou.node('/').allSubChildren():
        objTypeName = obj.type().name()
        objName = obj.name()
        objPath = obj.path()
        objPath = objPath.replace("\\", "/")
        sras = []
        if objTypeName in ['geometry']:
            if objPath == _ROP:
                _rop_Node = hou.node(_ROP)
                break
        elif objTypeName in ['ifd','arnold','Redshift_ROP']:
            if objPath == _ROP:
                _ROP_NAME = objName
                _PIC_TYPE = 'vm_picture'
                _ATT_LOGLEVEL = 'vm_verbose'
                _PIC_NAME_NEW = 'null'
                _PIC_EXTENSION = 'exr'
                
                if not os.environ.has_key('_ext'):
                    _ext=''
                else:
                    _ext= os.environ.get('_ext')
                
                if objTypeName == 'arnold':
                    _PIC_TYPE = 'ar_picture'
                
                if objTypeName == 'Redshift_ROP':
                    _PIC_TYPE = 'RS_outputFileNamePrefix'
                
                _PIC_NAME_ORG = obj.evalParm(_PIC_TYPE)
                print ('	_PIC_NAME_ORG == ' + _PIC_NAME_ORG + '\r')
                if objTypeName == 'Redshift_ROP':
                    if _PIC_NAME_ORG=='(not set)' or _PIC_NAME_ORG=='':
                        if not obj.evalParm("RS_outputEnable"):
                            obj.parm("RS_outputEnable").set(True)
                            _PIC_NAME_ORG="default.$F4.exr"
                    if obj.parm("RS_renderToMPlay")==1:
                        obj.parm("RS_renderToMPlay").set(0)
                # set log leve
                if  objTypeName in ['ifd','arnold']:
                    if obj.parm(_PIC_TYPE).isLocked():
                        obj.parm(_PIC_TYPE).lock(False)
                    if obj.parm(_ATT_LOGLEVEL).isLocked():
                        obj.parm(_ATT_LOGLEVEL).lock(False)
                    obj.parm(_ATT_LOGLEVEL).set(4)
                if  objTypeName in ['Redshift_ROP']:
                    if obj.parm("EnableDebugCapture").eval()==0:
                        obj.parm("EnableDebugCapture").set(1)
                        print("Turn on debug")

                
                _vp =hou.hscript("opparm -d  "+_ROP+ " "+_PIC_TYPE)
                print ('	_vp == ' + _vp[0] + '\r')
                
                _picture_this=_vp[0].split("(")[-1].split(")")[0].replace("'","").replace('\\', '/').strip() 
                _picture_this=_vp[0].split(_PIC_TYPE)[-1][4:-4]
                print len(_picture_this)
                _picture_this=_picture_this.replace('\\', '/').strip()
                print ('	_picture_this == ' + _picture_this + '\r')
                _picture_this=_picture_this.replace('\\', '/').strip() 
                if _picture_this !='' and _picture_this != 'ip' and _picture_this != 'md' and _ext =='' :

                    _picture_new =_picture_this.replace(_picture_this.split("/")[0],_RRD,1)
                    
                    print ('	_picture_new == ' +str(1)+ _picture_new + '\r')	
                elif _picture_this !='' and _picture_this != 'ip' and _picture_this != 'md' and _ext != '':
                    _pictureSplit_this= os.path.splitext(_picture_this)
                    _PIC_EXTENSION = _pictureSplit_this.split('.')[-1]
                    print str(2)+_pictureSplit_this[0]

                    _picture_new =_pictureSplit_this[0].replace(_pictureSplit_this[0].split("/")[0],_RRD,1)+_pictureSplit_this[1].replace(_PIC_EXTENSION, _ext)
                    print ('	_picture_new == ' +str(2)+ _picture_new + '\r')
                else:
                    _PIC_EXTENSION="exr"
                    _picture_new = _RRD + _HIP_BASENAME+'/' +_ROP_NAME +'/' +  _ROP_NAME + '.`padzero(4,$F)`.' + _PIC_EXTENSION
                    print ('	_picture_new == ' +str(3)+ _picture_new + '\r')              

                # output name setup
                #if _PIC_NAME_ORG !='' and _PIC_NAME_ORG != 'ip':
                # _PIC_NAME_ORG = _PIC_NAME_ORG.replace('\\', '/')
                # _PIC_SHORT_NAME = _PIC_NAME_ORG.split('/')[-1]
                # _PIC_EXTENSION = _PIC_SHORT_NAME.split('.')[-1]
                # _PIC_NAME_NEW = _RRD + _HIP_BASENAME + '.' + _ROP_NAME + '.`padzero(4,$F)`.' + _PIC_EXTENSION
                obj.parm(_PIC_TYPE).set(_picture_new)
                _THIS_PIC_NAME_NEW = obj.evalParm(_PIC_TYPE)
                _THIS_PIC_NAME_NEW_path =  os.path.split(_THIS_PIC_NAME_NEW)[0]
                
                if os.path.exists(_THIS_PIC_NAME_NEW_path)==False:
                    print ('    _THIS_PIC_NAME_NEW_path AS: ' + _THIS_PIC_NAME_NEW_path + '\r')
                    os.makedirs(_THIS_PIC_NAME_NEW_path)
                print ('    REDIRECT AS: ' + _THIS_PIC_NAME_NEW + '\r')

                # deep output setup
                if objTypeName == 'ifd':
                    _DOP_PIC_TYPE = 'null'
                    
                    _DOP_TYPE = obj.evalParm('vm_deepresolver')
                    if _DOP_TYPE == 'camera':
                        _DOP_PIC_TYPE = 'vm_dcmfilename'
                    if _DOP_TYPE == 'shadow':
                        _DOP_PIC_TYPE = 'vm_dsmfilename'
                    if _DOP_TYPE in ['camera','shadow']:
                        if obj.parm(_DOP_PIC_TYPE).isLocked():
                            obj.parm(_DOP_PIC_TYPE).lock(False)
                        _DOP_PIC_NAME_ORG = obj.evalParm(_DOP_PIC_TYPE)
                        _DOP_PIC_EXTENSION = _DOP_PIC_NAME_ORG.replace('\\', '/').split('/')[-1].split('.')[-1]
                        _DOP_FOLDER = 'deep' + '_' + _DOP_TYPE
                        _DOP_DIR = _RRD + _DOP_FOLDER
                        if not os.path.exists(_DOP_DIR):
                            os.makedirs(_DOP_DIR)
                        _DOP_PIC_NAME_NEW = _DOP_DIR + '/' + _HIP_BASENAME + '.' + _ROP_NAME + '.' + _DOP_FOLDER + '.`padzero(4,$F)`.' + _DOP_PIC_EXTENSION
                        obj.parm(_DOP_PIC_TYPE).set(_DOP_PIC_NAME_NEW)
                        _THIS_DOP_PIC_NAME_NEW = obj.evalParm(_DOP_PIC_TYPE)
                        print ('    DEEP REDIRECT AS: ' + _THIS_DOP_PIC_NAME_NEW + '\r')
                
                # frame range setup
                SFM = float(_SFM)
                EFM = float(_EFM)
                BFM = float(_BFM)
                print ('    RENDERING '+ _ROP + ' @ ' + str(SFM) + '~' + str(EFM) + '-' + str(BFM))
                if obj.parm('f1').isLocked():
                    obj.parm('f1').lock(False)
                if obj.parm('f2').isLocked():
                    obj.parm('f2').lock(False)
                if obj.parm('f3').isLocked():
                    obj.parm('f3').lock(False)
                obj.parm('f1').deleteAllKeyframes()
                obj.parm('f2').deleteAllKeyframes()
                obj.parm('f3').deleteAllKeyframes()
                SF = float(obj.evalParm('f1'))
                EF = float(obj.evalParm('f2'))
                BF = float(obj.evalParm('f3'))
                obj.parm('f1').set(SFM)
                obj.parm('f2').set(EFM)
                obj.parm('f3').set(BFM)
                SF = float(obj.evalParm('f1'))
                EF = float(obj.evalParm('f2'))
                BF = float(obj.evalParm('f3'))
                print ('    NEW RANGE '+ _ROP + ' @ ' + str(SF) + '~' + str(EF) + '-' + str(BF))
                if objTypeName == 'arnold':
                    hou.setFrame(float(_SFM))
                    _THIS_PIC_NAME_NEW = obj.evalParm(_PIC_TYPE)
                    print ('    REDIRECT _________********AS: ' + _THIS_PIC_NAME_NEW + '\r')
                if SF != SFM or EF != EFM or BF != BFM:
                    print "\nFATAL ERROR: FAILED TO REMAP FRAME RANGE. \n    PLS DELETE CHANNEL->SAVE FILE->UPLOAD AND TRY AGAIN."
                    sys.exit(1)
                _rop_Node = hou.node(_ROP)
                break

    return _rop_Node

def _RV_missingReferenceAutoFix(files, search_path):
    if len(files):
        for f in files:
            bname = os.path.basename(f)
            buff = RVLIB._RV_findAllWithFileName(bname, search_path)
            asset_best_fit = None
            m = len(buff)
            if len(buff)>0:
                j = 0;
                for b in buff:
                    n = RVLIB._RV_fileName_Match_Counts(b, f)
                    if n>j:
                        j = n
                        asset_best_fit = b

def _RV_missingReferenceSkip():
    for obj in hou.node('/').allSubChildren():
        objTypeName = obj.type().name()
        objName = obj.name()
        objPath = obj.path()
        objPath = objPath.replace("\\", "/")
        sras = []
        if objTypeName in ['file']:
            try:
                obj.parm('missingframe').set(2)
                print "    missingframe skipped @ ", objName ,objPath
            except:
                print "    Node or attribute locked", objName ,objPath
        if objTypeName in ['alembic']:
            _fileName_alembic = obj.evalParm('fileName')
            if not os.path.exists(_fileName_alembic) and os.path.isfile(_fileName_alembic):
                try:
                    obj.parm('missingfile').set(2)
                    print "    missing fileName skipped @ ", objName ,objPath
                except:
                    print "    Node or attribute locked", objName ,objPath

def _RV_missingReferenceCheckAndAutoFix(search_path, NodePath):
    _D_MSAS = {}
    for obj in hou.node(NodePath).allSubChildren():
        _D_MSAS.setdefault(obj, {})
        for pm in obj.parms():
            pmn = pm.name()
            pmv = obj.evalParm(pmn)
            if type(pmv).__name__=='str':
                pmv = pmv.replace("\\", "/")
                pmv_upper = pmv.upper()
                pmvs = pmv.split("/")
                if len(pmvs)>1:
                    if fnmatch.fnmatch(pmv, "[A-Z]:/*") or fnmatch.fnmatch(pmv, "//*") or fnmatch.fnmatch(pmv, "/*"):
                        pmv_dir = os.path.dirname(pmv)
                        pmv_basename_ext = os.path.basename(pmv)
                        pmv_basename_no_ext = os.path.splitext(os.path.basename(pmv))[0]
                        pmv_extension = os.path.splitext(os.path.basename(pmv))[1]
                        if pmv_basename_ext!='' and pmv_basename_no_ext!='' and pmv_extension!='':
                            _D_MSAS[obj].setdefault(pmn, pmv)
    if os.path.exists(search_path):
        for obj in _D_MSAS.keys():
            objPath = obj.path()
            #print objPath
            objTypeName = obj.type().name()
            objName = obj.name()
            for pmn in _D_MSAS[obj].keys():
                pmv = _D_MSAS[obj][pmn]
                pmv_dir = os.path.dirname(pmv)
                pmv_bn_ext = os.path.basename(pmv)
                pmv_bn_no_ext = os.path.splitext(os.path.basename(pmv))[0]
                pmv_ext = os.path.splitext(os.path.basename(pmv))[1]
                _BEST_FIT_MSA = None
                if fnmatch.fnmatch(pmv_bn_no_ext, '*.%(UDIM)d*'):
                    pmv_bn_no_ext = pmv_bn_no_ext.replace(".%(UDIM)d", "*")
                    buff = RVLIB._RV_findAllWithPattern(pmv_bn_no_ext, search_path)
                    if len(buff)>0:
                        j = 0
                        temp = []
                        for b in buff:
                            d = os.path.dirname(b)
                            if d not in temp:
                                temp.append(d)
                        for b in temp:
                            n = RVLIB._RV_filePath_Dir_Match_Counts(b, pmv_dir)
                            if n>j:
                                j = n
                                _BEST_FIT_MSA = b
                        _BEST_FIT_MSA = _BEST_FIT_MSA.replace('\\', '/')
                else:
                    buff = RVLIB._RV_findAllWithFileName(pmv_bn_ext, search_path)
                    if len(buff)>0:
                        j = 0
                        for b in buff:
                            n = RVLIB._RV_fileName_Dir_Match_Counts(pmv_bn_no_ext, pmv_ext, pmv_dir, pmv)
                            if n>j:
                                j = n
                                _BEST_FIT_MSA = os.path.dirname(b)
                        _BEST_FIT_MSA = _BEST_FIT_MSA.replace('\\', '/')
                if _BEST_FIT_MSA is not None:
                    if not _BEST_FIT_MSA.endswith('/'):
                        _BEST_FIT_MSA = _BEST_FIT_MSA + '/'
                    _BEST_FIT_MSA_FFNAME = _BEST_FIT_MSA + pmv_bn_ext
                    print "\n\n%s - \n      %s -> %s" % (objPath, pmv_bn_ext, _BEST_FIT_MSA_FFNAME)
                    obj.parm(pmn).set(_BEST_FIT_MSA_FFNAME)

def _RV_loadHipFile(hip_file, error_logger = None):
    import hou

    hip_file = hip_file.replace("\\", "/")
    if not os.path.exists(hip_file):
        _failWithProjectError("ERROR: Cannot open file %s" % hip_file, error_logger)
    if hasattr(hou, "allowEnvironmentToOverwriteVariable"):
        if "JOB" in os.environ:
            hou.allowEnvironmentToOverwriteVariable("JOB", True)
    try:
        hou.hipFile.load(hip_file)
        #_HIP_VAR = os.path.dirname(hip_file)
        #hou.hscript("setenv HIP=" + str(_HIP_VAR))
        #hou.hscript("setenv TEX="+r"//10.50.242.6/d/inputdata5/1828000/1828006/ROBOT/textures" )
        #hou.hscript("setenv MESH="+r"//10.50.242.6/d/inputdata5/1828000/1828006/ROBOT/mesh" )
        #hou.hscript("setenv OTL="+r"//10.50.242.6/d/inputdata5/1828000/1828006/ROBOT/otls" )
        #hou.hscript("varchange")
        #print "HIP_rvhou   "+hou.getenv("HIP")
        #print "MESH_rvhou   "+hou.getenv("MESH")
        #print "tex   "+hou.getenv("TEX")
        #print "OTL   "+hou.getenv("OTL")
    except hou.LoadWarning:
        print "except "
        pass

def _RV_createDirectories(dirs_to_create, expand_vars_with_hou=True):
    """Attempt to create given list of directories.  

    Raise an exception if the user doesn't have proper permissions to create
    the directory.
    """

    for dir_path in dirs_to_create:
        if expand_vars_with_hou:
            import hou
            dir_path = hou.expandString(dir_path)
        else:
            dir_path = os.path.expandvars(dir_path)

        if os.path.exists(dir_path):
            continue

        try:
            # Attempt to create the directory.
            os.makedirs(dir_path)
        except OSError, e:
            err_msg = e.strerror.upper().strip()
            if err_msg == "FILE EXISTS":
                # Directory already exists.  That's fine.
                pass
            elif err_msg == "PERMISSION DENIED":
                # Print a nicer looking message.
                print "ERROR: Cannot create " + dir_path \
                    + ".  Permission denied."
                sys.exit(1)
            else:
                # Raise all other exceptions.
                raise

def _RV_substituteWithHQROOT(file_path):
    """Replace the beginning of the given path with $HQROOT.
    
    if the path is not under HQ's shared network file system return the
    original path.  Return None if an error occurs.
    """
    # Get the HQ root.  It should have been set in the environment
    # by the server.
    hq_root = os.environ["HQROOT"]
    hq_root = os.path.normpath(hq_root)
    hq_root = hq_root.replace("\\", "/")

    # Normalize file path.
    # Stick with forward slashes instead of backward slashes.
    file_path = os.path.normpath(file_path)
    file_path = file_path.replace("\\", "/")

    # Compare the HQ root with the given file path.
    # Substitute the raw HQ root path with the HQROOT environment
    # variable.
    if file_path.startswith(hq_root):
        file_path = file_path[len(hq_root):]
        if not file_path.startswith("/"):
            file_path = "/" + file_path
        file_path = "$HQROOT" + file_path

    return file_path

def _RV_generateNameForHipRender(hip_file, rop, frames):
    hip_name = os.path.basename(hip_file)
    output_path = _RV_getOutputPath(rop)
    base_name = "Render -> HIP: %s ROP: %s" % (hip_name, rop.name())
    return _generateRenderJobName(base_name, frames, output_path)

def _RV_getOutputPath(rop):
    """Returns an empty string if it cannot be determined."""
    output_parm = _RV_getOutputParm(rop)
    if output_parm is not None:
        output_path = output_parm.getReferencedParm().unexpandedString()
    else:
        output_path = ""
    
    return output_path

def _RV_renderRop(rop, *args, **kwargs):
    print '---------------------------------------'
    print 'rop = ', rop
    print 'args = ', args
    print 'kwargs = ', kwargs
    print '---------------------------------------\n'
    
    if hasattr(rop, 'render'):
        rop.render(*args, **kwargs)
        print("RENDERING FINISHED WITH RENDER PARM!")
    elif rop.parm("execute"):
        #rop.render(*args, **kwargs)
        rop.parm("execute").pressButton()
        print("RENDERING FINISHED WITH EXECUTE PARM!")
    else:
        raise TypeError("Could not render given node: " + rop.name())

def _RV_getTargetFramesFromRop(rop):
    """Return a tuple of frame numbers that the given output driver is 
    configured to render.
    """
    (start_frame, end_frame, frame_incr) = _RV_getFrameRangeFromRop(rop)
    frames = range(start_frame, end_frame + 1, frame_incr)
    return frames

def _RV_getFrameRangeFromRop(rop):
    """Return a 3-tuple of start_frame, end_frame and frame_increment 
    for the render frame range in the given ROP node."""
    import hou

    if rop.type().name() == "merge":
        start_frame = None
        end_frame = None
        frame_incr = None

        # For Merge ROPs,
        # the start frame is the min. start frame of its inputs,
        # the end frame is the max. end frame of its inputs,
        # and the increment is the min. increment of its inputs.
        for input_rop in rop.inputs():
            in_start, in_end, in_inc = _getFrameRangeFromRop(input_rop)
            if start_frame is None or in_start < start_frame:
                start_frame = in_start
            if end_frame is None or in_end > end_frame:
                end_frame = in_end
            if frame_incr is None or in_inc < frame_incr:
                frame_incr = in_inc

        # If the start, end, inc are None (i.e. the Merge has no children),
        # then just return the current frame as the frame range.
        if start_frame is None or end_frame is None or frame_incr is None:
            start_frame = hou.frame()
            end_frame = hou.frame()
            frame_incr = 1
    elif rop.type().name() == "fetch":
        # Get the frame range from the fetched ROP.
        source_rop = _getFetchedROP(rop)
        start_frame, end_frame, frame_incr = _getFrameRangeFromRop(source_rop)
    else:
        # Get the start, end and increment frame values.
        # If trange absent, we assume the full range.
        if (rop.parm('trange') is not None) and (rop.evalParm("trange") == 0):
            start_frame = int(hou.frame())
            end_frame = int(hou.frame())
            frame_incr = 1
        else:
            start_frame = int(rop.evalParm("f1"))
            end_frame = int(rop.evalParm("f2"))
            frame_incr = int(rop.evalParm("f3"))
    
    if frame_incr <= 0:
        frame_incr = 1

    return (start_frame, end_frame, frame_incr)

def _RV_getOutputParm(rop_node):
    """Return the output file parameter from the given ROP node.

    Return None if `rop_node` is None or if it is not a recognized
    output driver.
    """
    if rop_node is None:
        return None

    rop_type = rop_node.type().name()

    # If we are pointing to an HQueue ROP, then what we really want
    # is the node specified by the Output Driver parameter.
    if rop_type == "hq_render" or rop_type == "hq_sim":
        rop_node = getOutputDriver(rop_node)
        if rop_node is None:
            return None
        rop_type = rop_node.type().name()

    # We only handle Mantra, Geometry and Composite ROPs for now.
    output_parm = None
    if rop_type == "ifd":
        output_parm = rop_node.parm("vm_picture")
    elif rop_type in ("rop_geometry", "geometry"):
        output_parm = rop_node.parm("sopoutput")
    elif rop_type in ("rop_comp", "comp"):
        output_parm = rop_node.parm("copoutput")
    elif rop_type in ("rop_dop", "dop"):
        output_parm = rop_node.parm("dopoutput")
    elif rop_type == "baketexture":
        # The Bake Texture ROP node has multiple output parameters so we just
        # choose the first one.
        output_parm = rop_node.parm("vm_uvoutputpicture1")

    return output_parm

def _getFrameRangeFromRop(rop):
    """Return a 3-tuple of start_frame, end_frame and frame_increment 
    for the render frame range in the given ROP node."""
    import hou

    if rop.type().name() == "merge":
        start_frame = None
        end_frame = None
        frame_incr = None

        # For Merge ROPs,
        # the start frame is the min. start frame of its inputs,
        # the end frame is the max. end frame of its inputs,
        # and the increment is the min. increment of its inputs.
        for input_rop in rop.inputs():
            in_start, in_end, in_inc = _getFrameRangeFromRop(input_rop)
            if start_frame is None or in_start < start_frame:
                start_frame = in_start
            if end_frame is None or in_end > end_frame:
                end_frame = in_end
            if frame_incr is None or in_inc < frame_incr:
                frame_incr = in_inc

        # If the start, end, inc are None (i.e. the Merge has no children),
        # then just return the current frame as the frame range.
        if start_frame is None or end_frame is None or frame_incr is None:
            start_frame = hou.frame()
            end_frame = hou.frame()
            frame_incr = 1
    elif rop.type().name() == "fetch":
        # Get the frame range from the fetched ROP.
        source_rop = _getFetchedROP(rop)
        start_frame, end_frame, frame_incr = _getFrameRangeFromRop(source_rop)
    else:
        # Get the start, end and increment frame values.
        # If trange absent, we assume the full range.
        if (rop.parm('trange') is not None) and (rop.evalParm("trange") == 0):
            start_frame = int(hou.frame())
            end_frame = int(hou.frame())
            frame_incr = 1
        else:
            start_frame = int(rop.evalParm("f1"))
            end_frame = int(rop.evalParm("f2"))
            frame_incr = int(rop.evalParm("f3"))
    
    if frame_incr <= 0:
        frame_incr = 1

    return (start_frame, end_frame, frame_incr)

def _setParmInROPChain(rop, parm_name, vals):
    """Set the values for the given parameters in each node of the ROP chain.

    `rop` is the last node in the chain.
    `parm_name` is the name of the parameter or parameter tuple to be set.
    `val` is the parameter values.
    """
    import hou
    rop_stack = [rop, ]
    visited_rops = []

    while len(rop_stack) > 0:
        cur_rop = rop_stack.pop()

        if type(vals) == type([]) or type(vals) == type(()):
            parm = cur_rop.parmTuple(parm_name)
        else:
            parm = cur_rop.parm(parm_name)

        # Set the parameter if it exists.
        if parm is not None:
            _setParm(parm, vals)

        visited_rops.append(cur_rop)

        # Examine inputs.
        for input_node in cur_rop.inputs():
            if input_node is None:
                continue

            if input_node.type().category() == hou.ropNodeTypeCategory() \
                and input_node not in visited_rops:
                rop_stack.append(input_node)

def _setParm(parm, value):
    """Sets a parm with the given value.

    Will handle parmTuples and cases where the parm has an expression set.
    """
    try:    
        zipped_items = zip(parm, value)
    except TypeError:
        parm.getReferencedParm().setExpression(str(value))
    else:
        for subparm, subvalue in zipped_items:
            subparm.getReferencedParm().setExpression(str(subvalue))
