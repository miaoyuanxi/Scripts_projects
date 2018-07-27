""" C4d loader """
#!/usr/bin/python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

import os
import sys
import subprocess

pyp_dev_path = '//10.60.100.101/p5/script2/User/119614/C4D/a0000/RBAnalyzer.pyp'
pyp_rel_path = 'B:/plugins/C4D/script/RBC4dAnalyzer.pyp'
maxon_data_path = 'C:/users/enfuzion/AppData/Roaming/MAXON/CINEMA 4D %s/plugins/'
c4d_pyp_config = {
    'CINEMA 4D R13' : 'R13_05DFD2A0',
    'CINEMA 4D R14' : 'R14_4A9E4467',
    'CINEMA 4D R15' : 'R15_53857526',
    'CINEMA 4D R16' : 'R16_14AF56B1',
    'CINEMA 4D R17' : 'R17_8DE13DAD',
    'CINEMA 4D R18' : 'R18_62A5E681',
}

class C4dLoader(object):
    """ C4d loader class """
    def __init__(self, cgv, taskid, cgfile, txtpath):
        self.cgver = cgv
        self.taskid = taskid
        self.cgfile = cgfile
        self.txtpath = txtpath

    def execute(self):
        """ update pyp & run c4d.exe """
        self.__update_pyp_script()

        """ run c4d """
        c4d_cmdline = '"C:/Program Files/MAXON/%s/CINEMA 4D 64 Bit.exe" -taskId:%s -cgFile:%s -txtPath:%s' % \
             (self.cgver, self.taskid, self.cgfile, self.txtpath)
        prog = subprocess.Popen(c4d_cmdline, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        out, err = prog.communicate()
        print(out, err)

    def __update_pyp_script(self):
        src = pyp_rel_path
        dst = maxon_data_path % (c4d_pyp_config[self.cgver])

        self.__copy_file(src, dst)

    def __copy_file(self, src, dst):
        os.system('xcopy /f /y /e "%s" "%s"' % (src, dst))

if __name__ == '__main__':
    args = sys.argv

    cg_ver = args[1]
    task_id = args[2]
    cg_file = args[3]
    txt_path = args[4]

    c4d_loader = C4dLoader(cg_ver, task_id, cg_file, txt_path)
    c4d_loader.execute()
