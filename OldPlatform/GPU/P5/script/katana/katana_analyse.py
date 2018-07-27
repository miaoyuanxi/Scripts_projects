
# /usr/bin/env python
import sys,os
katana_com_id=sys.argv[1]
kantan_task_is=sys.argv[2]

katana_script  = sys.argv[3]
katana_scene  = sys.argv[4]
katana_ana_txt=sys.argv[5]
kantan_root = "/opt/foundry/katana"
#kantan_root = "/home/ladaojeiang/yes"
def kanana_analyse_sys(kantan_root,katana_script,katana_scene,katana_ana_txt):
    

    os.system(r'%s/katana --script %s %s  %s' % (kantan_root,katana_script,katana_scene,katana_ana_txt))
    if  os.path.exists(katana_ana_txt):
        return 1
    else:
        return 0

kanana_analyse_sys(kantan_root,katana_script,katana_scene,katana_ana_txt)

