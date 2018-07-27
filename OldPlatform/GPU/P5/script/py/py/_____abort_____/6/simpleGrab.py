#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-
import logging
import os
import sys
import subprocess
import string
import time
import shutil
import threading
import time
from PIL import Image   
from PIL import ImageGrab
import PIL
import psutil

reload(sys)
sys.setdefaultencoding('utf-8')


im=ImageGrab.grab()
im.save('c:/work/test.jpg')