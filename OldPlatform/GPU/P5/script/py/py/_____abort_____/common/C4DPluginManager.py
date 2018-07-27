#!/usr/bin/python  
#coding=utf-8
#__author__:'kaname' QQ:1394041054

import os,sys

class C4DPlugin(object): 
    #初始化对象, 读取json来得出这些参数
    def __init__(self): 
        self.plugin_name    = ""
        self.plugin_version = ""
        self.soft_version   = ""
        self.node           = 'ABCDEF'
        
class C4DPluginManagerCenter(object):
    def __init__(self, user_id):
        self.user_id     = user_id
        self.plugin_root = r"B:\plugins\C4D"
        self.plugin      = C4DPlugin()
        self.plugin_path = ''

    def set_custom_env(self, plugin):
        self.plugin = plugin
        
        ###
        old_plugin_env = ''
        if os.environ.get('C4D_PLUGINS_DIR') is not None:
            old_plugin_env = os.environ["C4D_PLUGINS_DIR"]
        
        self.plugin_path = self.__get_plugin_path()
        #print '================================' + self.plugin_path
        # 检查路径有效性
        os.environ["C4D_PLUGINS_DIR"] = old_plugin_env + self.plugin_path + ';'
        
        ###
        old_library_env = ''
        if os.environ.get('C4D_BROWSERLIBS') is not None:
            old_library_env = os.environ["C4D_BROWSERLIBS"]
        library_path = self.__get_library_path()
        # 检查路径有效性
        os.environ["C4D_BROWSERLIBS"] = old_library_env + library_path + ';'

        print self.plugin_path + "\n" + library_path
        
        if plugin.plugin_name == 'c4dtoa':
            # copy ai.dll&solidangle.lic
            c4d_installed_path = os.path.join("C:/Program Files/MAXON", \
                                            self.plugin.soft_version) 
            ai_path  = os.path.join(self.plugin_path, "ai.dll")
            lic_path = os.path.join(self.plugin_path, "solidangle.lic")
            os.system('echo f | xcopy /f /y "%s" "%s"' % (ai_path, c4d_installed_path))
            os.system('echo f | xcopy /f /y "%s" "%s"' % (lic_path, c4d_installed_path))
        elif plugin.plugin_name == 'vray':
            # copy VrayBridge.key
            vray_installed_path = os.path.join("C:/Program Files/MAXON", \
                                            self.plugin.soft_version) 
                                            
            # 这里判断node 匹配出key，例如：VrayBridge.key.ABCDEFGHJ  w2一个镜像无需匹配，w5现在只用ABCDEF即可
             
            vray_key_path = os.path.join(self.plugin_path, 'vray_key', self.plugin.node, "VrayBridge.key")
            print vray_key_path
            vray_key_dest_path = os.path.join(vray_installed_path, "VrayBridge.key")
            print vray_key_dest_path
            os.system('echo f | xcopy /f /y "%s" "%s"' % (vray_key_path,  vray_key_dest_path))

        return True
    
    def __get_plugin_path(self):
        plugin_full_path =  os.path.join(self.plugin_root, \
                                        self.plugin.plugin_name, \
                                        self.plugin.plugin_name + '_' + self.plugin.plugin_version, \
                                        self.plugin.soft_version)
        return plugin_full_path
        
    def __get_library_path(self):
        library_full_path =  os.path.join(self.plugin_path, "library\\browser")
 
        return library_full_path

        
if __name__ == "__main__":
    plugin_name    = sys.argv[1]
    plugin_version = sys.argv[2]
    soft_version   = sys.argv[3]
    node           = sys.argv[4]
    print plugin_name,plugin_version,soft_version,node
    
    
    plugin_mgr = C4DPluginManagerCenter('100000')
    plugin = C4DPlugin()
    plugin.plugin_name      = plugin_name
    plugin.plugin_version   = plugin_version
    plugin.soft_version     = soft_version
    plugin.node             = node 

    plugin_mgr.set_custom_env(plugin)
    c4d_exec_path = '"C:/Program Files/MAXON/%s/CINEMA 4D 64 Bit.exe" ' % (soft_version)
    os.system(os.path.normpath(c4d_exec_path))
    
    
###test
'''
if __name__ == "__main__":
    soft_ver  = 'R16'
    plugin_mgr = C4DPluginManagerCenter("100001")
    plugin = C4DPlugin("c4dtoa", "1.0.14.1", 'CINEMA 4D', soft_ver)
    plugin_mgr.set_custom_env(plugin)
    c4d_exec_path = '"C:/Program Files/MAXON/CINEMA 4D %s/CINEMA 4D 64 Bit.exe" ' % (soft_ver)
    os.system(os.path.normpath(c4d_exec_path))
'''
#test:
# "C4DPluginManager.py" "CINEMA 4D R17" "c4depot_real_sky_studio" "1.11" "ABCDEF"

#C4D_PLUGINS_DIR
#B:\plugins\C4D\cineversity\cineversity_1.0.0\CINEMA 4D R17\;

#C4D_BROWSERLIBS
#B:\plugins\C4D\librarys\1822391\CINEMA 4D R16\library\browser
#B:\plugins\C4D\c4dtoa\c4dtoa_1.4.0.0\CINEMA 4D R17\library\browser;

#B:\plugins\C4D\vray\vray_1.9\CINEMA 4D R17\VrayBridge.key 
#B:\plugins\C4D\c4dtoa\c4dtoa_1.0.14.1\CINEMA 4D R17\ai.dll
#B:\plugins\C4D\c4dtoa\c4dtoa_1.0.14.1\CINEMA 4D R17\solidangle.lic

