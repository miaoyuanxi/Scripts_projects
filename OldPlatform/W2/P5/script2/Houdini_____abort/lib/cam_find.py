import hou
import os,sys

def abc_find(path=""):
   if path != "":
      cam_pl = path.split("/")
      if len(cam_pl)>0:
          node_pre = ""
          i=0
          n_types = ["alembicarchive","alembicxform","cam"]
          pathval = {}
          index = 1
          type_abc = False
          first_key = ""          
          for elm in cam_pl:
              if not elm=="" and not elm=="..":
                node_pre += "/"+elm             
                if hou.node(node_pre).type().name() in n_types:
                      if index==1:
                          if hou.node(node_pre).type().name()=="alembicarchive":
                              type_abc = True
                              first_key = elm

                      if type_abc==True:                          
                          p_val = hou.node(node_pre).parm("fileName").eval()
                          #print(hou.node(node_pre).type().name())
                          #print("\t%s" % p_val)
                          pathval[elm] = p_val                          
                      index+=1
              
          if len(pathval)>2:                     
              vals = pathval[first_key]
              same_p = True
              keys = None
              for elm in pathval:                          
                  if not pathval[elm] == vals:
                       same_p =False
                       keys = elm
              if same_p==True:
                  if not os.path.exists(vals):
                       print("\tThe cam donot exist on the server!")
                       print("\t\t%s" % vals)
              else:
                  print("\nABC cam with diffrenct path")
                  print("Base path:\t")
                  print("\t> %s" % vals)
                  print("\tNode:\t%s\t" % keys)
                  print("\t\t> %s" % pathval[keys])
                     
                     

def main():
    nodes = hou.node("/out").children()
    print("--"*20)
    print(">>Cameras")
    if len(nodes)>0:       
       for elm in nodes:
           if elm.type().name() == 'ifd':
               cam_node = elm.parm("camera").eval()
               
               if hou.node(cam_node):
                    print("\nNode:\t%s" % elm)
                    print("Camera exist!")
                    abc_find(cam_node)
               else:
                    print("\nNode:\t%s" % elm)
                    print("The cam donot exist!")
                    print("\tCam:\t%s" % cam_node)
    print(">>Cameras\n ")