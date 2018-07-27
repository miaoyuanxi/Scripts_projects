mread $_cmd_render_file
python //10.50.1.3/pool/script/houdini/nCZ_Houdini_Customers_Configs.py $_cmd_cid $_cmd_rd $_cmd_ext
render -V -I -f $_cmd_sf $_cmd_ef -i $_cmd_bf out/*
quit