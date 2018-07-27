userId = Wscript.Arguments(0)
taskId=Wscript.Arguments(1)
enfJobname=Wscript.Arguments(2)
outSmallPath = Wscript.Arguments(3)

frame = enfJobname

enfwork = "c:\enfwork"
smallPath = enfwork&"\"&taskId&"\RB_small"
outfolder = enfwork&"/"&taskId&"/output"
consumeTxt =enfwork&"/"&userId&"-"&taskId&"-"&enfJobname&".txt"

'taskId="11233"
'frame="frame0280"	
'consumeTxt = "c:/enfwork/11233/53-11233-test.txt"
'outSmallPath = "\\127.0.0.1\d\outputData\small\53\11233"

set p=createobject("wscript.shell")
Set fso = CreateObject("Scripting.FileSystemObject") 
wscript.echo "smallPath________________"&smallPath
'p.exec "cmd.exe /c mkdir "&smallPath&""	

if fso.FolderExists(smallPath) then
else
	fso.CreateFolder(smallPath)
end if
function convertFile(bigFile)
	
	
	bigName = bigFile.name
	bigPath = bigFile.path
	wscript.echo bigName+"......." + bigPath	
	replaceStr = "C:\enfwork\"&taskId&"\output\"
	
	
	
	finalSmallName = replace(bigPath,replaceStr,"")
	finalSmallName = replace(finalSmallName,"\","[_]")'\转成[_]
	finalSmallName = replace(finalSmallName,".","[-]")'.转成[-]
	finalSmallName = finalSmallName&".jpg"
	wscript.echo "after replace____________" + finalSmallName
	

	smallPath2 = smallPath&"\"&frame&"_"&finalSmallName
	smallPath3 = smallPath&"\*"
	p.run "c:\ImageMagick\nconvert.exe  -out jpeg -ratio -resize 200 0 -overwrite -o """&smallPath2&""" """&bigPath&"""",0,true'转换缩略图到本地RB_outsmall		
	'p.run "c:\\fcopy\\FastCopy.exe /cmd=move /speed=full /force_close  /no_confirm_stop /force_start  """&smallPath3&""" /to="""&outSmallPath&"""" ,0,true'拷贝缩略图到远程路径output/small	
	wscript.echo "move /Y """&smallPath3&""" """&outSmallPath&""""

	p.run "cmd.exe /c move /Y "&smallPath3&" "&outSmallPath&"" ,0,true'拷贝缩略图到远程路径output/small	
	
	
	'记录缩略图名和大图路径到文本
	if (fso.fileexists(consumeTxt)) then
		set f =fso.opentextfile(consumeTxt,8)
		f.writeline "small="&finalSmallName
		f.close	
	end if 


end function




function handFile(folderPath)
						wscript.echo "[folder]:"&folderPath
						set objSubFolder =fso.GetFolder(folderPath)
						set objFiles=objSubFolder.Files
						
            for each objFile in objFiles
								wscript.echo "subFile__________________"+ objFile.Path
								convertFile objFile
            next
            
            set objFiles = nothing
            set objSubFolder=nothing
            
end function



'vbs递归遍历当前目录下的所有文件夹和子文件夹   
Function loopFolders(outpath)  
    Set hfolder = fso.GetFolder(outpath)     
    folderPath = hfolder.path
    handFile folderPath 
    
    Set subFolderSet = hfolder.SubFolders  
    For Each subFolder in subFolderSet  
    		  
        loopFolders = subFolder.Path & ";" & loopFolders(subFolder.Path) &  loopFolders   
    Next  
    
    set subFolderSet = nothing
    set hfolder = nothing

End Function  
  
 

loopFolders outfolder
set p=nothing
set fso = nothing


 




'big=Wscript.Arguments(0)
'outpath=Wscript.Arguments(1)
'taskId="11233"
'frame="frame0001"
'busLoop  "11233","c:/enfwork/11233/output","\\127.0.0.1\d\outputData\small\53\11233","c:/enfwork/11233/53-11233-test.txt",frame
