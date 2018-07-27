import os,sys
import re

def Creat_adict(folder="",namein=""):
	# arg = D:/aa
	# D:/aa/aa.001.exr
	folder = folder
	file_adict = {}
	folder_arr = os.listdir(folder)
	if len(folder_arr)>0:		
		dif = True
		while dif:
			getval = getsque(folder_arr,namein)
			if not getval=="":
				file_adict[getval[0]] = getval[1]
				file_adict[getval[0]+"TLam"] = [getval[3],getval[4],getval[5],getval[6]]

				if len(getval[2])>0:
					folder_arr = getval[2]
				else:
					dif=False
			else:
				dif=False
		# print (file_adict)		
	else:
		print("This folder is empty")
	return file_adict

def Get_mis(arr=[],name="default",ext="exr",num_min=0,num_max=1,num_len=3):
	arr_not_exit = []

	if len(arr):
		# print("11111",arr[0])
		elm_n = re.findall("\d+",arr[0])
		if elm_n:
			if ("."+elm_n[-1]+".") in arr[0]:
				with_begain = True
			else:
				with_begain = False
		for i in range(num_min,num_max+1):
			if with_begain:
				num_str = "."+str(i).zfill(num_len)+"."
			else:
				num_str = str(i).zfill(num_len)+"."
			fullname = name+num_str+ext
			# print("6666",fullname)
			if fullname not in arr:
				# print("\tNot exit: %s" %fullname)
				arr_not_exit.append(fullname)
	return arr_not_exit

def getsque(arr_elm=[],namein=""):
	adict_out = {}
	folder_arr = arr_elm

	if len(folder_arr)>0:
		# namein: abc_123.txt  abc123.LLL.txt
		is_sequence=""

		if not namein=="":
			first_elm=""
			namein_num = re.findall("\d+",namein)
			# spli_str=""
			sequence_in = True
			if len(namein_num)>0:
				num_len = len(namein_num[-1])
				if ("."+namein_num[-1]+".") in namein:
					spli_str = "."+namein_num[-1]+"."
				elif (namein_num[-1]+".") in namein:
					spli_str = namein_num[-1]+"."
				else:
					sequence_in = False
					#print("Not an sequence yet: %s " %namein )
					return is_sequence
			else:
				sequence_in = False
				#print("Not an sequence yet: %s " %namein )
				return is_sequence	

			if sequence_in:
				namein_name = namein.split(spli_str)[0]
				namein=namein_name
				finded = False
				for elm in folder_arr:
					first_elm = elm
					num = re.findall("\d+",first_elm)
					if len(num)>0:
						num_len = len(num[-1])
						if ("."+num[-1]+".") in first_elm:
							spli_str = "."+num[-1]+"."
						else:
							spli_str = num[-1]+"."
						first_name = first_elm.split(spli_str)[0]

						if first_name==namein:
							first_elm==elm
							finded = True
							# print("Find files: %s " % first_elm)
							break
				if not finded:
					print("Cant find the file\" %s \" in this folder" % namein)
					return is_sequence

				else:
					num = re.findall("\d+",first_elm)
					if len(num)>0:
						# print (num[-1])
						num_len = len(num[-1])
						file_min = int(num[-1])
						file_max = int(num[-1])
						if ("."+num[-1]+".") in first_elm:
							spli_str = "."+num[-1]+"."
						else:
							spli_str = num[-1]+"."

						first_name = first_elm.split(spli_str)[0]
						first_end = first_elm.split(spli_str)[-1]

					f_arr = []
					f_dif_arr = []

					for elm in folder_arr:
						elm_n = re.findall("\d+",elm)
						if len(elm_n)>0:
							elm_n_len = len(elm_n[-1])
							elm_int = int(elm_n[-1])
							if ("."+elm_n[-1]+".") in elm:
								spli_str = "."+elm_n[-1]+"."
							else:
								spli_str = elm_n[-1]+"."
							elm_name = elm.split(spli_str)[0]
							elm_end = elm.split(spli_str)[-1]
							if first_name==namein:
								if elm_n_len==num_len and elm_name==first_name and elm_end==first_end:
									f_arr.append(elm)
									if elm_int < file_min:
										file_min = elm_int
									elif elm_int > file_max:
										file_max = elm_int
					return first_name,f_arr,f_dif_arr,file_min,file_max,num_len,first_end

		else:
			first_elm = folder_arr[0]
			num = re.findall("\d+",first_elm)
			if len(num)>0:
				# print (num[-1])
				num_len = len(num[-1])
				file_min = int(num[-1])
				file_max = int(num[-1])
				if ("."+num[-1]+".") in first_elm:
					spli_str = "."+num[-1]+"."
				else:
					spli_str = num[-1]+"."
				first_name = first_elm.split(spli_str)[0]
				first_end = first_elm.split(spli_str)[-1]
			# print(first_name,file_min,first_end,num_len)
			f_arr = []
			f_dif_arr = []
			for elm in folder_arr:
				elm_n = re.findall("\d+",elm)
				if len(elm_n)>0:
					elm_n_len = len(elm_n[-1])
					elm_int = int(elm_n[-1])
					if ("."+elm_n[-1]+".") in elm:
						spli_str = "."+elm_n[-1]+"."
					else:
						spli_str = elm_n[-1]+"."
					elm_name = elm.split(spli_str)[0]
					elm_end = elm.split(spli_str)[-1]			
					if elm_n_len==num_len and elm_name==first_name and elm_end==first_end:
						f_arr.append(elm)
						if elm_int < file_min:
							file_min = elm_int
						elif elm_int > file_max:
							file_max = elm_int
					else:
						f_dif_arr.append(elm)
			return first_name,f_arr,f_dif_arr,file_min,file_max,num_len,first_end

def WriteInfo(folder="",info=""):
	folder = os.path.join(folder,"Info")
	if not os.path.exists(folder):		
		os.makedirs(folder)
	file=os.path.join(folder,"infos.txt")
	print("\nYou can also get this information here: %s"%file)
	with open(file,"w") as f:
		f.write(info)
		f.close()


def main(folder="",namein="",logout=True,info_folder=""):
	notexit_adict = {}
	sequence_path = ""
	all_sque={}
	if os.path.exists(folder):
		all_sque = Creat_adict(folder,namein)

	if len(all_sque):		
		if namein=="":
			print("The amount of sequence in this folder: %d\n" % (len(all_sque)/2))
		# print(all_sque)

		for key in all_sque:
			file_name = key
			file_arr = []
			file_num_info=[]

			if "TLam" not in key:
				file_arr = all_sque[key]
				for key_n in all_sque:
					if key_n==key+"TLam":
						file_num_info = all_sque[key_n]
			if len(file_arr) and len(file_num_info):
				arr_n = Get_mis(file_arr,file_name,file_num_info[3],file_num_info[0],file_num_info[1],file_num_info[2])
				notexit_adict[file_name]=arr_n

			if not namein=="":
				file_name_base=""
				if "TLam" not in key:
					file_elm = all_sque[key][0]
					base_name_n = re.findall("\d+",file_elm)
					base_name_arr = file_elm.split(base_name_n[-1])
					file_name_base = base_name_arr[0]+("$F%d"%len(base_name_n[-1]))+base_name_arr[-1]	
					sequence_path = os.path.join(folder,file_name_base)
					# print (sequence_path)
					break
				

		if len(notexit_adict)>0:		
			
			for keys in notexit_adict:
				mis_name = notexit_adict[keys]
				if len(mis_name):
					print("--"*30)
					print("------infos")
					info= "The files following are not exit:\n"
					print ("The files following are not exit:\n")
					# print(mis_name)
					mis_name_n = re.findall("\d+",mis_name[0])
					mis_name_arr = mis_name[0].split(mis_name_n[-1])
					mis_name_finall = mis_name_arr[0]+("$F%d"%len(mis_name_n[-1]))+mis_name_arr[-1]

					print(">> \nMissing files of \" %s \"" % mis_name_finall)
					info += ("\n\n>> Files of \" %s \"" % mis_name_finall)
					for elm in notexit_adict[keys]:
						print("\t%s" % elm)
						info += ("\n\t%s" % elm)
					print("------infos")
					print("--"*30)
					print("\n")

			if logout:
				if not info_folder=="":
					WriteInfo(info_folder,info)
				else:
					WriteInfo(folder,info)

	return sequence_path

if __name__=="__main__":
	f= sys.argv[1]
	print("\nThe input path: %s"%f)
	print(main(f,"smoke_zhongxin_wuqi_a.1136.bgeo.sc",False))