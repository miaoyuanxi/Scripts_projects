set _cmd_opt = $_cmd_opt:as/@/ /
echo rendering using options:$_cmd_opt
mread $_cmd_render_file
python $_cmd_conf/nCZHoudini_Render_Configs.py $_cmd_cid $_cmd_rd $_cmd_ext $_cmd_rop
render -f $_cmd_sf $_cmd_ef -i $_cmd_bf $_cmd_opt obj/Render/$_cmd_rop
quit