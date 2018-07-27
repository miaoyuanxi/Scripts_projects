# # ! /usr/bin/env python
# # coding=utf-8
import os
import re
import maya.cmds as cmds 
import pymel.core as pm
for i in pm.ls(type='aiOptions'):
	if i.hasAttr("autotx"):
		i.autotx.set(False)
