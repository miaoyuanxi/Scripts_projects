import os,sys
def delfiles(pathin=""):
	if os.path.exists(pathin):
		for parent,dirnames,filenames in os.walk(pathin):
			#print(parent)
			for filename in filenames:
				delname = os.path.join(parent,filename)
				os.remove(delname)
			getf = os.listdir(parent)
			if len(getf)==0:
				 os.rmdir(parent)
def main(pathin=""):
	files_arr=[]
	if os.path.exists(pathin):
		files_arr=os.listdir(pathin)
	trytimes=0
	tun=True
	while tun==True:
		if trytimes<10:
			if len(files_arr)>0:
				try:
					delfiles(pathin)
				except:
					info=sys.exc_info() 
					print (info[0],":",info[1])
				trytimes+=1
			elif len(files_arr)==0:
				os.makedirs(pathin)
				tun=False
				print("rebult the houdini folder")
		else:
			print("something was wrong,can't delt some files in this folder")
			print("--------------------------\n")
			print(files_arr)
			tun=False

if __name__=="__main__":
	path=r"D:\plugins\houdini"
	main(path)