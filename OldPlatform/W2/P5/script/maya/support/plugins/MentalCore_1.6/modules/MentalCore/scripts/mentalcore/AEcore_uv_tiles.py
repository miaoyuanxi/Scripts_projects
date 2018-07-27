#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com


from functools import partial
import maya.cmds as cmds


def createLayout(node):
    cmds.columnLayout(adj=True)
    
    cmds.button('AEcore_uv_tiles_create', l='Add UV Tile', c=lambda *args: createNewTile(node))
    
    cmds.columnLayout('AEcore_uv_tiles_tiles', adj=True)
    
    refreshLayout(node)
    

def refreshLayout(node):
    #modify create button
    cmds.button('AEcore_uv_tiles_create', e=True, c=lambda *args: createNewTile(node))
    
    to_del = cmds.layout('AEcore_uv_tiles_tiles', q=True, ca=True)
    if to_del:
        for ui in to_del:
            cmds.deleteUI(ui)
            
            
    attrList = cmds.listAttr(node, m=True, v=True, c=True, st='tiles')
    if attrList:
        for attr in attrList:
            tile_attr = '%s.%s' % (node, attr)
            attr_num = attr.replace('tiles[', '')
            attr_num = int(attr_num.replace(']', ''))
    
            cmds.setParent('AEcore_uv_tiles_tiles')
        
            
            layout = cmds.frameLayout(l='Tile %i' % attr_num, collapse=0)
            
            cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)
            
            cmds.columnLayout(rs=1, adj=True)
            
            #Enabled
            cmds.rowLayout(nc=2, cw2=[148, 140], cat=[1, 'left', 0])
            cmds.iconTextButton(style='iconOnly', h=25, mw=0, mh=0, image='smallTrash.png', c=partial(deleteTile, tile_attr, layout))
            
            enabled = cmds.checkBox(l='Enable')
            cmds.connectControl(enabled, '%s.enabled' % tile_attr)
            cmds.setParent('..')
            
            #index
            index = cmds.intFieldGrp( numberOfFields=2, label='Tile Index', value1=0, value2=0)
            cmds.connectControl(index, '%s.index_x' % tile_attr, index=2)
            cmds.connectControl(index, '%s.index_y' % tile_attr, index=3)
            
            #maya texture
            cmds.attrColorSliderGrp( l='Texture', at='%s.texture' % tile_attr )
            
            #alpha
            cmds.attrControlGrp(l='Alpha', attribute='%s.alpha' % tile_attr)
            
            
            cmds.setUITemplate(popTemplate=True)
            
            
    
def createNewTile(node):
    attrList = cmds.listAttr(node, m=True, v=True, c=True, st='tiles')

    i = 0
    if cmds.listAttr(node, m=True, v=True, c=True, st='tiles'):
        while 'tiles[%i]' % i in cmds.listAttr(node, m=True, v=True, c=True, st='tiles'):
            i += 1
            
            
    cmds.getAttr ('%s.tiles[%i].enabled' % (node, i))
            
    
def deleteTile(attr, layout, *args):
    cmds.removeMultiInstance(attr, b=True)
    
