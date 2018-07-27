# /usr/bin/env python
import socket,os,shutil,sys
katana_com_id=sys.argv[1]
katana_task_is=sys.argv[2]
katana_scene  = sys.argv[3]
katana_render_node = sys.argv[4]
katana_farm_start=sys.argv[5]
katana_farm_end=sys.argv[6]
plugin_cfg=sys.argv[7]
print katana_com_id,type(katana_com_id)
#katana_root = '/opt/katana/katana'
#katana_root = "/home/ladaojeiang/yes"



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
    os.environ['foundry_LICENSE'] = "4101@127.0.0.1"
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
if katana_com_id in  ["1161188"]:
    print "katana_root"    
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
    
    
else:
    katana_root = set_plug()
def kanana_render(katana_root,katana_scene,katana_render_node,katana_farm_start,katana_farm_end):
    print "______--------start render___________---------------"
    if os.path.exists(r"/tmp/nzs-data"):
        os.environ['TMPDIR'] = r"/tmp/nzs-data"
        os.environ['KATANA_TMPDIR'] = r"/tmp/nzs-data"
    else:
        raise AssertionError("tmp dir is not exists")

    
    
    if katana_com_id in  ["1161188"]:
        print "copy katana batch"
        sev = "/mnt_rayvision/p5/script/katana/yidong/Katana-batch"
        local = "/opt/katana/bin/Katana-batch"    
        shutil.copy2(sev, local)
        print "copy katana batch"
        os.environ['solidangle_LICENSE'] = "5060@10.60.96.203;5060@10.60.5.248;5060@127.0.0.1"
        os.environ['foundry_LICENSE'] = "4101@10.60.5.248;4101@127.0.0.1"
        project_dir = os.path.dirname(katana_scene)
        cmd_str = "/opt/katana/bin/Katana-batch %s %s %s-%s %s %s  %s" % (katana_scene,katana_render_node,katana_farm_start,katana_farm_end,"32","32",project_dir)
    else:
        cmd_str = r'%s --batch --katana-file=%s --render-node=%s  --t=%s-%s' % (katana_root,katana_scene,katana_render_node,katana_farm_start,katana_farm_end)
    print "cmd info >>>>>> %s " % cmd_str
    os.system(cmd_str)
kanana_render(katana_root,katana_scene,katana_render_node,katana_farm_start,katana_farm_end)
