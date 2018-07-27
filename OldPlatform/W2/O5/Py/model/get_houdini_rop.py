import sys
import os
import json

cfg_path = r"\\10.50.244.116\d\ninputdata5\%s\temp" % (sys.argv[1])
task_info = eval(open(os.path.join(cfg_path, "server.cfg"), "r").read())

print task_info["rop"]
