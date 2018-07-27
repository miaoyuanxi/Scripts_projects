#! /usr/bin/env python
#coding=utf-8
import pymel.core as pm

if user_id in [962413]:
    for i in pm.ls(type="aiStandIn"):
        i.deferStandinLoad.set(0)
        print "set %s to 0" % (i.deferStandinLoad)
if user_id in [1814975]:
    for i in pm.ls(type='aiOptions'):
        if i.hasAttr("autotx"):
            i.autotx.set(False)
