
# /usr/bin/env python
import sys,os

katana_com_id=sys.argv[1]
kantan_task_is=sys.argv[2]
plugin_cfg  = sys.argv[3]
katana_scene  = sys.argv[4]
katana_ana_txt=sys.argv[5]

def set_plug():
    if sys.platform.startswith("win"):
        os_type = "win"
        katana_soft_path = r"B:/plugins/katana/win"
        katana_exe = 'katanaBin.exe'
    elif sys.platform.startswith("linux"):
        os_type = "linux"
        katana_soft_path = r"/munt/plugins"
        katana_exe = "katana"

    plugins_dict = eval(open(plugin_cfg).read())
    katana_n = plugins_dict['renderSoftware']
    katana_v = plugins_dict['softwareVer']
    plugins = plugins_dict['plugins']
    os.environ['foundry_LICENSE'] = "4101@127.0.0.1;4101@10.60.5.248"
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
    return katana_path
currentPath = os.path.split(os.path.realpath(__file__))[0]        
katana_script = currentPath+"/katana_script_bak.py"
def kanana_analyse_sys(katana_root,katana_script,katana_scene,katana_ana_txt):
    print "_________________________________________ start analyse_________________________________________ "
    print katana_root,katana_script,katana_scene,katana_ana_txt
    
    katana_scene_dir = os.path.dirname(katana_scene)
    os.chdir(katana_scene_dir)
    
    os.system(r'%s --script %s %s  %s' % (katana_root,katana_script,katana_scene,katana_ana_txt))
    print "_________________________________________ end analyse _________________________________________ "
    if  os.path.exists(katana_ana_txt):
        return 1
    else:
        return 0
if katana_com_id in  ["1161188"]:        
    katana_root = '/opt/katana/katana'
elif katana_com_id in  ["119768","1909127"]:
    katana_root = '/opt/katana2.5v3/katana'
    os.environ['RLM_LICENSE']="4101@10.60.5.248"
    os.environ['PIXAR_LICENSE_FILE']="/opt/pixar/pixar.license"
    os.environ['KATANA_ROOT']="/opt/katana2.5v3"
    os.environ['RMANTREE']="/opt/pixar/RenderManProServer-21.7"
    os.environ['KATANA_RESOURCES']="/opt/pixar/RenderManForKatana-21.7-katana2.5/plugins/Resources/PRMan21"
    os.environ['RMAN_SHADERPATH']="/opt/pixar/RenderManProServer-21.7/lib/shaders"
    os.environ['RMAN_RIXPLUGINPATH']="/opt/pixar/RenderManProServer-21.7/lib/plugins"
    os.environ['RFKTREE']="/opt/pixar/RenderManForKatana-21.7-katana2.5"
    _PATH_env = os.environ.get('PATH')
    os.environ['PATH'] = (_PATH_env if _PATH_env else "") + r":" + katana_root + r"\bin:" +"/opt/pixar/RenderManProServer-21.7/lib:"+"/opt/pixar/RenderManProServer-21.7/bin:"
    os.environ['DEFAULT_RENDERER']="prman"
    katana_script = "/mnt_rayvision/p5/script2/Katana/lib/katana_script_1909127.py"
    print katana_script
else:
    katana_root = set_plug()

kanana_analyse_sys(katana_root,katana_script,katana_scene,katana_ana_txt)


