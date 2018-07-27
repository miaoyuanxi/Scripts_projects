#  Copyright (c)2011 Core CG
#  All rights reserved
#  www.core-cg.com


## ------------------------------------------------------------------------
## IMPORTS
## ------------------------------------------------------------------------
import sys, os, re
import shutil
from datetime import datetime, date
import base64

import maya.cmds as cmds
import maya.mel as mel

## ------------------------------------------------------------------------
## UTILITY FUNCTIONS
## ------------------------------------------------------------------------	
def connect_next_avaliable(source, destination):
    dest_node, dest_attr = destination.split('.')
    i = 0
    while True:
        cur_attr = '%s[%i]' % (destination, i)
        if cmds.listConnections(cur_attr) == None:
            cmds.connectAttr(source, cur_attr, f=True)        
            return
        i += 1
        
def disconnect_next_avaliable(source, destination):
    src_node, src_attr = source.split('.')
    
    conn = cmds.listConnections(destination, p=True, c=True)
    if conn:
        for i in range(len(conn)/2):
            i *= 2
            dest_conn = conn[i]
            src_conn = conn[i+1]
            
            if src_conn == source:
                cmds.disconnectAttr(src_conn, dest_conn)

def clamp_precision(value, precision):
    format_str = '%.' + str(precision) + 'f'
    return float(format_str % value)

## ------------------------------------------------------------------------
## LICENSE FUNCTIONS
## ------------------------------------------------------------------------	
            
LIC_RE = re.compile('''LICENSE corecg mentalcore (?P<version>[0-9]\.[0-9]) (?P<expiry>[0-9]*-[A-Z]*-[0-9]*)''', re.IGNORECASE)
            
# Find mentalcore license
def find_license():
    '''Locates the path to the license file that RLM will be looking for'''
    lic_path = None
    lic_file = None
    
    #Platform specific license paths
    common_path = None
    if sys.platform == 'win32':
        common_path = r'C:\MentalCore'
    elif sys.platform == 'darwin':
        common_path = r'/Users/Shared/MentalCore'
    elif sys.platform == 'linux2':
        common_path = r'/usr/local/MentalCore'
    
    #Pick license file
    if os.environ.has_key('MENTALCORE_LICENSE'):
        lic_path = os.environ['MENTALCORE_LICENSE']
    elif common_path and os.path.exists(os.path.join(common_path, 'mentalcore.lic')):
        lic_path = common_path
    elif os.environ.has_key('MAYA_LOCATION'):
        lic_path = os.environ['MAYA_LOCATION']
        lic_path = os.path.join(os.path.normpath(lic_path), 'mentalray')
        
    if lic_path:
        lic_path = os.path.normpath(lic_path)
        if os.path.exists(lic_path):
            if 'mentalcore.lic' in os.listdir(lic_path):
                lic_file = os.path.join(lic_path, 'mentalcore.lic')
                
    return lic_file
    

#read license file
def read_license():
   lic_file = find_license()
   if lic_file and os.path.exists(lic_file):
       #read in license text
       f = open(lic_file, 'r')
       lic_text = f.read()
       f.close()

       return lic_text.strip()

#check if license is expired
def get_license_expiry():
    lic_text = read_license()
    if lic_text:
        match = LIC_RE.match(lic_text)
        if match:
            expiry = match.group('expiry')
            return datetime.strptime(expiry, '%d-%b-%Y').date()
            
#check when license expires
def is_license_expired():
    exp_date = get_license_expiry()
    if exp_date:
        cur_date = date.today()
        if cur_date > exp_date:
            return True
    return False

#is license valid
def is_license_valid():
    lic_text = read_license()
    if lic_text:
        if lic_text.startswith('LICENSE corecg mentalcore') or lic_text.startswith('HOST ') or lic_text.startswith('SERVER '):
            return True
    return False
   
#install license
def install_licence(fileName, fileType=None):
    if fileName and os.path.exists(fileName):
        #Platform specific license paths
        install_dir = None
        if sys.platform == 'win32':
            install_dir = r'C:\MentalCore'
        elif sys.platform == 'darwin':
            install_dir = r'/Users/Shared/MentalCore'
        elif sys.platform == 'linux2':
            install_dir = r'/usr/local/MentalCore'
            
        try:
            #create folder
            if not os.path.exists(install_dir):
                os.makedirs(install_dir)
                
            #remove existing licence
            if os.path.exists(install_dir + '/mentalcore.lic'):
                os.remove(install_dir + '/mentalcore.lic')
                
            #copy licence
            shutil.copy(fileName, install_dir + '/mentalcore.lic')
            cmds.confirmDialog( title='Licence Installed', message='MentalCore Licence Installed To: "%s".\n\nPlease restart Maya' % (install_dir + '/mentalcore.lic'), button=['Ok'], defaultButton='Ok', cancelButton='No', dismissString='Ok' )
        
        except:
            cmds.confirmDialog( title='Error Installing Licence', message='Error installing licence, make sure you have write privilages to "%s".\nOr install license manually' % install_dir, button=['Ok'], defaultButton='Ok', cancelButton='No', dismissString='Ok' )

    
## ------------------------------------------------------------------------
## STRING OPTIONS
## ------------------------------------------------------------------------
class MiStringOption(object):
    def __init__(self, name, default=None):
        self._attr = self._find_attr(name)
        if not self._attr:
            self._attr = self._next_free_attr()
            self.name = name
            if not default == None:
                self.value = default

    def _find_attr(self, name):
        string_opts = cmds.listAttr('miDefaultOptions', m=True, v=True, c=True, st='stringOptions')
        if string_opts:
            for opt in string_opts:
                cur_name = cmds.getAttr('miDefaultOptions.%s.name' % opt)
                if cur_name == name:
                    return 'miDefaultOptions.%s' % opt

    def _next_free_attr(self):
        i = 0
        while True:
            cur_name = cmds.getAttr('miDefaultOptions.stringOptions[%i].name' % i)
            if not cur_name:
                return 'miDefaultOptions.stringOptions[%i]' % i
            i += 1

    def _get_name(self):
        return cmds.getAttr('%s.name' % self._attr)

    def _set_name(self, name):
        cmds.setAttr('%s.name' % self._attr, name, type='string')

    def _get_value(self):
        value = cmds.getAttr('%s.value' % self._attr)
        attr_type = cmds.getAttr('%s.type' % self._attr)

        if attr_type == 'boolean':
            if value == 'true':
                return True
            else:
                return False
        elif attr_type == 'integer':
            return int(value)
        elif attr_type == 'scalar':
            return float(value)
        elif attr_type == 'string':
            return str(value)

    def _set_value(self, value):
        if type(value) == bool:
            if value:
                cmds.setAttr('%s.value' % self._attr, 'true', type='string')
            else:
                cmds.setAttr('%s.value' % self._attr, 'false', type='string')
            cmds.setAttr('%s.type' % self._attr, 'boolean', type='string')
        elif type(value) == int:
            cmds.setAttr('%s.value' % self._attr, str(value), type='string')
            cmds.setAttr('%s.type' % self._attr, 'integer', type='string')
        elif type(value) == float:
            cmds.setAttr('%s.value' % self._attr, str(value), type='string')
            cmds.setAttr('%s.type' % self._attr, 'scalar', type='string')
        elif type(value) == str:
            cmds.setAttr('%s.value' % self._attr, str(value), type='string')
            cmds.setAttr('%s.type' % self._attr, 'string', type='string')
            
    def delete(self):
        cmds.removeMultiInstance(self._attr, b=True)

    name = property(_get_name, _set_name)
    value = property(_get_value, _set_value)
    
## ------------------------------------------------------------------------
## INTERFACE WIDGETS
## ------------------------------------------------------------------------
class NodeLinkWdget(object):
    def __init__(self, label, node_type, node_name=None):
        self.node_type = node_type
        self.node_name = node_name
        self.link_attr = None
        self._script_job = None
        self.create_hook = None
    
        self.layout = cmds.rowLayout(nc=3)
        cmds.text(l=label)
        self.create_b = cmds.button(l='Create')
        self.select_b = cmds.symbolButton(image='inArrow.png', c=self.select)
        cmds.setParent('..')
        
    def set_visible(self, value):
        cmds.layout(self.layout, e=True, vis=value)
        
    def select(self, *args):
        node = cmds.listConnections(self.link_attr)
        if node and not cmds.about(b=True):
            mel.eval('showEditor %s' % node[0])

    def create(self, *args):
        if self.node_name:
            node = cmds.shadingNode(self.node_type, asShader=True, n=self.node_name)
        else:
            node = cmds.shadingNode(self.node_type, asShader=True)
        
        cmds.connectAttr('%s.message' % node, self.link_attr, f=True)
        self.select()
        
        if self.create_hook:
            self.create_hook(node)
        
    def delete(self, *args):
        node = cmds.listConnections(self.link_attr)
        if node:
            cmds.delete(node[0])
        
    def update(self, *args):
        has_node = cmds.connectionInfo(self.link_attr, id=True)
        if has_node:
            cmds.button(self.create_b, e=True, l='Delete', c=self.delete)
        else:
            cmds.button(self.create_b, e=True, l='Create', c=self.create)
        cmds.control(self.select_b, e=True, en=has_node)
        
    def connect(self, link_attr):
        if self._script_job:
            cmds.scriptJob( kill=self._script_job, force=True)
    
        self.link_attr = link_attr
        self._script_job = cmds.scriptJob(attributeChange=[self.link_attr, self.update], protected=True, parent=self.create_b)
        self.update()
        
    
## ------------------------------------------------------------------------
## ENVIRONMENT PREVIEW
## ------------------------------------------------------------------------
def build_env_preview(env_tex):
    allGeo = cmds.ls(type=['nurbsSurface','mesh','subdiv'])

    #create geo
    env_sphere = cmds.sphere(ax=[0,1,0], r=1, d=3, s=8, nsp=4, ch=0, n='core_env_preview')
    env_sphere = env_sphere[0]
    
    cmds.setAttr('%s.rotateY' % env_sphere, 270)
    cmds.makeIdentity(env_sphere, apply=True, t=True, r=True, s=True)
    
    cmds.reverseSurface(env_sphere, d=3, rpo=1, ch=0)  

    cmds.setAttr('%s.miDeriveFromMaya' % env_sphere, False)
    cmds.setAttr('%s.miHide' % env_sphere, True)

    cmds.setAttr('%s.overrideEnabled' % env_sphere, True)
    cmds.setAttr('%s.overrideDisplayType' % env_sphere, 2)

    cmds.setAttr('%s.tx' % env_sphere, lock=True, keyable=False, channelBox=False)
    cmds.setAttr('%s.ty' % env_sphere, lock=True, keyable=False, channelBox=False)
    cmds.setAttr('%s.tz' % env_sphere, lock=True, keyable=False, channelBox=False)
    cmds.setAttr('%s.rx' % env_sphere, lock=True, keyable=False, channelBox=False)
    cmds.setAttr('%s.ry' % env_sphere, keyable=False, channelBox=False)
    cmds.setAttr('%s.rz' % env_sphere, lock=True, keyable=False, channelBox=False)

    #shader
    shader = cmds.shadingNode('surfaceShader', asShader=True, n='core_env_preview_shader')
    cmds.setAttr('%s.outTransparency' % shader, 0.3,0.3,0.3, type='double3')    

    cmds.select(env_sphere, r=True)    
    cmds.hyperShade(assign=shader)

    #set texture
    if env_tex.__class__ == unicode:
        cmds.connectAttr(env_tex, '%s.outColor' % shader, f=True)

        if cmds.nodeType(env_tex.split('.')[0]) == 'file':
            cmds.setAttr(env_tex.split('.')[0] + '.hdrMapping', 2)
            
        matInfo = cmds.listConnections(shader, type='materialInfo')
        if matInfo:
            cmds.connectAttr(env_tex, '%s.texture[0]' % matInfo[0], f=True)

    else:
        cmds.setAttr('%s.outColor' % shader, env_tex[0], env_tex[1], env_tex[2])    


    #scale
    newSize = 0
    if allGeo:
        bbox = cmds.exactWorldBoundingBox(allGeo)

        for bb in bbox:
            if abs(bb) > newSize:
                newSize = abs(bb)
    else:
        newSize = 10

    newSize *= 10
    cmds.setAttr('%s.scale' % env_sphere, newSize, newSize, newSize)

    return [env_sphere, shader]
    

def create_env_preview(env_node):
    if not cmds.objExists(env_node):
        raise Exception, 'Environment "%s" does not exist!' % env_node    

    mel.eval('source AEhardwareTextureTemplate.mel')
    
    #Store selection
    sel = cmds.ls(sl=True)

    #find texture
    env_tex = None
    inputs = cmds.listConnections('%s.env_tex' % env_node, s=True, d=False, p=True)
    if inputs:
        env_tex = inputs[0]
    else:
        env_tex = cmds.getAttr('%s.env_tex' % env_node)[0]

    #build env preview node
    geo, shader = build_env_preview(env_tex)
    cmds.select(shader, r=True)

    #connect
    if not cmds.objExists("%s.env_preview" % env_node):
        cmds.addAttr(env_node, at='message', ln='env_preview')
        
    cmds.connectAttr("%s.message" % shader, "%s.env_preview" % env_node, f=True)
    cmds.connectAttr("%s.env_rot" % env_node, "%s.ry" % geo, f=True)
    
    #Show AE
    cmds.select(sel, r=True)
    mel.eval('evalDeferred("showEditor \\"%s\\"")' % env_node)
    
    
## ------------------------------------------------------------------------
## ENV LIGHT LOCATORS
## ------------------------------------------------------------------------
def create_envlight_loc(n='envLightLoc', p=None):
    '''Creates a spherical env light locator'''
    #stored curve
    shape = '''MyAzOCAxIG5vIDMgCTQzIDAgMCAwIDEgMiAzIDQgNSA2IDcgOCA4IDggOSAxMCAxMSAxMiAxMyAx
        NCAxNSAxNiAxNiAxNiAxNyAxOCAxOSAyMCAyMSAyMiAJIDIzIDI0IDI0IDI0IDI1IDI2IDI3IDI4
        IDI5IDMwIDMxIDMyIDMyIDMyIAk0MSAJNi4xMjMyMzM5OTU3MzY3NjZlLTAxNyA2LjEyMzIzMzk5
        NTczNjc2NmUtMDE3IC0xIAktMC4xMzAwNjAyMTQ2Nzc0MTg4IDYuMTIzMjMzOTk1NzM2NzY2ZS0w
        MTcgLTEgCS0wLjM5MzAyNzgxNzM0MzI3NTI0IDUuODA0NDA4NjYxNzEzNTYxM2UtMDE3IC0wLjk0
        NzkzMTg3MTU4MjA0NTczIAktMC43MjU0MTI5MTE0NzI5NDcyOSA0LjQ0MjUwMjA1OTAyODQwMjll
        LTAxNyAtMC43MjU1MTU2NDQ1MzA1NjExNyAJLTAuOTQ3OTYxMjIzODg0MjIwOTkgMi40MDQyNjQ3
        ODkyMzc2MjI3ZS0wMTcgLTAuMzkyNjQ2MjM3NDE0OTk0MzMgCS0xLjAyNjAxOTM4ODA1Nzg4OTgg
        LTIuOTUxMTk4ODMxMTMzMDcyNmUtMDMzIDQuODE5NjczNDQ5MDEwNDYxM2UtMDE3IAktMC45NDc5
        NjEyMjM4ODQyMjA3NyAtMi40MDQyNjQ3ODkyMzc2MjNlLTAxNyAwLjM5MjY0NjIzNzQxNDk5NDM4
        IAktMC43MjU0MTI5MTE0NzI5NDc0IC00LjQ0MjUwMjA1OTAyODQwNTRlLTAxNyAwLjcyNTUxNTY0
        NDUzMDU2MTUgCS0wLjM5MzAyNzgxNzM0MzI3NTAyIC01LjgwNDQwODY2MTcxMzU2ZS0wMTcgMC45
        NDc5MzE4NzE1ODIwNDU2MiAJLTAuMTMwMDYwMjE0Njc3NDE4NzEgLTYuMTIzMjMzOTk1NzM2NzY2
        ZS0wMTcgMSAJMS4wNTMwMTExMzczNjQwNTgyZS0wMTYgLTYuMTIzMjMzOTk1NzM2NzY2ZS0wMTcg
        MSAJLTQuMTIyNzQxNTcwNTUzNjQxNmUtMDE1IDAuMTMwMDYwMjE0Njc3NDE4OCAxIAktMy43ODgy
        ODk2ODk1ODEzOTI1ZS0wMTUgMC4zOTMwMjc4MTczNDMyNzUyNCAwLjk0NzkzMTg3MTU4MjA0NTcz
        IAktMi43MTA4NzAwMzg5MjA3MTk4ZS0wMTUgMC43MjU0MTI5MTE0NzI5NDcyOSAwLjcyNTUxNTY0
        NDUzMDU2MTE3IAktMS4yMjA0NzgyMDg3MTE5MTA4ZS0wMTUgMC45NDc5NjEyMjM4ODQyMjA5OSAw
        LjM5MjY0NjIzNzQxNDk5NDMzIAk0LjU1NjQ0MTM5MzMzNDczMjdlLTAxNiAxLjAyNjAxOTM4ODA1
        Nzg4OTggLTQuODE5NjczNDQ5MDEwNDYxM2UtMDE3IAkyLjA2MjQzNjkxMDQ3ODM5NWUtMDE1IDAu
        OTQ3OTYxMjIzODg0MjIwNzcgLTAuMzkyNjQ2MjM3NDE0OTk0MzggCTMuMzU1MTY2MTMyMjYyODMw
        MWUtMDE1IDAuNzI1NDEyOTExNDcyOTQ3NCAtMC43MjU1MTU2NDQ1MzA1NjE1IAk0LjEzNzM2ODUx
        NTI4NzUzMThlLTAxNSAwLjM5MzAyNzgxNzM0MzI3NTAyIC0wLjk0NzkzMTg3MTU4MjA0NTYyIAk0
        LjIzODI1ODI0NjQ5MTY5MDllLTAxNSAwLjEzMDA2MDIxNDY3NzQxODcxIC0xIAk0LjE4MDQ5OTkw
        ODUyMjY2NjNlLTAxNSAtMS4wNTMwMTExMzczNjQwNzQyZS0wMTYgLTEgCTAuMTMwMDYwMjE0Njc3
        NDE4OCA0Ljc0NTIwNDg0MzIzOTY0MDNlLTAxNiAtMSAJMC4zOTMwMjc4MTczNDMyNzUyNCAxLjU2
        MDk0MjY1NDkwOTAyNDJlLTAxNSAtMC45NDc5MzE4NzE1ODIwNDU3MyAJMC43MjU0MTI5MTE0NzI5
        NDcyOSAyLjk0Mzc0NDg1OTQ1ODc1NzdlLTAxNSAtMC43MjU1MTU2NDQ1MzA1NjExNyAJMC45NDc5
        NjEyMjM4ODQyMjA5OSAzLjg4MDg2MzI3NzkxMTM2MzdlLTAxNSAtMC4zOTI2NDYyMzc0MTQ5OTQz
        MyAJMS4wMjYwMTkzODgwNTc4ODk4IDQuMjI2NDQ4Mzg5OTQ2MDc5MmUtMDE1IDQuODE5NjczNDQ5
        MDEwNDYxM2UtMDE3IAkwLjk0Nzk2MTIyMzg4NDIyMDc3IDMuOTI4OTQ4NTczNjk2MTE1ZS0wMTUg
        MC4zOTI2NDYyMzc0MTQ5OTQzOCAJMC43MjU0MTI5MTE0NzI5NDc0IDMuMDMyNTk0OTAwNjM5MzI2
        MmUtMDE1IDAuNzI1NTE1NjQ0NTMwNTYxNSAJMC4zOTMwMjc4MTczNDMyNzUwMiAxLjY3NzAzMDgy
        ODE0MzI5NDRlLTAxNSAwLjk0NzkzMTg3MTU4MjA0NTYyIAkwLjEzMDA2MDIxNDY3NzQxODcxIDUu
        OTY5ODUxNjQyMzg2OTg5OGUtMDE2IDEgCS0xLjA1MzAxMTEzNzM2NDA2MDdlLTAxNiA2LjEyMzIz
        Mzk5NTczNjcyMjllLTAxNyAxIAkzLjExNTIyMDYxODY1Mjg0MThlLTAxNSAtMC4xMzAwNjAyMTQ2
        Nzc0MTg4IDEgCTUuMzQ4Nzg1NzgwMjgzMDUxZS0wMTUgLTAuMzkzMDI3ODE3MzQzMjc1MjQgMC45
        NDc5MzE4NzE1ODIwNDU3MyAJNy44NjUwMTA2NzI0NDU2ODZlLTAxNSAtMC43MjU0MTI5MTE0NzI5
        NDcyOSAwLjcyNTUxNTY0NDUzMDU2MTE3IAk5LjE4OTE5NDc5MDYzODg2ODFlLTAxNSAtMC45NDc5
        NjEyMjM4ODQyMjA5OSAwLjM5MjY0NjIzNzQxNDk5NDMzIAk5LjExMjg4Mjc4NjY2OTQ2MWUtMDE1
        IC0xLjAyNjAxOTM4ODA1Nzg4OTggLTQuODE5NjczNDQ5MDEwNDYxM2UtMDE3IAk3LjY0OTk3OTI0
        NDY5MDgwOThlLTAxNSAtMC45NDc5NjEyMjM4ODQyMjA3NyAtMC4zOTI2NDYyMzc0MTQ5OTQzOCAJ
        NS4wMjA5MTExOTQzOTY0OTY1ZS0wMTUgLTAuNzI1NDEyOTExNDcyOTQ3NCAtMC43MjU1MTU2NDQ1
        MzA1NjE1IAkxLjYzMjc5MDczMzgzOTc0MTVlLTAxNSAtMC4zOTMwMjc4MTczNDMyNzUwMiAtMC45
        NDc5MzE4NzE1ODIwNDU2MiAJLTguMDQ4ODcwOTk4OTE4NjUzOWUtMDE2IC0wLjEzMDA2MDIxNDY3
        NzQxODcxIC0xIAktMS45NjAwNTM4NTkyNzIzNTQ0ZS0wMTUgMS4wNTMwMTExMzczNjM4ODMxZS0w
        MTYgLTE7'''
        
    #create
    nc = cmds.createNode('nurbsCurve', n=n, p=p, ss=True)
    cmds.setAttr('%s.overrideEnabled' % nc, True)
    cmds.setAttr('%s.overrideColor' % nc, 12)
    mel.eval('setAttr "%s.cc" -type "nurbsCurve" %s' % (nc, base64.decodestring(shape)))
    
    return nc

def update_envlight_loc(light):
    '''Given a env light shader, updates the area light with a spherical locator if needed'''
    areaLight = cmds.listConnections('%s.message' % light, s=False, d=True, type='areaLight')
    if areaLight:
        areaLight = areaLight[0]
        lightType = cmds.getAttr('%s.type' % light)

        cur_loc = cmds.listRelatives(areaLight, s=True, type='nurbsCurve', f=True)

        if lightType == 0: #omni
            if not cur_loc:
                create_envlight_loc(n='%s_envLoc' % areaLight, p=areaLight)

        elif lightType == 1: #directional
            if cur_loc:
                cmds.delete(cur_loc)
                
                
def update_envlight_falloff_loc(light):
    '''Given and env light shader, creates and deletes falloff spheres around the light when needed'''
    areaLight = cmds.listConnections('%s.message' % light, s=False, d=True, type='areaLight')
    if areaLight:
        areaLight = areaLight[0]
        has_falloff = cmds.getAttr('%s.falloff' % light)

        #delete existing locators
        for t in cmds.listRelatives(areaLight, c=True, f=True):
            if cmds.listRelatives(t, s=True, type='sphericalLightLocator'):
                cmds.delete(t)

        if has_falloff:
            #Falloff stop locator
            fo_stop_trans = cmds.createNode('transform', ss=True, p=areaLight)
            fo_stop_loc = cmds.createNode('sphericalLightLocator', ss=True, p=fo_stop_trans)
            fo_stop_trans = cmds.rename(fo_stop_trans, '%s_falloffStop' % areaLight)
                
            cmds.setAttr('%s.translate' % fo_stop_trans, 0, 0, 0)
            cmds.setAttr('%s.rotate' % fo_stop_trans, 0, 0, 0)
            cmds.setAttr('%s.scale' % fo_stop_trans, 1, 1, 1)
            cmds.setAttr('%s.template' % fo_stop_trans, 1)

            cmds.connectAttr('%s.falloff_stop' % light, '%s.sx' % fo_stop_trans)
            cmds.connectAttr('%s.falloff_stop' % light, '%s.sy' % fo_stop_trans)
            cmds.connectAttr('%s.falloff_stop' % light, '%s.sz' % fo_stop_trans)
            cmds.connectAttr('%s.falloff_loc_vis' % light, '%s.v' % fo_stop_trans)

            #Falloff start locator
            fo_start_trans = cmds.createNode('transform', ss=True, p=areaLight)
            fo_start_loc = cmds.createNode('sphericalLightLocator', ss=True, p=fo_start_trans)
            fo_start_trans = cmds.rename(fo_start_trans, '%s_falloffStart' % areaLight)
                
            cmds.setAttr('%s.translate' % fo_start_trans, 0, 0, 0)
            cmds.setAttr('%s.rotate' % fo_start_trans, 0, 0, 0)
            cmds.setAttr('%s.scale' % fo_start_trans, 1, 1, 1)
            cmds.setAttr('%s.template' % fo_start_trans, 1)

            cmds.connectAttr('%s.falloff_start' % light, '%s.sx' % fo_start_trans)
            cmds.connectAttr('%s.falloff_start' % light, '%s.sy' % fo_start_trans)
            cmds.connectAttr('%s.falloff_start' % light, '%s.sz' % fo_start_trans)
            cmds.connectAttr('%s.falloff_loc_vis' % light, '%s.v' % fo_start_trans)
            
