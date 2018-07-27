#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com

import re
from functools import partial
import maya.cmds as cmds


class layer():
    def __init__(self, attr):
        self.attr = attr
        self.enabled = True
        self.name = ''
        self.blend_mode = 0
        self.colour = (0.0, 0.0, 0.0)
        self.opacity = 1.0
        self.inv_opacity = False
        
    def break_connections(self):
        #enabled
        if type(self.enabled) in (str, unicode) and cmds.objExists(self.enabled):
            cmds.disconnectAttr(self.enabled, '%s.enabled' % self.attr)
            
        #blend_mode
        if type(self.blend_mode) in (str, unicode) and cmds.objExists(self.blend_mode):
            cmds.disconnectAttr(self.blend_mode, '%s.blend_mode' % self.attr)
            
        #colour
        if type(self.colour) in (str, unicode) and cmds.objExists(self.colour):
            cmds.disconnectAttr(self.colour, '%s.colour' % self.attr)
            
        #opacity
        if type(self.opacity) in (str, unicode) and cmds.objExists(self.opacity):
            cmds.disconnectAttr(self.opacity, '%s.opacity' % self.attr)
            
        #inv_opacity
        if type(self.inv_opacity) in (str, unicode) and cmds.objExists(self.inv_opacity):
            cmds.disconnectAttr(self.inv_opacity, '%s.inv_opacity' % self.attr)
        
    def move_up(self, *args):
        self.move(True)
        
    def move_down(self, *args):
        self.move(False)
        
    def move(self, up):
        node, attr = self.attr.split('.')
        layers = collect_layer_info(node)
        
        #find layer to swap with
        cur_layer = None
        swap_layer = None
        for i in range(len(layers)):
            if layers[i].attr == self.attr:
                cur_layer = layers[i]
                if up:
                    swap_layer = layers[i-1]
                else:
                    swap_layer = layers[i+1]
        
        #break connections
        cur_layer.break_connections()
        swap_layer.break_connections()
        
        #reconnect attributes
        
        #name
        cmds.setAttr('%s.name' % cur_layer.attr, swap_layer.name, type="string")
        cmds.setAttr('%s.name' % swap_layer.attr, cur_layer.name, type="string")
        
        #enabled
        if type(swap_layer.enabled) in (str, unicode) and cmds.objExists(swap_layer.enabled):
            cmds.connectAttr(swap_layer.enabled, '%s.enabled' % cur_layer.attr, f=True)
        else:
            cmds.setAttr('%s.enabled' % cur_layer.attr, swap_layer.enabled)
        
        if type(cur_layer.enabled) in (str, unicode) and cmds.objExists(cur_layer.enabled):
            cmds.connectAttr(cur_layer.enabled, '%s.enabled' % swap_layer.attr, f=True)
        else:
            cmds.setAttr('%s.enabled' % swap_layer.attr, cur_layer.enabled)
            
        #blend_mode
        if type(swap_layer.blend_mode) in (str, unicode) and cmds.objExists(swap_layer.blend_mode):
            cmds.connectAttr(swap_layer.blend_mode, '%s.blend_mode' % cur_layer.attr, f=True)
        else:
            cmds.setAttr('%s.blend_mode' % cur_layer.attr, swap_layer.blend_mode)
        
        if type(cur_layer.blend_mode) in (str, unicode) and cmds.objExists(cur_layer.blend_mode):
            cmds.connectAttr(cur_layer.blend_mode, '%s.blend_mode' % swap_layer.attr, f=True)
        else:
            cmds.setAttr('%s.blend_mode' % swap_layer.attr, cur_layer.blend_mode)
            
        #colour
        if type(swap_layer.colour) in (str, unicode) and cmds.objExists(swap_layer.colour):
            cmds.connectAttr(swap_layer.colour, '%s.colour' % cur_layer.attr, f=True)
        else:
            cmds.setAttr('%s.colour' % cur_layer.attr, swap_layer.colour[0], swap_layer.colour[1], swap_layer.colour[2])
        
        if type(cur_layer.colour) in (str, unicode) and cmds.objExists(cur_layer.colour):
            cmds.connectAttr(cur_layer.colour, '%s.colour' % swap_layer.attr, f=True)
        else:
            cmds.setAttr('%s.colour' % swap_layer.attr, cur_layer.colour[0], cur_layer.colour[1], cur_layer.colour[2])
            
        #opacity
        if type(swap_layer.opacity) in (str, unicode) and cmds.objExists(swap_layer.opacity):
            cmds.connectAttr(swap_layer.opacity, '%s.opacity' % cur_layer.attr, f=True)
        else:
            cmds.setAttr('%s.opacity' % cur_layer.attr, swap_layer.opacity)
        
        if type(cur_layer.opacity) in (str, unicode) and cmds.objExists(cur_layer.opacity):
            cmds.connectAttr(cur_layer.opacity, '%s.opacity' % swap_layer.attr, f=True)
        else:
            cmds.setAttr('%s.opacity' % swap_layer.attr, cur_layer.opacity)
            
        #inv_opacity
        if type(swap_layer.inv_opacity) in (str, unicode) and cmds.objExists(swap_layer.inv_opacity):
            cmds.connectAttr(swap_layer.inv_opacity, '%s.inv_opacity' % cur_layer.attr, f=True)
        else:
            cmds.setAttr('%s.inv_opacity' % cur_layer.attr, swap_layer.inv_opacity)
        
        if type(cur_layer.enabled) in (str, unicode) and cmds.objExists(cur_layer.inv_opacity):
            cmds.connectAttr(cur_layer.inv_opacity, '%s.inv_opacity' % swap_layer.attr, f=True)
        else:
            cmds.setAttr('%s.inv_opacity' % swap_layer.attr, cur_layer.inv_opacity)
            
        #Refresh Layers
        refreshLayout(node)
        
    def __str__(self):
        return ('Attr: %s\nEnabled: %s, Name: %s, BlendMode: %s, Colour: %s, Opacity: %s, InvOpacity: %s' % (self.attr, str(self.enabled), str(self.name), str(self.blend_mode), str(self.colour), str(self.opacity), str(self.inv_opacity)))
        
        
def collect_layer_info(node):
    layers_info = []

    attrList = cmds.listAttr(node, m=True, v=True, c=True, st='layer')
    if attrList:
        for layer_attr in attrList:
            layer_attr = '%s.%s' % (node, layer_attr)
            layer_info = layer(layer_attr)
            
            #enabled
            enabled = cmds.listConnections('%s.enabled' % layer_attr, s=True, d=False, p=True)
            if enabled:
                layer_info.enabled = enabled[0]
            else:
                layer_info.enabled = cmds.getAttr('%s.enabled' % layer_attr)
                
            #name
            layer_info.name = cmds.getAttr('%s.name' % layer_attr)
                
            #blendmode
            enabled = cmds.listConnections('%s.blend_mode' % layer_attr, s=True, d=False, p=True)
            if enabled:
                layer_info.blend_mode = enabled[0]
            else:
                layer_info.blend_mode = cmds.getAttr('%s.blend_mode' % layer_attr)
                
            #colour
            enabled = cmds.listConnections('%s.colour' % layer_attr, s=True, d=False, p=True)
            if enabled:
                layer_info.colour = enabled[0]
            else:
                layer_info.colour = cmds.getAttr('%s.colour' % layer_attr)[0]
                
            #opacity
            enabled = cmds.listConnections('%s.opacity' % layer_attr, s=True, d=False, p=True)
            if enabled:
                layer_info.opacity = enabled[0]
            else:
                layer_info.opacity = cmds.getAttr('%s.opacity' % layer_attr)
                
            #inv opacity
            enabled = cmds.listConnections('%s.inv_opacity' % layer_attr, s=True, d=False, p=True)
            if enabled:
                layer_info.inv_opacity = enabled[0]
            else:
                layer_info.inv_opacity = cmds.getAttr('%s.inv_opacity' % layer_attr)
            
            layers_info.append(layer_info)
            
    return layers_info


def createLayout(node):
    cmds.columnLayout(adj=True)
    
    cmds.button('AEcore_texture_blend_create', l='Create Layer', c=lambda *args: createNewLayer(node))
    
    cmds.columnLayout('AEcore_texture_blend_layers', adj=True)
    
    refreshLayout(node)
    
    
def refreshLayout(node):
    #modify create button
    cmds.button('AEcore_texture_blend_create', e=True, c=lambda *args: createNewLayer(node))
    
    to_del = cmds.layout('AEcore_texture_blend_layers', q=True, ca=True)
    if to_del:
        for ui in to_del:
            cmds.deleteUI(ui)
    
    layers_info = collect_layer_info(node)
    if layers_info:
        for layer in layers_info:
            cmds.setParent('AEcore_texture_blend_layers')
        
            
            layout = cmds.frameLayout(l='Layer: "%s"' % layer.name, collapse=0)
            
            cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)
            
            cmds.columnLayout(rs=1, adj=True)
            
            #Enabled
            cmds.rowLayout(nc=6, cw6=[30, 25, 25, 60, 138, 100], cat=[1, 'left', 0])
            cmds.iconTextButton(style='iconOnly', h=25, mw=0, mh=0, image='smallTrash.png', c=partial(deleteLayer, layer.attr, layout))
            
            up_enabled = True
            down_enabled = True
            if layer == layers_info[0]:
                up_enabled = False
            if layer == layers_info[-1]:
                down_enabled = False
            
            cmds.symbolButton(image='arrowUp.png', en=up_enabled, c=layer.move_up)
            cmds.symbolButton(image='arrowDown.png', en=down_enabled, c=layer.move_down)
            
            cmds.separator(style='none')
            
            enabled = cmds.checkBox(l='Enable')
            cmds.connectControl(enabled, '%s.enabled' % layer.attr)
            
            #inv opacity
            inv_opacity = cmds.checkBox(l='Invert Opacity')
            cmds.connectControl(inv_opacity, '%s.inv_opacity' % layer.attr)
        
            cmds.setParent('..')
            
            #Name
            name = cmds.textFieldGrp(l='Name', tx=cmds.getAttr('%s.name' % layer.attr), cc=partial(renameLayer, layer.attr, layout))
            
            #Blend Mode
            cmds.attrEnumOptionMenuGrp(l='Blend Mode',
                    at='%s.blend_mode' % layer.attr,
                    ei = [(0, "Normal"),
                    (1, "Darken"),
                    (2, "Multiply"),
                    (3, "Color Burn"),
                    (4, "Inverse Color Burn"),
                    (5, "Subtract"),
                    (6, "Add"),
                    (7, "Lighten"),
                    (8, "Screen"),
                    (9, "Color Dodge"),
                    (10, "Inverse Color Dodge"),
                    (11, "Overlay"),
                    (12, "Soft Light"),
                    (13, "Hard Light"),
                    (14, "Reflect"),
                    (15, "Glow"),
                    (21, "Illuminate"),
                    (16, "Average"),
                    (17, "Difference"),
                    (18, "Exclusion"),
                    (19, "Min"),
                    (20, "Max")])
                    
            #Colour
            cmds.attrColorSliderGrp( l='Colour', at='%s.colour' % layer.attr )
            
            #opacity
            cmds.attrFieldSliderGrp( l='Opacity', min=0, max=1, at='%s.opacity' % layer.attr )
            
            cmds.setUITemplate(popTemplate=True)
            
    
def createNewLayer(node):
    index = 0
    attrList = cmds.listAttr(node, m=True, v=True, c=True, st='layer')
    if attrList:
        match = re.search('.*\[([0-9]*)\]', attrList[-1])
        if match:
            index = int(match.groups()[0])
            index += 1
            
    if index == 0:
        label = 'Base Layer'
    else:
        label = 'Layer %i' % (len(attrList) + 1)
            
    cmds.setAttr ('%s.layer[%i].name' % (node, index), label, type="string")
            
    
def deleteLayer(attr, layout, *args):
    cmds.removeMultiInstance(attr, b=True)
    
    
def renameLayer(attr, layout, *args):
    new_name = args[0]
    cmds.setAttr ('%s.name' % attr, new_name, type="string")
    cmds.frameLayout(layout, e=True, l='Layer: "%s"' % new_name)
