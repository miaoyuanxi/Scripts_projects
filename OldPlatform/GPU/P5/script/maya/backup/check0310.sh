#!/usr/bin/env bash
# /mnt_rayvision/p5/script/maya/check.sh 100001 666 /usr/autodesk/maya2014-x64/bin/mayapy /mnt/test /mnt/test/inputdata5/2014_ball.mb /mnt_rayvision/p5/config/100000/100001/666/analyse_net.txt
# Author: Liu Qiang
# Tel:    13811571784
# QQ:     386939142
user_id=$1
task_id=$2
maya_exe_path=$3
cg_project=$4
cg_file=$5
net_file=$6

cmd="$maya_exe_path /mnt_rayvision/o5/py/model/check.py --cf $cg_file --nf $net_file"
echo "Run: $cmd"
$cmd
