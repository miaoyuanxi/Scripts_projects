
# /usr/bin/env python
import sys,os

katana_com_id=sys.argv[1]
kantan_task_is=sys.argv[2]
plugin_cfg  = sys.argv[3]
katana_scene  = sys.argv[4]
katana_ana_txt=sys.argv[5]

def set_env(env,val):
    if sys.platform.startswith("win"):
        spec = ";"
    if sys.platform.startswith("linux"):
        spec = ":"
    env_val = os.environ.get(env)
    os.environ[env] = (env_val  + spec  if env_val else "") + val
    return os.environ[env]


def set_plug():
    plugins_dict = eval(open(plugin_cfg).read())
    katana_n = plugins_dict['renderSoftware']
    katana_v = plugins_dict['softwareVer']    
    plugins = plugins_dict['plugins']
    
    
    if sys.platform.startswith("win"):
        #os.environ['foundry_LICENSE'] = "4101@127.0.0.1"
        set_env('foundry_LICENSE',"4101@127.0.0.1")
        os_type = "win"
        katana_soft_path = r"B:/plugins/katana/win"
        katana_exe = 'katanaBin.exe'
        katana_root = "%s/%s%s" % (katana_soft_path ,katana_n,katana_v)
        katana_path = "%s/bin/%s" % (katana_root,katana_exe)
        _PATH_env = os.environ.get('PATH')
        os.environ['PATH'] = (_PATH_env if _PATH_env else "") + r";" + katana_root + r"\bin;"        
        for plugin in plugins:
            plg_name = plugin
            plg_v = plugins[plg_name]
            plg_root = "%s/%s-%s-%s%s" % (katana_soft_path,plg_name, plg_v,katana_n,katana_v.split('v')[0])
            plg_config = plg_root+"/Config.py"
            if os.path.exists(plg_config):
                sys.path.append(plg_root)
                try:
                    cfg = __import__('Config')
                    reload(cfg)
                    cfg.doConfigSetup(plugins)
                    print ('=== the plugin %s %s load  Success for katana' % (plg_name,plg_v))
                except Exception as err:
                    print ('=== Error occur import/execute "%s"! ===\n=== Error Msg : %s ===' % (plg_config, err))
                try:
                    while True:
                        sys.path.remove(plg_root)
                except:
                    pass
            else:
                print ('plugin file "%s" is not exists!' % (plg_config))
    elif sys.platform.startswith("linux"):
        os_type = "linux"
        katana_soft_path = r"/B/plugins/"
        katana_exe = "katana"
        
        
        
        
        
        for plugin in plugins:
            plg_name = plugin
            plg_v = plugins[plg_name]



    return katana_path
currentPath = os.path.split(os.path.realpath(__file__))[0]        
katana_script = currentPath+"/katana_script_bak.py"
def kanana_analyse_sys(kantan_root,katana_script,katana_scene,katana_ana_txt):
    katana_scene_dir = os.path.dirname(katana_scene)
    os.chdir(katana_scene_dir)
    
    os.system(r'%s --script %s %s  %s' % (kantan_root,katana_script,katana_scene,katana_ana_txt))
    if  os.path.exists(katana_ana_txt):
        return 1
    else:
        return 0
if katana_com_id in  ["1161188"]:        
    kantan_root = '/opt/katana/katana'
else:
    kantan_root = set_plug()
print kantan_root
kanana_analyse_sys(kantan_root,katana_script,katana_scene,katana_ana_txt)


