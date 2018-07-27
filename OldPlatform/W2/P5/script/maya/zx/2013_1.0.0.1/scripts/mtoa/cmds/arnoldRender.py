import maya.cmds as cmds
import maya.mel as mel
import mtoa.core as core

def arnoldRender(width, height, doShadows, doGlowPass, camera, options):
    # Make sure the aiOptions node exists
    core.createOptions()
    cmds.arnoldRender(cam=camera, w=width, h=height) 
    
def arnoldBatchRenderOptionsString():
    try:
        port = core.MTOA_GLOBALS['COMMAND_PORT']
        return ' -r arnold -ai:port %i ' % port
    except:
        return ' -r arnold '

def arnoldBatchRender(option):
    # Make sure the aiOptions node exists
    core.createOptions()
    # Parse option string
    kwargs = {}
    options = option.split(" ")
    i, n = 0, len(options)
    if cmds.objExists('defaultResolution.mtoaCommandPort'):
        kwargs['port'] = cmds.getAttr('defaultResolution.mtoaCommandPort')
    while i < n:
        if options[i] in ["-w", "-width"]:
            i += 1
            if i >= n:
                break
            kwargs["width"] = int(options[i])

        elif options[i] in ["-h", "-height"]:
            i += 1
            if i >= n:
                break
            kwargs["height"] = int(options[i])

        elif options[i] in ["-cam", "-camera"]:
            i += 1
            if i >= n:
                break
            kwargs["camera"] = options[i]
        i += 1
    try:
        cmds.arnoldRender(batch=True, **kwargs)
    except RuntimeError, err:
        print err
        
def arnoldBatchStop():
    import pymel.core as pm
    pm.mel.eval('batchRender')

def arnoldIprStart(editor, resolutionX, resolutionY, camera):
    # Make sure the aiOptions node exists
    core.createOptions()
    cmds.arnoldIpr(cam=camera, w=resolutionX, h=resolutionY, mode='start')

def arnoldIprStop():
    cmds.arnoldIpr(mode='stop')

def arnoldIprIsRunning():
    return cmds.arnoldIpr()

def arnoldIprRender(width, height, doShadows, doGlowPass, camera):
    cmds.arnoldIpr(cam=camera, w=width, h=height, mode=render)

def arnoldIprRefresh():
    cmds.arnoldIpr(mode='refresh')

def arnoldIprPause(editor, pause):
    if pause:
        cmds.arnoldIpr(mode='pause')
    else:
        cmds.arnoldIpr(mode='unpause')

def arnoldIprChangeRegion(renderPanel):
    cmds.arnoldIpr(mode='region')
