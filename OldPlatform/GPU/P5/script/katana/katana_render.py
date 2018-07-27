# /usr/bin/env python
import sys,os
katana_com_id=sys.argv[1]
katana_task_is=sys.argv[2]


katana_scene  = sys.argv[3]
katana_render_node = sys.argv[4]
katana_farm_start=sys.argv[5]
katana_farm_end=sys.argv[6]



katana_root = "/opt/foundry/katana"
#katana_root = "/home/ladaojeiang/yes"
os.system(r'%s/katana --batch --katana-file=%s --render-node=%s  --t=%s-%s' % (katana_root,katana_scene,katana_render_node,katana_farm_start,katana_farm_end))
