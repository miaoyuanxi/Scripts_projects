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

if [ $user_id = 1914867 ]
then
export INSTALLDIR=/usr/autodesk/maya2017
export REDSHIFT_LICENSE=5057@10.60.5.248
export REDSHIFT_LICENSEPATH=/usr/autodesk/redshift-core2.lic
export MAYA_PLUG_IN_PATH=/usr/autodesk/of3d/opiumPipe/0.80/plug-ins/lin2017:$MAYA_PLUG_IN_PATH
export LD_LIBRARY_PATH=/usr/autodesk/of3d/opiumPipe/0.80/lin_lib:$LD_LIBRARY_PATH

export ARNOLD_PLUGIN_PATH=/opt/solidangle/1.0.0rc20-ai5.0.1.0/bin:$ARNOLD_PLUGIN_PATH                    
export MAYA_CUSTOM_TEMPLATE_PATH=/opt/solidangle/1.0.0rc20-ai5.0.1.0/aexml:$MAYA_CUSTOM_TEMPLATE_PATH                    
export MTOA_TEMPLATES_PATH=/opt/solidangle/1.0.0rc20-ai5.0.1.0/ae:$MTOA_TEMPLATES_PATH

fi
cmd="${cg_software_path/mayapy/maya} -batch -command \"python \\\"cg_file, \
cg_info_file, cg_software=\\\\\\\"$cg_file\\\\\\\", \
\\\\\\\"$cg_info_file\\\\\\\", \\\\\\\"Maya\\\\\\\";\
execfile(\\\\\\\"/mnt_rayvision/o5/py/model/check_all2.py\\\\\\\")\\\"\""

echo "Run: $cmd"
eval $cmd
