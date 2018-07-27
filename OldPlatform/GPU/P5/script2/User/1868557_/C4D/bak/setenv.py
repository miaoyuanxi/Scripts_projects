import os,sys

def SETENV():
    #_REDSHIFT_LOCALDATAPATH='D:/WORK/REDSHIFT/CACHE/G1'

    os.environ["C4D_PLUGINS_DIR"] = r'B:/plugins/C4D/redshift/redshift_2527/CINEMA 4D R18/plugins'
    dir_app=r'B:/plugins/C4D/redshift/redshift_2527/Redshift/'
    os.environ['PATH']= "$PATH;"+dir_app+"/bin"
    os.environ['REDSHIFT_COREDATAPATH']= dir_app
    os.environ['REDSHIFT_LOCALDATAPATH']= dir_app
    os.environ['REDSHIFT_PREFSPATH']= dir_app
    os.environ['REDSHIFT_LICENSEPATH']= "5059@127.0.0.1"
    #os.environ['LOCALAPPDATA'] = _REDSHIFT_LOCALDATAPATH
    print("Env done!")
    return 0
    
if __name__=='__main__':
    SETENV()
    cmds = r'"C:/Program Files/MAXON/CINEMA 4D R18/CINEMA 4D 64 Bit.exe" '

    print (cmds)
    os.system(cmds)
    #os.system("D:/plugins/houdini/155632/bin/houdinifx.exe")