import maya.cmds as cmds
import maya.mel
import pymel.core as pm
cmds.dirmap( en=True )
cmds.dirmap( m=('X:', '//10.99.1.13'))
cmds.dirmap( m=('O:', '//10.99.1.2/digital/film_projec'))
print("Mapping successfully")
