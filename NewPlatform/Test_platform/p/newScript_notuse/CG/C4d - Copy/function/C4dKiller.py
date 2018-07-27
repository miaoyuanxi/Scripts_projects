""" C4d killer """
#!/usr/bin/python
# -*- coding=utf-8 -*-
# Author: kaname
# QQ: 1394041054

import os

def kill_c4d_app():
    """ kill all c4d process """
    kill_command = './taskkill.exe /F /IM "CINEMA 4D 64 Bit.exe"'
    os.system(kill_command)

if __name__ == '__main__':
    kill_c4d_app()
