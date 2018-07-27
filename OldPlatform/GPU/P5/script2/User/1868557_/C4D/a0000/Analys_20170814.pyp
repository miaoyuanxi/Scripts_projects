#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file
#.C4D_Analys-'Lion''QQ:58701328'
### modify by kanada
import c4d, sys, re, os, json
from c4d import documents, gui

class C4Dparser():
    def __init__(self, *args):
        
        self.texture_tag              = "------------texture-----------------"
        self.image_size_tag           = "------------Image Size-----------------"
        self.render_frame_tag         = "------------Render Frame-----------------"
        self.render_format_tag        = "------------Render Format-----------------"
        self.multi_pass_tag           = "------------Multi-Pass-----------------"
        self.camera_tag               = "------------camera-----------------"
        self.rfmesh_name_path_tag     = "------------RFMesh_name_path-----------------"
        self.rfparticle_name_path_tag = "------------RFParticle_name_path-----------------"
        self.cgFileStr  = args[0]
        self.txtFileStr = args[1]
        #self.taskIdStr = args[1]
       
    def __del__(self):
        sys.path.append(r'\\10.60.100.101\p5\script2\User\119614\C4D\a0000')
        import kill
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R13_05DFD2A0\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R14_4A9E4467\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R15_53857526\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R16_14AF56B1\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R17_8DE13DAD\plugins\Analys.pyp')
        os.remove('C:\users\enfuzion\AppData\Roaming\MAXON\CINEMA 4D R18_62A5E681\plugins\Analys.pyp')
       
    def getAllCams(self,doc):
        cameraStr=''
        doc = c4d.documents.GetActiveDocument()
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        Cameras = doc.GetActiveObjectsFilter(True, type=5103, instanceof=True)
        for C in (Cameras):
            if C.GetTypeName() == "Camera":
                obj = str(C)
                print obj+'\n'
                for C in obj.split():
                    if "/" in C:
                        keyword = C
                        break
                word = keyword.replace("'","")
                wordSplit = word.split("/")
                if wordSplit:
                    wordHead = wordSplit[0]
                    print "CameaName:"+wordHead + '\n'
                    cameraStr=cameraStr+("cameraName:"+str(wordHead)+"\n\n")
            else:
                continue
        c4d.CallCommand(12113) # Deselect All
        return cameraStr

    def getRFMesh(self, doc):
        RFMeshStr=''
        doc = c4d.documents.GetActiveDocument()
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        obj = doc.GetObjects()
        for i in (obj):
            if not obj: return
            if i.GetTypeName() == ('RealFlow Mesh Importer' and '网格导入RealFlow Mesh Importer'):
                RFMesh_path = i[c4d.M_IMP_FILE_PATH]
                obj = str(i)
                for i in obj.split():
                    if "/" in i:
                        keyword1 = i
                        break
                word = keyword1.replace("'","")
                wordSplit = word.split("/")
                if wordSplit:
                    wordHead1 = wordSplit[0]
                    print "RFMesh_Name:"+wordHead1 + '\n'
                print 'RFMesh_path' + ':' + RFMesh_path
                RFMeshStr=RFMeshStr+("RFMesh_Name:"+str(wordHead1)+"\n\n"+'RFMesh_path'+':'+ str(RFMesh_path)+"\n\n")
            else:
                continue
        c4d.CallCommand(12113) # Deselect All
        return RFMeshStr

    def getRFParticle(self, doc):
        RFParticleStr=''
        doc = c4d.documents.GetActiveDocument()
        c4d.CallCommand(12112) # Select All
        c4d.CallCommand(16388) # Select Children
        obj = doc.GetObjects()
        for i in (obj):
            if not obj: return
            if i.GetTypeName() == ('RealFlow Particle Importer' and '粒子导入RealFlow Particle Importer'):
                RFParticle_path = i[c4d.P_IMP_FILE_PATH]
                obj = str(i)
                for i in obj.split():
                    if "/" in i:
                        keyword1 = i
                        break
                word = keyword1.replace("'","")
                wordSplit = word.split("/")
                if wordSplit:
                    wordHead1 = wordSplit[0]
                    print "RFParticle_Name:"+wordHead1 + '\n'
                print 'RFParticle_path' + ':' + RFParticle_path
                RFParticleStr=RFParticleStr+("RFParticle_Name:"+str(wordHead1)+"\n\n"+'RFParticle_path'+':'+ str(RFParticle_path)+"\n\n")
            else:
                continue
        c4d.CallCommand(12113) # Deselect All
        return RFParticleStr
        
    def MultiPass(self, doc):
        MPnameStr=''
        rd = doc.GetActiveRenderData()
        vp = rd.GetFirstMultipass()
        single_path = rd[c4d.RDATA_PATH]
        multi_path = rd[c4d.RDATA_MULTIPASS_FILENAME]
        multi_path_arr = multi_path.split("\\")
        i = 0
        arr_len = len (multi_path_arr)
        arr_len = arr_len - 1
        object_buffer_arr = []
        object_bufferID_arr = []
        pfadarr = []
        file_type_arr = []
        file_name =  multi_path_arr[arr_len]
        i = 0
        j = 0
        k = 0
        while vp:
            if vp.GetTypeName() == "Object Buffer":
                object_buffer_arr.append (vp.GetName())
                object_bufferID_arr.append (vp[c4d.MULTIPASSOBJECT_OBJECTBUFFER])
                j = j + 1
            mp_name = vp.GetName()
            print mp_name + '\n'
            MPnameStr=MPnameStr+("MultiPassName:"+str(mp_name)+"\n\n")
           
            multipass_type = ""
            if mp_name == "RGBA Image":
                multipass_type = "rgb"
            elif mp_name == "Ambient":
                multipass_type = "ambient"
            elif mp_name == "Ambient Occlusion":
                multipass_type = "ao"
            elif mp_name == "Atmosphere":
                multipass_type = "atmos"        
            elif mp_name == "Atmosphere (Multiply)":
                multipass_type = "atmosmul"
            elif mp_name == "Caustics":
                multipass_type = "caustics"
            elif mp_name == "Depth":
                multipass_type = "depth"
            elif mp_name == "Diffuse":
                multipass_type = "diffuse"
            elif mp_name == "Global Illumination":
                multipass_type = "gi"
            elif mp_name == "Illumination":
                multipass_type = "illum"
            elif mp_name == "Material Color":
                multipass_type = "matcolor"
            elif mp_name == "Material Diffusion":
                multipass_type = "matdif"            
            elif mp_name == "Material Environment":
                multipass_type = "matenv"            
            elif mp_name == "Material Luminance":
                multipass_type = "matlum"
            elif mp_name == "Material Reflection":
                multipass_type = "matrefl"            
            elif mp_name == "Material Refraction":
                multipass_type = "matrefr"            
            elif mp_name == "Material Specular":
                multipass_type = "matspec"            
            elif mp_name == "Material Specular Color":
                multipass_type = "matspeccol"  
            elif mp_name == "Material Transparency":
                multipass_type = "mattrans"            
            elif mp_name == "Motion Vector":
                multipass_type = "motion"            
            elif mp_name == "Material Normal":
                multipass_type = "normal"            
            elif mp_name == "Specular":
                multipass_type = "specular"            
            elif mp_name == "Shadow":
                multipass_type = "shadow"            
            elif mp_name == "Material UVW":
                multipass_type = "uv"              
            elif mp_name == "Reflection":
                multipass_type = "refl"            
            elif mp_name == "Refraction":
                multipass_type = "refr"              
            elif mp_name == "Post Effects":
                multipass_type = "post"
            vp = vp.GetNext()
        else:
            print "multipass is Null"
        return MPnameStr

    def Analyze(self, *args):
        self.dict_result = dict()
        doc = documents.GetActiveDocument()
        # =========================================
        dict_textures = {}
        texs = doc.GetAllTextures()
        for item in texs:
            dict_textures[item[0]] = item[1]
        
        self.dict_result['texture'] = dict_textures
        # =========================================
        dict_image_size = {}
        rd = doc.GetActiveRenderData()
        sizeX = int(rd[c4d.RDATA_XRES_VIRTUAL]) 
        sizeY = int(rd[c4d.RDATA_YRES_VIRTUAL]) 
        dict_image_size['Width']  = sizeX
        dict_image_size['Height'] = sizeY

        self.dict_result['image_size'] = dict_image_size
        # =========================================
        dict_render_frame = {}
        rd = doc.GetActiveRenderData()
        fps = doc.GetFps()
        sf = (rd[c4d.RDATA_FRAMEFROM]).GetFrame(fps)
        ef = (rd[c4d.RDATA_FRAMETO]).GetFrame(fps)
        dict_render_frame['StartFrame'] = sf
        dict_render_frame['EndFrame']   = ef
        
        self.dict_result['render_frame'] = dict_render_frame
        # =========================================
        dict_render_format = {}
        rd = doc.GetActiveRenderData()
        RI_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'BodyPaint 3D(B3D)',1023737:'DPX',1103:'IFF',1104:'JPEG',1016606:'OpenEXR',1106:'Photoshop(PSD)',
                    1111:'Photoshop Large Document(PSB)',1105:'PICT',1023671:'PNG',1001379:'Radiance(HDR)',1107:'RLA',1108:'RPF',
                    1101:'TARGA',1110:'TIFF(B3D Layers)',1100:'TIFF(PSD Layers)',1122:'AVI Movie',1125:'QuickTime Movie',
                    1150:'QuickTime VR Panorama',1151:'QuickTime VR Object'}
        dict_render_format['RI_Format'] = RI_Format[int(rd[c4d.RDATA_FORMAT])]
        MP_Format = {1035823:'Arnold-Dummy',1102:'BMP',1109:'BodyPaint 3D(B3D)',1023737:'DPX',1103:'IFF',1104:'JPEG',1016606:'OpenEXR',1106:'Photoshop(PSD)',
                    1111:'Photoshop Large Document(PSB)',1105:'PICT',1023671:'PNG',1001379:'Radiance(HDR)',1107:'RLA',1108:'RPF',
                    1101:'TARGA',1110:'TIFF(B3D Layers)',1100:'TIFF(PSD Layers)',1122:'AVI Movie',1125:'QuickTime Movie'}
        dict_render_format['MP_Format'] = MP_Format[int(rd[c4d.RDATA_MULTIPASS_SAVEFORMAT])]
        
        self.dict_result['render_format'] = dict_render_format
        # =========================================
        dict_multipass = {}
        rd = doc.GetActiveRenderData()
        fmp = rd.GetFirstMultipass()
        arr_mp_name = []
        while fmp:
            mp_name = fmp.GetName()
            arr_mp_name.append(mp_name)           
            fmp = fmp.GetNext()
        dict_multipass['names'] = arr_mp_name
        
        self.dict_result['multipass'] = dict_multipass
        # =========================================
        arr_cameras = []
        self.dict_result['cameras'] = arr_cameras
        
        arr_rfmesh = []
        self.dict_result['RFMesh'] = arr_rfmesh
                 
        self.parse_analyze_result()
        
        # write result to file
        # root_dir = os.path.dirname(self.txtFileStr)
        # result_file = os.path.join(root_dir, 'result.json')  
        with open(self.txtFileStr, 'w') as outfile:
            json.dump(self.dict_result, outfile, indent=4)  
            
    
    def parse_analyze_result(self):
        dict_textures = self.dict_result['texture']
        self.parse_texture(dict_textures)
 
    #(21, 'T:\\195_NOVA\\_mg\\Jason\\for_renderbus\\Green_v008\\tex\\3d66Model-364628-2-97_1.jpg')   
    #(22, '3d66Model-364628-2-97_1.jpg')  
    def parse_texture(self, textures):
        tex_missings = []
        print type(textures)
        for idx, texture in textures.items():
            # 绝对路径检查
            if texture.find(':\\') > -1: 
                if os.path.exists(texture) == False:
                    tex_missings.append(texture)
            # 文件名检查
            else: 
                root_dir = os.path.dirname(self.cgFileStr)
                tex_dir = os.path.join(root_dir, 'tex')  
                tex_file = os.path.join(tex_dir, texture)

                if os.path.exists(tex_file) == False:
                    tex_missings.append(texture)

        self.dict_result['texture_missing'] = tex_missings
    
def PluginMessage(id, data):
    print 'plugin------'
    
    if id==c4d.C4DPL_COMMANDLINEARGS:
        cgFileStr=''
        txtFileStr=''
        print sys.argv #print arguments
        for arg in sys.argv:
            print arg
            if arg.startswith('-cgFile'):
                cgFileStr=arg.replace('-cgFile:', '')
                print cgFileStr
            elif arg.startswith('-txtPath'):
                txtFileStr=arg.replace('-txtPath:', '')
                print txtFileStr
            else:
                print 'no info'
        RFile = str(cgFileStr)
        c4d.documents.LoadFile(RFile)

        mainFunc = C4Dparser(cgFileStr, txtFileStr)
        mainFunc.Analyze()
        return True

    return False