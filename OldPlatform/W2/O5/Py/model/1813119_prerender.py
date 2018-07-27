import pymel.core as pm
print "+++++++++++++++++++++++++++++++++the prerender strat++++++++++++++++++++++++++++++++++++++++++++++++"

print PXO
for i in pm.ls(type="aiOptions"):
    if i.hasAttr("log_verbosity"):
        i.log_verbosity.set(2)
    if i.hasAttr("autotx"):
        i.autotx.set(False)
    if i.hasAttr("textureMaxMemoryMB"):
        i.textureMaxMemoryMB.set(20480)
        print "set arnold textureMaxMemoryMB 20480 "

'''
d = {
         "defaultRenderGlobals": {"renderVersion": "v002"},
         "defaultArnoldRenderOptions": {"GIDiffuseSamples": 10,
"renderType": 2},
         }
'''
def maya_startup(dict_):
     nodes = ["defaultRenderGlobals", "defaultArnoldRenderOptions"]
     for node in nodes:
         if dict_.get(node):
             for k, v in dict_.get(node).items():
                 current_node =  pm.PyNode(node)
                 current_node.setAttr(k, v )
                 print "setAttr %s %s %s " % (current_node,k,v)


maya_startup(PXO)

print "**********************************************the prerender end******************************************************"