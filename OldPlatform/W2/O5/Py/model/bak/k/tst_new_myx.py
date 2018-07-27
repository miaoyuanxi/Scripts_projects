import os, sys
cusId= raw_input("cusid: ")
taskId=raw_input("taskId: ")
custom_plugin_cfg=raw_input('custom_plugin_cfg: ')
cmd=raw_input("cmd: ")
print "custom_plugin_cfg"
print custom_plugin_cfg
print type(custom_plugin_cfg)
if cusId =="":
    cusId="1234567"
    fileId="1234567"
else:
    if int(cusId[-3:]) >= 500:
        fileId = str(int(cusId) - int(cusId[-3:]) + 500)
    else:
        fileId = str(int(cusId) - int(cusId[-3:]))
if taskId=="":
    taskId="1000000"


if taskId[0] == "5":
    plugin_config1 = r"//10.50.244.116/p5/config/%s/%s/%s/plugins.json" % (fileId, cusId, taskId)
    plugin_config2 = r"//10.50.244.116/d/ninputdata5/%s/temp/plugins.cfg" %(taskId)
    custom_config = r"\\10.50.1.22\td\custom_config"
    model = r"\\10.50.5.29\o5\py\model"
if taskId[:2] == "10":
    plugin_config1 = r"//10.60.100.101/p5/config/%s/%s/%s/plugins.json" % (fileId, cusId, taskId)
    plugin_config2 = r"//10.60.100.101/d/ninputdata5/%s/temp/plugins.cfg" %(taskId)
    custom_config = r"\\10.60.100.151\td\custom_config"
    model = r"\\10.60.100.101\o5\py\model"
    model = os.path.join(model,"function")
if taskId[:2] == "19":
    plugin_config1 = r"//10.80.100.101/p5/config/%s/%s/%s/plugins.json" % (fileId, cusId, taskId)
    plugin_config2 = r"//10.80.100.101/d/ninputdata5/%s/temp/plugins.cfg" %(taskId)
    custom_config = r"\\10.80.243.50\td\custom_config"
    model = r"\\10.80.100.101\o5\py\model"
if taskId[:2] == "16":
    plugin_config1 = r"//10.90.100.101/p5/config/%s/%s/%s/plugins.json" % (fileId, cusId, taskId)
    plugin_config2 = r"//10.90.100.101/d/ninputdata5/%s/temp/plugins.cfg" %(taskId)
    custom_config = r"\\10.80.243.50\td\custom_config"
    model = r"\\10.90.100.101\o5\py\model"
if taskId[0] == "8":
    plugin_config1 = r"//10.70.242.102/p5/config/%s/%s/%s/plugins.json" % (fileId, cusId, taskId)
    plugin_config2 = r"//10.70.242.102/d/ninputdata5/%s/temp/plugins.cfg" %(taskId)
    custom_config = r"\\10.70.242.50\td\custom_config"
    model = r"\\10.70.242.102\o5\py\model"
#model=r"D:\temp"
sys.path.append(model)
import RayvisionPluginsLoader
from MayaPlugin import MayaPlugin

if os.path.exists(plugin_config1):
    plugin_cfg_file = plugin_config1
elif os.path.exists(plugin_config2):
    plugin_cfg_file = plugin_config2

# plugin_cfg = r"E:\PycharmProjects\ffmpeg_test\plugins.json"
if custom_plugin_cfg =="":
    plugin_cfg_file=plugin_cfg_file
else:
    plugin_cfg_file = custom_plugin_cfg
print "plugin_cfg_file"
print plugin_cfg_file
custom_file = custom_config + "/" + cusId + "/RayvisionCustomConfig.py"
print plugin_cfg_file

maya_plugin=MayaPlugin(plugin_cfg_file,[custom_file])
maya_plugin.config()           
sys.stdout.flush()

# plginLd = RayvisionPluginsLoader.RayvisionPluginsLoader()
# plginLd.RayvisionPluginsLoader(plugin_cfg_file, [custom_file])
with open(plugin_cfg_file, 'r') as file:
    file_str = file.read()
    plugis_dict = dict(eval(file_str))
    
    if plugis_dict:
        renderSoftware = plugis_dict['renderSoftware']
        softwareVer = plugis_dict['softwareVer']
        plugis_list_dict = plugis_dict['plugins']
        print plugis_list_dict
cmd1 = r"C:\Program Files\Autodesk\Maya%s\bin\maya.exe" % (softwareVer)
print '"'+cmd1+'"'
cmd2 = 'cmd'
if cmd=="":
    cmd_str=cmd1
elif cmd=="2":
    cmd_str=cmd2
print cmd
    
os.system('"' + cmd_str + '"')
