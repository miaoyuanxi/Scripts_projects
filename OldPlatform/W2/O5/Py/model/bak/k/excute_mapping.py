# -*- coding: utf-8 -*-
import os
import sys
import json
import ctypes.wintypes

def k_mount():
    #k_mapping_imputs=r'Mapping T: to \\10.60.200.102\d\inputdata5\963000\963140\S;\2018-06-12 09:58:53 INFO - cmd...net use "M:" "\\10.60.200.103\d\inputdata5\1849000\1849290\S";"S:": "\\\\10.60.200.103\\d\\inputdata5\\1849000/1849290\\S",'

    #k_mapping_imputs=r''
    k_mapping_imputs = raw_input("mapping: ")

    k_mapping_imputsl = k_mapping_imputs.split(';')
    #print (k_mapping_imputsl)
    mount = {}

    if k_mapping_imputs:
        for k_mapping_imput in k_mapping_imputsl:
            if 'Mapping' in k_mapping_imput:
                k_mapping_imput = k_mapping_imput.split('Mapping')[1].strip()
                if 'to' in k_mapping_imput:
                    k_mapping_list = [ i.strip() for i in k_mapping_imput.split('to')]
                    mount[k_mapping_list[0]]=k_mapping_list[1]

            elif 'net use' in k_mapping_imput:
                k_mapping_imput = k_mapping_imput.split('net use')[1].strip()
                if ' ' in k_mapping_imput:
                    k_mapping_list = [ i.strip("\"") for i in k_mapping_imput.split(' ')]
                    mount[k_mapping_list[0]]=k_mapping_list[1]

            else:
                if k_mapping_imput.endswith(','):
                    k_mapping_imput=k_mapping_imput[:-1]
                k_mapping_imput=k_mapping_imput.replace('\\','/').replace('//','/')
                k_mapping_list = [i.strip("\"").replace('/','\\') for i in k_mapping_imput.split(': ')]
                mount[k_mapping_list[0]]=k_mapping_list[1]


    model = r"\\10.60.100.101\o5\py\model\function"
    sys.path.append(model)

    import k_mapping

    custom_config = r"\\10.60.100.151\td\custom_config"
    B_path = custom_config.split(r'\custom_config')[0]



    print (mount)
    if k_mapping_imputs:
        k_mapping.k_mapping(B_path,mount)

def k_dirmap():

    k_dirmap_imputs = raw_input("dirmap: ")
    #k_dirmap_imputs = "'mappings': {u'//server3d/work': 'W:', u'W:': 'W:'},"
    
    #CSIDL_PERSONAL = 0       
    #SHGFP_TYPE_CURRENT = 1   

    #buf= ctypes.create_unicode_buffer(ctypes.wintypes.MAX_PATH)
    #ctypes.windll.shell32.SHGetFolderPathW(None, CSIDL_PERSONAL, None, SHGFP_TYPE_CURRENT, buf)
    #print(buf.value)
    #Desktop = buf.value
    #k_usersetup_mel = Documents + (r'\maya\scripts\userSetup.py')

    k_current_dir = os.path.dirname(os.path.realpath(__file__))

    k_usersetup_mel = k_current_dir + (r'\userSetup.py')
    print (k_usersetup_mel)


    if k_dirmap_imputs:
        if k_dirmap_imputs.endswith(','):
            k_dirmap_imputs=k_dirmap_imputs[:-1]

        k_dirmap_dict = "{"+k_dirmap_imputs+"}"

        k_dirmap=eval(k_dirmap_dict)
        print (k_dirmap)
        #获取桌面地址
        
        with open(k_usersetup_mel, "w") as f:
            f.write("import maya.cmds as cmds\n")
            f.write("cmds.dirmap( en=True )\n")
            for i in k_dirmap['mappings']:
                if not i.startswith("$"):
                    old_path = i
                    #if isinstance(old_path, unicode):
                    old_path = i.encode("gb18030")
                        #old_path = i
                    #if isinstance(k_dirmap['mappings'][i], unicode):
                    new_path = k_dirmap['mappings'][i].encode("gb18030")                       
                    f.write("cmds.dirmap ( m=('%s' , '%s'))\n" % (old_path,
                            new_path))
            f.write("print('Mapping successfully')\n")

    else:
        if os.path.exists(k_usersetup_mel):
            os.remove(k_usersetup_mel)

if __name__ == '__main__':
    k_mount()
    k_dirmap()
    os.system('pause')
    sys.exit(0)
