#!/usr/bin/env python
#encoding:utf-8
# -*- coding: utf-8 -*-

import logging
import os
import sys



import ConfigParser
conf = ConfigParser.ConfigParser()
conf.read(r"\\10.50.8.15\p5\temp\56299_render\cfg\render.cfg")
storage = conf.get("client", "storage_texture")

print storage