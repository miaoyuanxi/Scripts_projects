#!/usr/bin/env bash
# mount.cifs //10.50.24.11/d /mnt/test -o user=enfuzion,passwd=abc123456
# /mnt_rayvision/p5/script/maya/check.sh 100001 666 /usr/autodesk/maya2014-x64/bin/mayapy /mnt/test /mnt/test/inputdata5/2014_ball.mb /mnt_rayvision/p5/config/100000/100001/666/analyse_net.txt
# Author: Liu Qiang
# Tel:    13811571784
# QQ:     386939142
user_id=$1
task_id=$2
cg_software_path=$3
cg_project=$4
cg_file=$5
cg_info_file=$6

if [ $user_id = 1841730 ]
then
export ASE_ASSETS=/ASE/01prj/AAJ/prod
export MAYA_ENABLE_LEGACY_RENDER_LAYERS=1
cp -u -a /mnt_rayvision/p5/script/assemblage/scripts/* /root/maya/2016.5/scripts
cp -u -a /mnt_rayvision/p5/script/assemblage/mod/mtoa_1.3.1.0/* /usr/autodesk/maya2016.5/modules
cp -u -a /mnt_rayvision/p5/script/assemblage/renderDesc/* /usr/autodesk/maya2016.5/bin/rendererDesc
fi

if [ $user_id = 1807081 ]
then
mkdir -p /tmp/nzs-data/plugins/
cp -u -a /mnt_rayvision/p5/script/88studio/redchillies/* /tmp/nzs-data/plugins/
export solidangle_LICENSE=5053@localhost:5060@10.60.96.203
export MAYA_MODULE_PATH=/tmp/nzs-data/plugins
export ARNOLD_PLUGIN_PATH=/tmp/nzs-data/plugins/alShaders-linux-1.0.0rc19-ai4.2.12.2/bin
export MTOA_TEMPLATES_PATH=/tmp/nzs-data/plugins/alShaders-linux-1.0.0rc19-ai4.2.12.2/ae
export MAYA_CUSTOM_TEMPLATE_PATH=/tmp/nzs-data/plugins/alShaders-linux-1.0.0rc19-ai4.2.12.2/aexml
fi

if [ $user_id = 1882862 ]
then
cp -u -a /mnt_rayvision/p5/script/88studio/userSetup/* /root/maya/2016/scripts
export PROJECTNAME=Butterbean
export JOB_ASSETS=/prod/PROJECTS/bbn/AssetsRepo
export BBF_TOOLS_PATH=/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE
export MAYA_MODULE_PATH=/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/Butterbean/Maya/Modules:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Modules:${MAYA_MODULE_PATH}
export MAYA_SCRIPT_PATH=/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/StartUp/Override/2016/scripts/:${MAYA_SCRIPT_PATH}
export PYTHONPATH=${PYTHONPATH}:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/StartUp/Override/2016/scripts:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Tools
export MAYA_PLUG_IN_PATH=${MAYA_PLUG_IN_PATH}:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfCharLightRig/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfGeometry/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfRig/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Tools/Rigging/cvShapeInverter/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/spReticle/2016-x64_linux/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfPublish/:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfVariant
export MAYA_RELEASE_PYTHON_GIL=1
fi

if [ $user_id = 1869998 ]
then
export ASE_ASSETS=/ASE/01prj/ICE/prod
export RLM_LICENSE=5077@10.60.5.248
export MAYA_ENABLE_LEGACY_RENDER_LAYERS=1
export solidangle_LICENSE=5053@localhost:5060@10.60.96.203
cp -u -a /mnt_rayvision/p5/script/assemblage/shave_mayafile/maya2016.5/* /usr/autodesk/maya2016.5
cp -u -a /mnt_rayvision/p5/script/assemblage/mod/mtoa_1.4.2.2/* /usr/autodesk/maya2016.5/modules
fi

if [ $user_id = 1879909 ]
then
export VRAY_AUTH_CLIENT_FILE_PATH=/var/vraylicense
export ASE_ASSETS=/ASE/01prj/LB2/prod
fi

if [ $user_id = 1833083 ]
then
#cp -u -a /mnt_rayvision/p5/script/88studio/bin/* /opt/solidangle/mtoa/2015/shaders
#cp -u -a /mnt_rayvision/p5/script/88studio/ae/* /opt/solidangle/mtoa/2015/scripts/mtoa/ui/ae
export JOB_ASSETS=/prod/PROJECTS/3bl/prod/assets/publish
export MAYA_ENABLE_LEGACY_RENDER_LAYERS=1
fi
if [ $user_id = 1833038 ]
then
cp -u -a /mnt_rayvision/p5/script/88studio/bin/* /opt/solidangle/mtoa/2015/shaders
cp -u -a /mnt_rayvision/p5/script/88studio/ae/* /opt/solidangle/mtoa/2015/scripts/mtoa/ui/ae
export JOB_ASSETS=/prod/PROJECTS/ths/prod/assets/publish
fi

cmd="${cg_software_path/mayapy/maya} -batch -command \"python \\\"cg_file, \
cg_info_file, cg_software=\\\\\\\"$cg_file\\\\\\\", \
\\\\\\\"$cg_info_file\\\\\\\", \\\\\\\"Maya\\\\\\\";\
execfile(\\\\\\\"/mnt_rayvision/o5/py/model/check_all2.py\\\\\\\")\\\"\""

echo "Run: $cmd"
eval $cmd
