#.A ---- customer cannot assign folder
#.B ---- customer can assign folder
#.d ---- the item is a folder
#.f ---- the item is a file

import bpy, sys, re

wfile = open('RB_blender_debug.txt','w+')
wfile.write("------------debug-----------------")

def blend(rfile_name):
	rHandle = open(rfile_name,'r')
        #output texture path
	bpy.data.scenes[0].render.resolution_percentage = 100

	while True:
		eachLine = rHandle.readline()
		if not eachLine:
 			break
		
		#print("....."+eachLine) 
		if eachLine.split('.')[0] == "Clips":  
			for image in bpy.data.images:
				image.filepath = eachLine.split('::')[1]
		if eachLine.split('::')[0] == "Width":
			w = eachLine.split('::')[1]
			print("w____"+w)
			bpy.data.scenes[0].render.resolution_x = int(w)
		if eachLine.split('::')[0] == "Height":
			h = eachLine.split('::')[1]
			print("h___"+h)
			bpy.data.scenes[0].render.resolution_y = int(h)
	rHandle.close


#sys.stdout.write("write-------------.." +sys.argv[10])
print("print-------------.." +sys.argv[10])
wfile.write("\n==------"+sys.argv[10]+"----------\n")
wfile.close()
blend(sys.argv[10])