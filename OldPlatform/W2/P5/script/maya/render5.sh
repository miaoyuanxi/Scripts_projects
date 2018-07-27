#!/usr/bin/env bash
# /mnt_rayvision/p5/script/maya/render5.sh 1 2 3 4 1 1 1 8 9 /mnt_rayvision/p5/config/100000/100001/545320/render.json /mnt_rayvision/p5/config/100000/100001/545320/plugin.json
# Author: Liu Qiang
# Tel:    13811571784
# QQ:     386939142
user_id=$1
task_id=$2
render=$3
txt=$4
start_frame=$5
end_frame=$6
by_frame=$7
project=$8
mb=$9
json=${10}
plugin_json=${11}
tile_index=${12}
tiles=${13}

echo task info:
echo "	userId:		$user_id"
echo "	task_id:	$task_id"
echo "	render:		$render"
echo "	txt:		$txt"
echo "	start_frame:	$start_frame"
echo "	end_frame:	$end_frame"
echo "	by_frame:	$by_frame"
echo "	project:	$project"
echo "	mb:		$mb"
echo "	json:		$json"
echo "	plugin_json:	$plugin_json"
echo "	tile_index:	$tile_index"
echo "	tiles:	$tiles"

if [ $user_id = 1841730 ]
then
export ASE_ASSETS=/ASE/01prj/LB2/prod
export MAYA_ENABLE_LEGACY_RENDER_LAYERS=1
export solidangle_LICENSE=5053@localhost:5060@10.60.96.203
cp -u -a /mnt_rayvision/p5/script/assemblage/scripts/* /root/maya/2016.5/scripts
cp -u -a /mnt_rayvision/p5/script/assemblage/mod/mtoa_1.3.1.0/* /usr/autodesk/maya2016.5/modules
cp -u -a /mnt_rayvision/p5/script/assemblage/renderDesc/* /usr/autodesk/maya2016.5/bin/rendererDesc
fi

if [ $user_id = 1869998 ]
then
export ASE_ASSETS=/ASE/01prj/ICE/prod
export MAYA_ENABLE_LEGACY_RENDER_LAYERS=1
export RLM_LICENSE=5077@10.60.5.248
export solidangle_LICENSE=5053@localhost:5060@10.60.96.203
cp -u -a /mnt_rayvision/p5/script/assemblage/renderDesc/* /usr/autodesk/maya2016.5/bin/rendererDesc
cp -u -a /mnt_rayvision/p5/script/assemblage/shave_mayafile/maya2016.5/* /usr/autodesk/maya2016.5
cp -u -a /mnt_rayvision/p5/script/assemblage/mod/mtoa_1.4.2.2/* /usr/autodesk/maya2016.5/modules
fi


if [ $user_id = 1879909 ]
then
cp -u -a /mnt_rayvision/p5/script/assemblage/temp/zxf/ARN_linux64_109/* /usr/autodesk/maya2015-x64/bin/plug-ins
export VRAY_AUTH_CLIENT_FILE_PATH=/var/vraylicense
export ASE_ASSETS=/ASE/01prj/LB2/prod
export VRAY_PLUGINS_x64=/usr/autodesk/maya2015-x64/vray/vrayplugins
export PATH=$PATH:/usr/autodesk/maya2015-x64/vray/bin
export LD_LIBRARY_PATH=/usr/autodesk/maya2015-x64/lib
echo $ASE_ASSETS
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


if [ $user_id = 1833083 ] || [ $user_id = 1868556 ] || [ $user_id = 1852991 ]
then
#cp -u -a /mnt_rayvision/p5/script/88studio/bin/* /opt/solidangle/mtoa/2015/shaders
#cp -u -a /mnt_rayvision/p5/script/88studio/ae/* /opt/solidangle/mtoa/2015/scripts/mtoa/ui/ae
#cp -u -a /mnt_rayvision/p5/script/88studio/rfconnect2015-maya2015-x64-2015.0.0.9/* /usr/autodesk
cp -u -a /mnt_rayvision/p5/script/88studio/arnoldrender/* /usr/autodesk/maya2017/bin/rendererDesc
cp -u -a /mnt_rayvision/p5/script/88studio/prefs/* /root/maya/2017/prefs
cp -u -a /mnt_rayvision/p5/script/88studio/realflow/* /usr/autodesk
/bin/cp -u -a /mnt_rayvision/p5/script/88studio/userSetup_2017/* /root/maya/2017/scripts
#export JOB_ASSETS=/prod/PROJECTS/3bl/prod/assets/publish
export VRAY_FOR_MAYA2016_MAIN_x64=/usr/autodesk/maya2016/vray
export VRAY_FOR_MAYA2016_PLUGINS_x64=/usr/autodesk/maya2016/vray/vrayplugins
export MAYA_PLUG_IN_PATH=/usr/autodesk/maya2016/vray/vrayplugins
export MAYA_SCRIPT_PATH=/usr/autodesk/maya2016/vray/scripts
export solidangle_LICENSE=5053@localhost:5060@10.60.96.203
mkdir -p /usr/apps/solidangle/mtoa_1.4.2.3/mtoa/2017up4/procedurals
cp -u -a /opt/solidangle/mtoa/2017/procedurals/* /usr/apps/solidangle/mtoa_1.4.2.3/mtoa/2017up4/procedurals
export MAYA_ENABLE_LEGACY_RENDER_LAYERS=1
fi

if [ $user_id = 1882862 ]
then
/bin/cp -u -a /mnt_rayvision/p5/script/88studio/userSetup/* /root/maya/2016/scripts
/bin/cp -u -a /mnt_rayvision/p5/script/88studio/vray_official_license/* /var/vraylicense  
export PROJECTNAME=Butterbean
export JOB_ASSETS=/prod/PROJECTS/bbn/AssetsRepo
export BBF_TOOLS_PATH=/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE
export MAYA_MODULE_PATH=/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/Butterbean/Maya/Modules:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Modules:${MAYA_MODULE_PATH}
export MAYA_SCRIPT_PATH=/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/StartUp/Override/2016/scripts/:${MAYA_SCRIPT_PATH}
export PYTHONPATH=${PYTHONPATH}:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/StartUp/Override/2016/scripts:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Tools
export MAYA_PLUG_IN_PATH=${MAYA_PLUG_IN_PATH}:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfCharLightRig/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfGeometry/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfRig/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Tools/Rigging/cvShapeInverter/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/spReticle/2016-x64_linux/plug-ins:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfPublish/:/prod/PROJECTS/bbn/pipe/code/88PICTURES_PIPELINE/BBF/Maya/Lib/bbfVariant
export MAYA_RELEASE_PYTHON_GIL=1
export MAYA_ENABLE_LEGACY_RENDER_LAYERS=1
fi


if [ $user_id = 1867865 ]
then
cp -u -a /opt/solidangle/mtoa/2017/arnoldRenderer.xml /usr/autodesk/maya2017/bin/rendererDesc
export solidangle_LICENSE=5053@localhost:5060@10.60.96.203
fi

if [ $user_id = 1862035 ]
then
export solidangle_LICENSE=5053@localhost:5060@10.60.96.203
fi
if [ $user_id = 1833038 ]
then
cp -u -a /mnt_rayvision/p5/script/88studio/bin/* /opt/solidangle/mtoa/2015/shaders
cp -u -a /mnt_rayvision/p5/script/88studio/ae/* /opt/solidangle/mtoa/2015/scripts/mtoa/ui/ae
export JOB_ASSETS=/prod/PROJECTS/ths/prod/assets/publish
fi
cmd="python /mnt_rayvision/o5/py/model/cgrender_linux.py --js $json --pl $plugin_json --sf $start_frame --ef $end_frame --by $by_frame --pt 1002 --sp $project --tile_index $tile_index --tiles $tiles"
echo "Run: $cmd"
$cmd

exitcode=$?
echo "exitcode: $exitcode"
if [ $exitcode == 0 ]
then
	echo "Render finished."
	exit 0
else
	echo "Render failed."
	exit $exitcode
fi
