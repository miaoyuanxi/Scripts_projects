# ! /usr/bin/env python
#coding=utf-8
import argparse
import copy
import os
import subprocess
import _subprocess
import pprint
import sys
import shutil
import filecmp
import time
import RayvisionPluginsLoader
import re


def get_platfom(platform):
    info = {"platform": platform,
            "7z.exe": None,
            "plugin_path": None,
            "cfg_path": None,
            "home_path": None,
            "auto_plugins": None,
            "custom_config": None,
            }

    if info["platform"] == 1002:
        info["7z.exe"] = r"\\20.0.100.1\o5\py\model\7z\7z.exe"
        info["plugin_path"] = r"\\20.0.100.1\d\plugins"
        info["auto_plugins"] = r"\\20.0.100.1\td"
        info["cfg_path"] = r"\\20.0.100.1\d\ninputdata"
        info["home_path"] = r"\\20.0.100.1\d\inputdata"
        info["custom_config"] = r"\\20.0.100.1\td\custom_config"
    elif info["platform"] == 1005:
        info["7z.exe"] = r"\\10.50.5.29\o5\py\model\7z\7z.exe"
        info["plugin_path"] = r"\\10.50.24.10\d\plugins"
        info["auto_plugins"] = r"\\10.50.1.22\td"
        info["cfg_path"] = r"\\10.50.8.15\d\ninputdata5"
        info["home_path"] = r"\\10.50.24.11\d\inputdata5"
        info["custom_config"] = r"\\10.50.1.22\td\custom_config"
    elif info["platform"] == 1007:
        ''
    elif info["platform"] == 1099:
        ''

    for i in info:
        if type(info[i]) == type(""):
            info[i] = info[i].replace("\\", "/")

    info["auto_plugins"] = info["auto_plugins"].replace("/", "\\")

    return info


def get_json(**kwargs):
    options = {"common": {},
               "renderSettings": {},
               "mappings": {},
               "mount": {},
               "variables": {},
               "platform": {},
               "server":{}}

    options["common"]["debug"] = kwargs["debug"]
    options["common"]["tmp"] = "%s/%s" % (os.environ["tmp"], kwargs["task_id"])
    if not os.path.exists(options["common"]["tmp"]):
        os.makedirs(options["common"]["tmp"])

    if kwargs["json"]:
        if os.path.exists(kwargs["json"]):
            options_json = eval(open(kwargs["json"]).read())
            for i in options_json:
                options[i] = options_json[i]

            options["renderSettings"]["start"] = kwargs["start"]
            options["renderSettings"]["end"] = kwargs["end"]
            options["renderSettings"]["by"] = kwargs["by"]

            options["common"]["debug"] = kwargs["debug"]
            options["common"]["tmp"] = "%s/%s" % (os.environ["tmp"],
                options["common"]["taskId"])
            if not os.path.exists(options["common"]["tmp"]):
                os.makedirs(options["common"]["tmp"])

            options["common"]["plugin_file"] = kwargs["plugin_file"]

            options["platform"] = get_platfom(kwargs["platform"])
            return options
        else:
            raise Exception("Can not find the json file: %s." % kwargs["json"])

    if kwargs["task_id"]:
        options["platform"] = get_platfom(kwargs["platform"])
        options["renderSettings"]["start"] = kwargs["start"]
        options["renderSettings"]["end"] = kwargs["end"]
        options["renderSettings"]["by"] = kwargs["by"]

        cfg_path = "%s/%s/%s" % (options["platform"]["cfg_path"],
            kwargs["task_id"], "temp")

        options["platform"]["cfg_path"] = cfg_path

        cfg_file = "%s/%s" % (cfg_path, "render.cfg")

        server_info = eval(open(os.path.join(cfg_path, "server.cfg")).read())

        result = {}
        with open(os.path.join(cfg_path, "render.cfg"), "r") as f:
            while 1:
                line = f.readline()
                if "=" in line:
                    line_split = line.split("=")
                    result[line_split[0].strip()] = line_split[1].strip()
                if ">>" in line:
                    break
            cfg_info = result

        options["common"]["submitFrom"] = "client"
        options["common"]["cgv"] = int(server_info["maya_version"])
        options["common"]["cgFile"] = server_info["maya_file"]
        options["common"]["cgSoftName"] = cfg_info["cgSoftName"]
        options["common"]["userId"] = int(server_info["user_id"])
        options["common"]["taskId"] = int(server_info["task_id"])
        options["common"]["projectId"] = int(cfg_info["projectId"])
        options["common"]["projectSymbol"] = cfg_info["projectSymbol"]

        options["renderSettings"]["renderType"] = "render.exe"
        options["renderSettings"]["renderableCamera"] = cfg_info["renderableCamera"]
        options["renderSettings"]["projectPath"] = server_info["project"]

        options["server"] = server_info
        for i in options["server"]["variables"]:
            options["variables"][i] = options["server"]["variables"][i]

        cfg_info["mountFrom"] = eval(cfg_info["mountFrom"])

        if kwargs["storage_path"]:
            kwargs["storage_path"] = kwargs["storage_path"].replace("\\", "/")
            options["platform"]["home_path"] = re.findall(r'(.+?)/\d+/',
                kwargs["storage_path"], re.I)[0]

        # if options["platform"]["platform"] == 1005:
        #     if options["common"]["userId"] in [100001]:
        #         # options["mount"]["vcfs"] = server_info["spare_drives"][0]
        #         # options["platform"]["home_path"] = "%s/vcfs/cache/d/inputdata5" % (options["mount"]["vcfs"])
        #         options["platform"]["home_path"] = r"\\www.vcfs.com\share\d\inputdata5"
        #         # options["platform"]["home_path"] = r"\\10.50.100.7\share\d\inputdata5"
        #     # else:
        #     #     options["platform"]["home_path"] = r"\\10.50.24.11\d\inputdata5"

        sys.stdout.flush()
        print "storage path is: " + options["platform"]["home_path"]
        sys.stdout.flush()

        for i in cfg_info["mountFrom"]:
            options["mount"][cfg_info["mountFrom"][i]] = options["platform"]["home_path"] + i

        options["mappings"] = server_info["mappings"]

        options["common"]["plugin_file"] = os.path.join(cfg_path,
            "plugins.cfg")

        if options["common"]["userId"] in [100001, 963493, 963494,
            963495, 962413, 963496, 120151, 963433]:
            options["common"]["plugin_file"] = None

        return options


class RvOs(object):
    is_win = 0
    is_linux = 0
    is_mac = 0

    if sys.platform.startswith("win"):
        os_type = "win"
        is_win = 1
        #add search path for wmic.exe
        os.environ["path"] += ";C:/WINDOWS/system32/wbem"
    elif sys.platform.startswith("linux"):
        os_type = "linux"
        is_linux = 1
    else:
        os_type = "mac"
        is_mac = 1

    @staticmethod
    def get_windows_mapping():
        if RvOs.is_win:
            networks = {}
            locals = []
            for i in RvOs.run_command('wmic logicaldisk get deviceid,drivetype,providername'):
                if i.strip():
                    info = i.split()
                    if info[1] == "4":
                        networks[info[0]] = info[2].replace("\\", "/")
                    elif info[1] == "3":
                        locals.append(info[0])

        return (locals, networks)

    @staticmethod
    def get_virtual_drive():
        if RvOs.is_win:
            return dict([i.strip().split("\\: =>")
                for i in RvOs.run_command('subst') if i.strip()])

    @staticmethod
    def run_command(cmd):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = _subprocess.SW_HIDE

        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT, startupinfo=startupinfo)

        while 1:
            #returns None while subprocess is running
            return_code = p.poll()
            if return_code == 0:
                break
            # elif return_code == 1:
            #     raise Exception(cmd + " was terminated for some reason.")
            elif return_code != None:
                print "exit return code is: " + str(return_code)
                break
                # raise Exception(cmd + " was crashed for some reason.")
            line = p.stdout.readline()
            yield line

    @staticmethod
    def get_process_list(name):
        process_list = []
        for i in RvOs.run_command("wmic process where Caption=\"%s\" get processid" % (name)):
            if i.strip() and i.strip().isdigit():
                process_list.append(int(i.strip()))

        return process_list

    @staticmethod
    def get_all_child():
        parent_id = str(os.getpid())
        child = {}
        for i in RvOs.run_command('wmic process get Caption,ParentProcessId,ProcessId'):
            if i.strip():
                info = i.split()
                if info[1] == parent_id:
                    if info[0] != "WMIC.exe":
                        child[info[0]] = int(info[2])

        return child

    @staticmethod
    def kill_children():
        for i in RvOs.get_all_child().values():
            #os.kill is Available from python2.7, need another method.
#            os.kill(i, 9)
            if RvOs.is_win:
                os.system("taskkill /f /t /pid %s" % (i))

    @staticmethod
    def timeout_command(command, timeout):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = _subprocess.SW_HIDE

        start = time.time()
        process = subprocess.Popen(command, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        while process.poll() is None:
#            print "return: " + str(process.poll())
            time.sleep(0.1)
            now = time.time()
            if (now - start) > timeout:
#                os.kill(process.pid, 9)
                if RvOs.is_win:
                    os.system("taskkill /f /t /pid %s" % (process.pid))

                return None
        return process.poll()

    @staticmethod
    def call_command(cmd, shell=0):
        return subprocess.call(cmd, shell=shell)


class Zip7(object):

    def __init__(self, exe):
        self.exe = exe

    def compress(self, src):
        zip_file = os.path.splitext(src)[0] + ".7z"

        if self.is_same(zip_file, src):
            print_info("compressed file %s exists, skip compress" % (zip_file))
            result = 1
        else:
            print_info("compressing %s to %s" % (src, zip_file))

            cmd = "\"%s\" a \"%s\" \"%s\" -mx3 -ssw" % (self.exe,
                zip_file, src)

            result = 0
            for line in RvOs.run_command(cmd):
                if line.strip() == "Everything is Ok":
                    result = 1

        if result:
            return zip_file
        else:
            return src

    def decompress(self, zip_file, mark_path):
        zip_info = self.get_zip_info(zip_file)

        out = os.path.dirname(zip_file)
        src = os.path.join(out, zip_info["Path"])

        decompress_ok = "%s/%s" % (mark_path, "decompress_ok")
        start_decompress = "%s/%s" % (mark_path, "start_decompress")

        if os.path.exists(start_decompress):
            while 1:
                if os.path.exists(decompress_ok):
                    print "%s is already exists, skip decopress" % (src)
                    return src

                print "Waiting for decompress..."
                time.sleep(1)
        else:
            with open(start_decompress, "w") as f:
                ''

            try:
                print "decopress %s from %s" % (src, zip_file)
                cmd = "\"%s\" e \"%s\" -o\"%s\" -y" % (self.exe, zip_file, out)
                print cmd
                result = 0
                for line in RvOs.run_command(cmd):
                    if line.strip() == "Everything is Ok":
                        result = 1

                if result:
                    with open(decompress_ok, "w") as f:
                        ''
                    return src
                else:
                    os.remove(start_decompress)

            except:
                print "Catch except when decompress, delete %s" % (start_decompress)
                os.remove(start_decompress)

    def try_decompress(self, zip_file, retry=3):
        if retry == 0:
            return None
        else:
            try:
                print "try decompress %s time" % (4-retry)
                return self.decompress(zip_file)
            except:
                return self.try_decompress(zip_file, retry-1)

    def get_zip_info(self, zip_file):
        {'Attributes': 'A',
         'Block': '0',
         'Blocks': '1',
         'CRC': '836CB95D',
         'Encrypted': '-',
         'Headers Size': '138',
         'Method': 'LZMA2:20',
         'Modified': '2015-03-28 15:59:26',
         'Packed Size': '29191866',
         'Path': 'M02_P04_S046.mb',
         'Physical Size': '29192004',
         'Size': '138382876',
         'Solid': '-',
         'Type': '7z'}

        cmd = "\"%s\" l -slt \"%s\"" % (self.exe, zip_file)
        print cmd
        result = {}
        for line in RvOs.run_command(cmd):
            if "=" in line:
                line_split = [i.strip() for i in line.strip().split("=")]
                result[line_split[0]] = line_split[1]

        return result


    def is_same(self, zip_file, src):
        if os.path.exists(zip_file) and os.path.exists(src):
            zip_info = self.get_zip_info(zip_file)

            z_time = zip_info["Modified"]
            z_size = zip_info["Size"]

            f_time = time.strftime("%Y-%m-%d %H:%M:%S",
                                   time.localtime(os.path.getmtime(src)))
            f_size = str(os.path.getsize(src))

            if z_time == f_time and z_size == f_size:
                return 1


class Render(dict, Zip7):

    def __init__(self, options):
        for i in options:
            self[i] = options[i]

        self.check_mapping()
        self.check_7z()
        # self.check_sweeper()

    def check_sweeper(self):
        processes = RvOs.get_process_list("sweeper.exe")
        if processes:
            print "sweeper is running."
            sys.stdout.flush()
            print processes
            sys.stdout.flush()
        else:
            print "start sweeper."
            cmd = "start %s" % (r"C:\sweeper\sweeper.exe")
            print "cmd: " + cmd
            RvOs.call_command(cmd, shell=1)
            processes = RvOs.get_process_list("sweeper.exe")
            sys.stdout.flush()
            print processes
            sys.stdout.flush()

    def check_mapping(self):
        if self["common"]["submitFrom"] == "client":
            self.clean_network()
            self.mapping_network()
            self.mapping_plugins()

    def check_7z(self):
        if self["common"]["cgFile"].endswith(".rayvision"):
            print "Found 7z file: %s" % (self["common"]["cgFile"])
            Zip7.__init__(self, self["platform"]["7z.exe"])

            result = self.decompress(self["common"]["cgFile"],
                self["platform"]["cfg_path"])
            if result:
                self["common"]["cgFile"] = result
            else:
                raise Exception("decompress error %s" % \
                (self["common"]["cgFile"]))

    def run_command(self, command):
        #weird bug, don't know why
#        return subprocess.call(command, shell=1)
        return subprocess.call(command)

    def clean_network(self):
        if self.run_command("net use * /delete /y"):
            print "clean mapping network failed."
        else:
            print "clean mapping network successfully."
        sys.stdout.flush()

        self.clean_virtual_drive()
        sys.stdout.flush()

        # if self["platform"]["platform"] == 1005:
        #     self.clean_vcfs()

    def clean_vcfs(self):
        print "clean vcfs"
        cmd = r"c:\vcfsclient\vcfstask stop"
        print cmd
        sys.stdout.flush()
        self.run_command(cmd)
        sys.stdout.flush()

    def clean_virtual_drive(self, max=60):
        virtual_drive = RvOs.get_virtual_drive()
        if max == 0:
            print "clean virtual_drive failed"
            pprint.pprint(virtual_drive)
            sys.stdout.flush()
            return 0
        else:
            for i in virtual_drive:
                if self.run_command("subst %s /d" % (i)):
                    print "clean virtual drive failed: %s => %s" % (i,
                        virtual_drive[i])
                    sys.stdout.flush()
                else:
                    print "clean virtual drive successfully: %s => %s" % (i,
                        virtual_drive[i])
                    sys.stdout.flush()

            virtual_drive = RvOs.get_virtual_drive()
            if virtual_drive:
                time.sleep(1)
                print "wait 1 second and try remove subst again"
                sys.stdout.flush()
                self.clean_virtual_drive(max - 1)
            else:
                print "clean virtual_drive success"
                sys.stdout.flush()

    def create_virtua_drive(self, virtual_drive, path, max=60):
        if max == 0:
            print "can not create virutal drive: %s => %s" % (virtual_drive,
                path)
            sys.stdout.flush()
            return 0
        else:
            self.run_command("subst %s %s" % (virtual_drive, path))
            sys.stdout.flush()
            if os.path.exists(virtual_drive + "/"):
                print "create virutal drive: %s => %s" % (virtual_drive,
                    path)
                print virtual_drive + "/" + " is exists"
                sys.stdout.flush()
            else:
                time.sleep(1)
                print "wait 1 second and try subst again"
                sys.stdout.flush()
                self.create_virtua_drive(virtual_drive, path, max-1)

    def mapping_network(self):
        for i in self["mount"]:
            if i == "vcfs":
                cmd = r"c:\vcfsclient\vcfstask start /path=c:\vcfsclient " \
                    "/conf=vcfs.conf /log=opt_result.log " \
                    "/letter=%s" % (self["mount"][i].strip(":").lower())
                print cmd

                sys.stdout.flush()
                if self.run_command(cmd):
                    sys.stdout.flush()
                    print "can not start vcfs %s" % (self["mount"][i])
                    sys.stdout.flush()
                # else:
                #     mark = 120
                #     while 1:
                #         if os.path.exists(self["mount"][i]):
                #             print self["mount"][i] + " is exist"
                #             print "start vcfs %s" % (self["mount"][i])
                #             sys.stdout.flush()
                #             break
                #         else:
                #             if mark == 0:
                #                 break
                #             else:
                #                 print self["mount"][i] + " is not exist"
                #                 mark -= 1
                #                 time.sleep(1)
                #                 print "waiting 1 second for vcfs"
                #                 sys.stdout.flush()

            else:
                #on windows, we must use '\' slash when mount, not '/'
                path = self["mount"][i].replace("/", "\\")
                if path.startswith("\\"):
                    if self.run_command("net use %s %s" % (i, path)):
                        print "can not mapping %s to %s" % (i, path)
                    else:
                        print "Mapping %s to %s" % (i, path)
                else:
                    self.create_virtua_drive(i, path)

                sys.stdout.flush()

        self.run_command("net use")
        self.run_command("subst")

    def mapping_plugins(self):
        drive = "B:"
        auto_plugins = self["platform"]["auto_plugins"]
        if self.run_command("net use %s %s" % (drive, auto_plugins)):
            print "can not mapping %s to %s" % (drive, auto_plugins)
        else:
            print "Mapping %s to %s" % (drive, auto_plugins)

    def copytree(self, src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            if os.path.isdir(s):
                self.copytree(s, d)
            else:
                if os.path.exists(d):
                    if filecmp.cmp(s, d):
                        print "%s already exists, skip" % (d)
                    else:
                        print "copy %s to %s" % (s, d)
                        shutil.copy2(s, d)

                else:
                    print "copy %s to %s" % (s, d)
                    shutil.copy2(s, d)

    def copytree2(self, src, dst):
        if not os.path.exists(dst):
            os.makedirs(dst)

        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)

            if os.path.isdir(s):
                self.copytree2(s, d)
            else:
                print "copy %s to %s" % (s, d)
                shutil.copy2(s, d)

class MayaBatch(Render):

    def __init__(self, options):
        ''


class MayaGui(Render):

    def __init__(self, options):
        ''


class ArnoldKick(Render):

    def __init__(self, options):
        ''


class MayaClass(Render):

    def __init__(self, options):
        Render.__init__(self, options)
        self.get_maya_info()
        self.create_setup_file()
        self.set_variables()
        self.set_plugins()

    def get_maya_info(self):
        self["renderSettings"]["maya_file"] = self["common"]["cgFile"]

        self["renderSettings"]["render.exe"] = "C:/Program Files/Autodesk/" \
            "maya%s/bin/render.exe" % (self["common"]["cgv"])
        self["renderSettings"]["mayabatch.exe"] = "C:/Program Files/Autodesk/" \
            "maya%s/bin/mayabatch.exe" % (self["common"]["cgv"])
        self["renderSettings"]["output"] = "c:/work/render/%s/output/" % \
            (self["common"]["taskId"])
        if not os.path.exists(self["renderSettings"]["output"]):
            os.makedirs(self["renderSettings"]["output"])

    def create_setup_file(self):
        if self["mappings"]:
            self["renderSettings"]["setup_file"] = "%s/usersetup.mel" % \
                (self["common"]["tmp"])

            with open(self["renderSettings"]["setup_file"], "w") as f:
                f.write("dirmap -en true;\n")
                for i in self["mappings"]:
                    if not i.startswith("$"):
                        old_path = i
                        if isinstance(old_path, unicode):
                            old_path = i.encode("gb18030")
                        f.write("dirmap -m \"%s\" \"%s\";\n" % (old_path,
                                self["mappings"][i]))

    def set_variables(self):
        if self["common"]["userId"] in [963130]:
            os.environ["IDMT_PROJECTS"] = "Z:/Projects"
        else:
            for i in self["variables"]:
                os.environ[i] = self["variables"][i]

        if self["mappings"]:
            os.environ.setdefault("MAYA_SCRIPT_PATH", "")
            if os.environ["MAYA_SCRIPT_PATH"]:
                os.environ["MAYA_SCRIPT_PATH"] += ";"
            os.environ["MAYA_SCRIPT_PATH"] += self["common"]["tmp"]

        for i in self["mappings"]:
            if i.startswith("$"):
                try:
                    variable = re.findall(r'\$\{(.+)\}', i, re.I)[0]
                    os.environ[variable] = self["mappings"][i]
                except:
                    pass

    def set_plugins(self):
        if self["common"]["plugin_file"]:
            sys.stdout.flush()
            plginLd = RayvisionPluginsLoader.RayvisionPluginsLoader()
            sys.stdout.flush()
            if self["platform"]["custom_config"]:
                custom_file = self["platform"]["custom_config"] + "/" + \
                    str(self["common"]["userId"]) + "/RayvisionCustomConfig.py"
                sys.stdout.flush()
                print "custom_config is: " + custom_file
                sys.stdout.flush()
            plginLd.RayvisionPluginsLoader(self["common"]["plugin_file"], [custom_file])
            sys.stdout.flush()

class MayaRender(MayaClass):

    def __init__(self, options):
        MayaClass.__init__(self, options)

    def render(self):
        if self["common"]["debug"]:
            print "json info:"
            pprint.pprint(self)

        print "start maya render process..."

        cmd = "\"%(render.exe)s\" -s %(start)s -e %(end)s -b %(by)s " \
            "-proj \"%(projectPath)s\" -rd \"%(output)s\"" \
            % self["renderSettings"]

        if self["renderSettings"]["renderableCamera"]:
            if not "," in self["renderSettings"]["renderableCamera"] and \
                not "{rayvision}" in self["renderSettings"]["renderableCamera"]:
                cmd += " -cam \"%(renderableCamera)s\"" % self["renderSettings"]

        if not self["common"]["plugin_file"]:
            # if self["common"]["userId"] in [961872]:
            #     shutil.copy2(r"\\10.50.24.11\d\plugins\100001\Maya.env",
            #                  r"C:\users\enfuzion\Documents\maya\2015-x64\Maya.env")
            #     self.copytree2(r"\\10.50.24.11\d\plugins\100001\pixar\desc",
            #                    r"C:\Program Files\Autodesk\Maya2015\bin\rendererDesc")

            if self["common"]["userId"] in [100001]:
                shutil.copy2(r"\\10.50.24.11\d\plugins\100002\Maya.env",
                             r"C:\users\enfuzion\Documents\maya\2013-x64\Maya.env")
                self.copytree2(r"\\10.50.24.11\d\plugins\100002\3Delight",
                               r"C:\Program Files\3Delight")


            if self["common"]["userId"] in [963493,963494,963495,963496]:
                self.copytree2(r"\\10.50.8.16\td\zhaoxiaofei\mash\maya",
                               r"C:\users\enfuzion\Documents\maya")
                self.copytree2(r"\\10.50.8.16\td\zhaoxiaofei\mash\bin",
                               r"C:\Program Files\Autodesk\Maya2014\bin")

            if self["common"]["userId"] in [962413]:
                cmd += " -preRender \"python \\\"user_id=%s;execfile(\\\\\\\"//20.0.100.1/o5/py/model/prerender.py\\\\\\\")\\\"\"" % (self["common"]["userId"])

    #                    image_name = os.path.basename(self.cfg_info["maya_file"]).split("-")[0]
    #                    image_name = "<RenderPass>/" + image_name + "_<RenderPass>"
    #                    cmd += " -im \"%s\"" % image_name

                if self["common"]["cgv"] == 2013:
                    pre_bat = r"\\10.50.8.16\td\zhaoxiaofei\HQ_Animation\HQ_Setting.bat"
                    cmd = "\"%s\" && %s" % (pre_bat, cmd)

                if self["common"]["cgv"] == 2015:
                    pre_bat = r"\\10.50.8.16\td\zhaoxiaofei\HQ_Animation\2015_VFX\HQ_VFX_Setting.bat"
                    cmd = "\"%s\" && %s" % (pre_bat, cmd)

            if self["common"]["userId"] in [962276]:
                pre_bat = r"\\10.50.24.10\d\plugins\962000\962276\hqPlugins\hq.bat"
                cmd = "\"%s\" && %s" % (pre_bat, cmd)

            if self["common"]["userId"] in [120151]:
                pre_bat = r"\\10.50.8.16\td\zhaoxiaofei\ants_moon\moon.bat"
                cmd = "\"%s\" && %s" % (pre_bat, cmd)

            if self["common"]["userId"] in [962276]:
                pre_bat = r"\\10.50.8.16\td\zhaoxiaofei\vj\vj.bat"
                cmd = "\"%s\" && %s" % (pre_bat, cmd)

            if self["common"]["userId"] in [963433]:
                pre_bat = r"\\10.50.24.10\d\plugins\963433\fengbaocg.bat"
                cmd = "\"%s\" && %s" % (pre_bat, cmd)

        if self["common"]["userId"] in [963287, 963492, 963250, 964462,965366]:
            cmd += " -r arnold -ai:lve 1"
        # elif self["common"]["userId"] in [961872]:
        #     cmd += " -r rman"
        else:
            cmd += " -mr:art -mr:aml"

        if self["common"]["userId"] in [100001]:
            self["renderSettings"]["output"] += "<pass>/<scene>_<pass>" \
                                                "_<aov>_#.<ext>"
            cmd = "\"%(render.exe)s\" -r 3delight -rp all -an 1" \
                  " -s %(start)s -e %(end)s -inc %(by)s " \
                  " -proj \"%(projectPath)s\" -img \"%(output)s\"" \
                  % self["renderSettings"]

        cmd += " \"%(maya_file)s\"" % self["renderSettings"]

        print "render cmd info:"
        print cmd
        sys.stdout.flush()

        # subprocess.call(cmd)
        is_complete = 0
        re_complete = re.compile(r'^Scene.+completed\.$', re.I)
        for line in RvOs.run_command(cmd):
            line_str = line.strip()
            if line_str:
                print line_str

                if self["common"]["userId"] in [963287]:
                    if "Maya exited with status -1073741818" in line_str:
                        exit(-1073741818)
                    if "Maya exited with status -1073741819" in line_str:
                        exit(-1073741819)

                if re_complete.findall(line_str):
                    is_complete = 1

        if not is_complete:
            exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Liu Qiang || MMmaomao')
    parser.add_argument("--js", dest="json", type=str)
    parser.add_argument("--ti", dest="task_id", type=int)
    parser.add_argument("--pt", dest="platform", type=int)
    parser.add_argument("--sf", dest="start", type=int, required=1)
    parser.add_argument("--ef", dest="end", type=int, required=1)
    parser.add_argument("--by", dest="by", type=int, required=1)
    parser.add_argument("--lg", dest="log_object", type=str)
    parser.add_argument("--pl", dest="plugin_file", type=str)
    parser.add_argument("--sp", dest="storage_path", type=str)
    parser.add_argument("-d", dest="debug", default=False, action="store_true")

    kwargs = parser.parse_args().__dict__
    options = get_json(**kwargs)

    render = None
    if options["common"]["cgSoftName"] == "maya":
        if options["renderSettings"]["renderType"] == "render.exe":
            render = MayaRender(options)
        elif options["renderSettings"]["renderType"] == "mayabatch.exe":
            render = MayaBatch(options)
        elif options["renderSettings"]["renderType"] == "maya.exe":
            render = MayaGui(options)
    elif options["common"]["cgSoftName"] == "arnold":
        if options["renderSettings"]["renderType"] == "kick.exe":
            render = ArnoldKick(options)

    if render:
        render.render()
        if not options["common"]["debug"]:
            render.clean_network()
    else:
        raise Exception("Can not find the match render class.")
