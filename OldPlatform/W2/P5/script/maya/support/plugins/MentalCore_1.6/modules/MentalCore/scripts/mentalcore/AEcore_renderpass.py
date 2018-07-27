#  Copyright (c)2012 Core CG
#  All rights reserved
#  www.core-cg.com

from functools import partial
import maya.cmds as cmds
    

def createLayout(node):
    #check maya version
    maya_ver = int(cmds.about(f=True))
        
    maya2013 = False
    if maya_ver >= 2013:
        maya2013 = True
        
    if not maya2013:
        return

    #Create Main Layout
    cmds.columnLayout(adj=True)
    
    #Create Metadata button
    cmds.button('mc_rpmeta_create', l='Add Metadata', c=lambda *args: create_metadata(node))
        
    cmds.separator()

    #Metadata Layout
    cmds.columnLayout('mc_rpmeta_layout', rs=1, adj=True)
    
    #Refresh layout
    refreshLayout(node)
    
    
def refreshLayout(node):
    #check maya version
    maya_ver = int(cmds.about(f=True))
        
    maya2013 = False
    if maya_ver >= 2013:
        maya2013 = True
        
    if not maya2013:
        return
        
    #Set parent
    cmds.setParent('mc_rpmeta_layout')

    #modify create button
    cmds.button('mc_rpmeta_create', e=True, c=lambda *args: create_metadata(node))
    
    #Delete existing children
    child_array = cmds.layout('mc_rpmeta_layout', q=True, ca=True)
    if child_array:
        for child in child_array:
            cmds.deleteUI(child)
            
    #List all meta data attributes
    meta_attrs = cmds.listAttr(node, m=True, v=True, c=True, st='metadata')
    
    cmds.setUITemplate('attributeEditorTemplate', pushTemplate=True)
    
    if meta_attrs:
        for attr in meta_attrs:
            #Full metadata attribute
            full_attr = '%s.%s' % (node, attr)
            
            #Column layout
            cmds.columnLayout(adj=True, dtg=full_attr)
               
            #Key Row layout
            cmds.rowLayout(nc=4, adj=4, cw4=[30, 20, 80, 100])

            #Delete data
            cmds.iconTextButton(l='', mw=0, mh=0, h=24, image='smallTrash.png', c=partial(delete_metadata, full_attr))

            #Enable data
            en_check = cmds.checkBox(l='')
            cmds.connectControl(en_check, '%s.meta_enable' % full_attr)
            
            cmds.scriptJob(attributeChange=['%s.meta_enable' % full_attr, partial(update_metadata_enable, full_attr)], 
                            protected=True, 
                            parent=en_check)
            
            #Data Type
            meta_type = cmds.attrEnumOptionMenuGrp( l='',
                            cw=[1, 1],
                            at='%s.meta_type' % full_attr,
                            ei=[(0, 'String'),(1, 'Boolean'), (2, 'Integer'), (3, 'Scalar'), (4, 'Vector') ] )
                            
            cmds.scriptJob(attributeChange=['%s.meta_type' % full_attr, partial(update_metdata_type, full_attr)], 
                            protected=True, 
                            parent=meta_type)
            
            #Data Key
            key_field = cmds.textFieldGrp(l='Key:', cw2=[22, 70])
            cmds.connectControl(key_field, '%s.meta_key' % full_attr, index=2)
            
            cmds.setParent('..')
            
            #Value Row layout
            cmds.rowLayout(nc=4, adj=3, cw4=[126, 32, 100, 2])
            
            cmds.separator(style='none', h=24)
            
            cmds.text(l='Value:')
            
            data_layout = cmds.columnLayout(adj=True)
            
            #Data Controls
            string_data = cmds.textField(vis=False)
            cmds.connectControl(string_data, '%s.meta_string' % full_attr)
            
            bool_data = cmds.checkBoxGrp(l='', cw=[1,0], vis=False)
            cmds.connectControl(bool_data, '%s.meta_bool' % full_attr, index=2)
            
            int_data = cmds.intField(vis=False)
            cmds.connectControl(int_data, '%s.meta_int' % full_attr)
            
            scalar_data = cmds.floatField(vis=False)
            cmds.connectControl(scalar_data, '%s.meta_scalar' % full_attr)
            
            vector_data = cmds.floatFieldGrp(l='', nf=3, cw4=[0,65,65,65], vis=False)
            cmds.connectControl(vector_data, '%s.meta_vectorX' % full_attr, index=2)
            cmds.connectControl(vector_data, '%s.meta_vectorY' % full_attr, index=3)
            cmds.connectControl(vector_data, '%s.meta_vectorZ' % full_attr, index=4)
            
            cmds.setParent('..')
            
            cmds.separator(style='none', w=2)
            
            cmds.setParent('..')
            
            #Update meta data
            update_metadata_enable(full_attr)
            update_metdata_type(full_attr)
            
            cmds.separator()
            
            cmds.setParent('..')

    cmds.setUITemplate(popTemplate=True)

def update_metadata_enable(attr):
    #find matching metadata ui
    child_array = cmds.layout('mc_rpmeta_layout', q=True, ca=True)
    
    for child in child_array:
        if attr == cmds.layout(child, q=True, dtg=True): #Found
            #Find matching control, hide others
            enabled = cmds.getAttr('%s.meta_enable' % attr)
            layouts = cmds.layout(child, q=True, ca=True)
            
            grandchildren = cmds.layout(layouts[0], q=True, ca=True)[2:]
            
            for control in grandchildren:
                cmds.control(control, e=True, en=enabled)
                
            grandchildren = cmds.layout(layouts[1], q=True, ca=True)
            
            for control in grandchildren:
                cmds.control(control, e=True, en=enabled)
                
            break
    
def update_metdata_type(attr):
    #find matching metadata ui
    child_array = cmds.layout('mc_rpmeta_layout', q=True, ca=True)

    for child in child_array:
        if attr == cmds.layout(child, q=True, dtg=True): #Found
            #Find matching control, hide others
            type = cmds.getAttr('%s.meta_type' % attr)
            value_layout = cmds.layout(child, q=True, ca=True)[1]
            type_layout = cmds.layout(value_layout, q=True, ca=True)[-2]
            type_controls = cmds.layout(type_layout, q=True, ca=True)
            match_control = None
                        
            for i in range(len(type_controls)):
                control = type_controls[i]
                if type == i:
                    match_control = control
                else:
                    cmds.control(control, e=True, vis=False)
              
            #Show matched control
            if match_control:     
                cmds.control(match_control, e=True, vis=True)
            
            break
            
def create_metadata(node):
    #find next attribute
    meta_attrs = cmds.listAttr(node, m=True, v=True, c=True, st='metadata')
    if meta_attrs:
        last_attr = meta_attrs[-1]
        last_attr = last_attr.replace('metadata[', '')
        last_attr = last_attr.replace(']', '')
        
        cmds.getAttr('%s.metadata[%i].meta_enable' % (node, int(last_attr) + 1))
    else:
        cmds.getAttr('%s.metadata[0].meta_enable' % node)
            
def delete_metadata(attr):
    #find matching metadata ui
    child_array = cmds.layout('mc_rpmeta_layout', q=True, ca=True)
    
    for child in child_array:
        if attr == cmds.layout(child, q=True, dtg=True): #Found
            cmds.deleteUI(child)
            break
            
    cmds.removeMultiInstance(attr)