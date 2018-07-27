#! /usr/bin/env python
#coding=utf-8



import os
import os.path
import sys

# os.environ[ "NUKE_INTERACTIVE" ] = '1'



input_file = sys.argv[1]
output_file = sys.argv[2]

rootdir = input_file




if os.path.exists(r'C:/Program Files/Nuke10.0v4/'):
    runpath = 'C:/Program Files/Nuke10.0v4'
    
if os.path.exists(r'C:/Program Files/Nuke10.5v5/'):
    runpath = 'C:/Program Files/Nuke10.5v5'
        
        
# runpath = 'C:/Program Files/Nuke10.0v4'

os.environ['HFS'] = runpath
_PATH_ORG = os.environ.get('PATH')
os.environ['PATH'] = (_PATH_ORG if _PATH_ORG else "") + r";" + runpath
libpath = "%s/lib" % (runpath)
_PATH_New = os.environ.get('PATH')
print "_PATH_New = " + _PATH_New
sitepath = "%s/lib/site-packages" % (runpath)
if libpath not in sys.path:
    sys.path.append(libpath)
if sitepath not in sys.path:
    sys.path.append(sitepath)

import nuke
print "5555555"
for parent, dirnames, filenames in os.walk(rootdir):
    for filename in filenames:  
        pa_list = parent.split('\\')
        parent = "/".join(pa_list)
        print "parent is: " + parent
        print "filename is: " + filename
        print "the full name of the file is: " + os.path.join(parent, filename)

        texture_file = parent + "/"  + filename

        print texture_file
        path_list = parent.split("/")[6:]

        new_path = output_file + '/'+'/'.join(path_list)
        new_out_put =  new_path + '/'+ filename
        
        print "new_path" + new_path
        new_path.replace("/","\\")
        new_path=new_path.strip()
        new_path=new_path.rstrip("\\")
        
        isExists=os.path.exists(new_path)
       
        if not isExists:
            
            os.makedirs(new_path)      

        else:

            print new_path +' is exist '


        print "new_out_put:" + new_out_put
        shot = texture_file
        print "shot:" + shot
        
        r = nuke.nodes.Read(file=shot)

        if r.metadata() == '':
            print "false"
        else:
            print "true"

            g = nuke.nodes.Reformat( inputs=[r] )
            g['format'].setValue( "HD_1080" )

            w = nuke.nodes.Write(file = new_out_put, inputs=[g]) 
            w['file_type'].setValue( "exr" )
            w['datatype'].setValue( "32" )



            nuke.execute( w, 1, 1 )
    




