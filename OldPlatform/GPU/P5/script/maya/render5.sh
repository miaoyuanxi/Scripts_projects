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
if [ $user_id = 1914867  ] || [ $user_id = 119768 ]
then
export gpuid=1
export INSTALLDIR=/usr/autodesk/maya2017
export redshift_LICENSE=5057@127.0.0.1
export REDSHIFT_LICENSEPATH=/usr/redshift_lic/redshift-core2.lic
export MAYA_PLUG_IN_PATH=/usr/autodesk/of3d/opiumPipe/0.80/plug-ins/lin2017:$MAYA_PLUG_IN_PATH
export LD_LIBRARY_PATH=/usr/autodesk/of3d/opiumPipe/0.80/lin_lib:$LD_LIBRARY_PATH
export ARNOLD_PLUGIN_PATH=/opt/solidangle/1.0.0rc20-ai5.0.1.0/bin:$ARNOLD_PLUGIN_PATH                    
export MAYA_CUSTOM_TEMPLATE_PATH=/opt/solidangle/1.0.0rc20-ai5.0.1.0/aexml:$MAYA_CUSTOM_TEMPLATE_PATH                    
export MTOA_TEMPLATES_PATH=/opt/solidangle/1.0.0rc20-ai5.0.1.0/ae:$MTOA_TEMPLATES_PATH

export projectData=/mnt/projectFiles
export proj=/mnt/proj

export MAYA_SCRIPT_PATH=/mnt_rayvision/o5/py/model/User/$user_id/SCRIPT:$MAYA_SCRIPT_PATH
export MAYA_RENDER_DESC_PATH=/usr/redshift/redshift4maya/common/rendererDesc:$MAYA_RENDER_DESC_PATH
fi

cmd="python /mnt_rayvision/o5/py/model/cgrender_linux.py --js $json --pl $plugin_json --sf $start_frame --ef $end_frame --by $by_frame --pt 1008 --sp $project --tile_index $tile_index --tiles $tiles"
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
