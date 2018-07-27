#! /usr/bin/env python
#coding=utf-8
import os
import subprocess
import _subprocess
import pprint
import sys
import shutil
import filecmp
import time


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
            elif return_code == 1:
                raise Exception(cmd + " was terminated for some reason.")
            elif return_code != None:
                print "exit return code is: " + str(return_code)
                raise Exception(cmd + " was crashed for some reason.")
            line = p.stdout.readline()
            yield line

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
                os.system("taskkill /pid %s" % (i))

    @staticmethod
    def timeout_command(command, timeout):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= _subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = _subprocess.SW_HIDE

        start = time.time()
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.poll() is None:
#            print "return: " + str(process.poll())
            time.sleep(0.1)
            now = time.time()
            if (now - start) > timeout:
#                os.kill(process.pid, 9)
                if RvOs.is_win:
                    os.system("taskkill /pid %s" % (process.pid))

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

    def try_decompress(self, zip_file, retry=3, mark_path=None):
        if retry == 0:
            return None
        else:
            try:
                print "try decompress %s time" % (4-retry)
                return self.decompress(zip_file, mark_path)
            except:
                return self.try_decompress(zip_file, retry-1, mark_path)

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


class Render(Zip7):

    def __init__(self, task_id, user_id):
        self.task_id = task_id
        self.user_id = user_id
        self.cfg_path = self.get_cfg_path()
        self.cfg_info = self.get_cfg_info()
        self.plugin_info = self.get_plugin_info()
        Zip7.__init__(self, r"\\10.50.5.29\o5\py\model\7z\7z.exe")
        self.plugin_path = r"\\10.50.24.10\d\plugins"
        if self.cfg_info["father_id"]:
            self.cfg_info["user_id"] = self.cfg_info["father_id"]

    def pre_render(self):
        print "Start default pre render process..."
        self.clean_network()

        self.mapping_network()

    def post_render(self):
        print "Start default post render process..."
#        self.clean_network()

    def run_command(self, command):
        #weird bug, don't know why
#        return subprocess.call(command, shell=1)
        return subprocess.call(command)

    def clean_network(self):
        if self.run_command("net use * /delete /y"):
            print "clean mapping network failed."
        else:
            print "clean mapping network successfully."

        virtual_drive = RvOs.get_virtual_drive()
        for i in virtual_drive:
            if self.run_command("subst %s /d" % (i)):
                print "clean virtual drive failed: %s => %s" % (i, virtual_drive[i])
            else:
                print "clean virtual drive successfully: %s => %s" % (i, virtual_drive[i])

    def mapping_network(self):
        if not os.path.exists("O:/"):
            print "start mounting drive O:"
            self.run_command("net start vcfsservice")
#        mapping = {"x:": r"\\10.50.1.6\d\inputdata8\maya\21000\21293\X",
#                   "z:": r"\\192.168.0.88\3dsoft\temp"}

        if self.cfg_info["user_id"] in [961577, 961580, 961581, 962152]:
            self.cfg_info["mappings"]["z:"] = r'\\10.50.24.11\d\inputdata5\961500\961577\YishuZSLM\maya\Z'

        if self.cfg_info["user_id"] in [962134]:
            self.cfg_info["mappings"]["z:"] = r'\\10.50.24.10\d\inputdata5\962000\962134\YishuZSLM\maya\Z'

        if self.cfg_info:
            for i in self.cfg_info["mappings"]:
                if i.endswith(":"):
                    #on windows, we must use '\' slash when mount, not '/'
                    path = self.cfg_info["mappings"][i].replace("/", "\\")
                    if path.startswith("\\"):
                        if self.run_command("net use %s %s" % (i, path)):
                            print "can not mapping %s to %s" % (i, path)
                        else:
                            print "Mapping %s to %s" % (i, path)
                    else:
                        if self.run_command("subst %s %s" % (i, path)):
                            print "can not create virutal drive: %s => %s" % (i, path)
                        else:
                            print "create virutal drive: %s => %s" % (i, path)

                    sys.stdout.flush()

        self.run_command("net use")
        self.run_command("subst")

    def get_cfg_path(self):
        if self.user_id:
            cfg = r"\\10.50.8.15\d\ninputdata5\%s\%s\temp" % \
                (self.user_id, self.task_id)
        else:
            cfg = r"\\10.50.8.15\d\ninputdata5\%s\temp" % \
                (self.task_id)

        cfg = cfg.replace("\\", "/")

        if os.path.exists(cfg):
            return cfg

    def get_cfg_info(self):
        if self.cfg_path:
            cfg_file = os.path.join(self.cfg_path, "server.cfg")
            if os.path.exists(cfg_file):
                return eval(open(cfg_file).read())

    def get_extra_info(self):
        result = {}
        if self.cfg_path:
            file = os.path.join(self.cfg_path, "render.cfg")
            with open(file, "r") as f:
                while 1:
                    line = f.readline()
                    if "=" in line:
                        line_split = line.split("=")
                        result[line_split[0].strip()] = line_split[1].strip()
                    if ">>" in line:
                        break
                return result

    def get_plugin_info(self):
        if self.cfg_path:
            plugin_file = os.path.join(self.cfg_path, "plugins.cfg")
            if os.path.exists(plugin_file):
                return eval(open(plugin_file).read())

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

class MayaRender(Render):

    def __init__(self, task_id, user_id=None):
        Render.__init__(self, task_id, user_id)
        self.plugin_path = os.path.join(self.plugin_path, "maya")

        if self.cfg_info:
            self.extra_info = self.get_extra_info()

            self.cfg_info["maya_version"] = int(self.cfg_info["maya_version"])

            self.get_maya_info()
            self.create_setup_file()
            self.set_variables()
            self.set_plugins()


        else:
            print "The cfg file of task %s doesn't exists." % self.task_id

        print "\n"

    def get_maya_info(self):
        self.cfg_info["render_exe"] = "C:/Program Files/Autodesk/" \
            "maya%s/bin/render.exe" % (self.cfg_info["maya_version"])
        self.cfg_info["mayabatch_exe"] = "C:/Program Files/Autodesk/" \
            "maya%s/bin/mayabatch.exe" % (self.cfg_info["maya_version"])
        self.cfg_info["output"] = "c:/work/render/%s/output/" % (self.task_id)
        if not os.path.exists(self.cfg_info["output"]):
            os.makedirs(self.cfg_info["output"])

        if self.cfg_info["maya_file"].endswith(".7z") or self.cfg_info["maya_file"].endswith(".rayvision"):
            result = self.decompress(self.cfg_info["maya_file"],
                mark_path = self.cfg_path)
            if result:
                self.cfg_info["maya_file"] = result
            else:
                raise Exception("decompress error %s" % (self.cfg_info["maya_file"]))

    def create_setup_file(self):
        if self.cfg_info["mappings"]:
            self.cfg_info["tmp"] = os.path.join(os.environ["tmp"],
                str(self.task_id))
            if not os.path.exists(self.cfg_info["tmp"]):
                os.makedirs(self.cfg_info["tmp"])

            self.cfg_info["setup_file"] = os.path.join(self.cfg_info["tmp"],
                "usersetup.mel")

            with open(self.cfg_info["setup_file"], "w") as f:
                f.write("dirmap -en true;\n")
                for i in self.cfg_info["mappings"]:
                    old_path = i
                    if isinstance(old_path, unicode):
                        old_path = i.encode("gb2312")
                    f.write("dirmap -m \"%s\" \"%s\";\n" % (old_path,
                        self.cfg_info["mappings"][i]))

    def set_variables(self):
        for i in self.cfg_info["variables"]:
            os.environ[i] = self.cfg_info["variables"][i]

        if self.cfg_info["mappings"]:
            os.environ.setdefault("MAYA_SCRIPT_PATH", "")
            if os.environ["MAYA_SCRIPT_PATH"]:
                os.environ["MAYA_SCRIPT_PATH"] += ";"
            os.environ["MAYA_SCRIPT_PATH"] += self.cfg_info["tmp"]

    def set_plugins(self):
        pprint.pprint(self.plugin_info)

        if self.cfg_info["user_id"] in [120151, 100001, 962413]:
            return 0

        if self.cfg_info["user_id"] in [962539, 962796]:
            self.copytree2(r"\\10.50.8.16\td\lion\soft\maya\plugins\vray2.04.01 for maya 2014\Program Files",
                                     r"C:\Program Files")
            return 0

        if "mtoa" in self.plugin_info:
            print "set mtoa plugin"
#            modules_path = r'C:\users\enfuzion\Documents\maya\%s-x64\modules' % (self.cfg_info["maya_version"])
#            self.create_mtoa_module(modules_path)
#
#            env_path = r'C:\users\enfuzion\Documents\maya\%s-x64' % (self.cfg_info["maya_version"])
#            self.create_mtoa_env(env_path)

            self.copy_mtoa()

        if self.user_id in [100001, 300133, 961624]:
            self.copytree(r"\\10.50.8.16\td\zhaoxiaofei\300133\Autodesk",
                         r"C:\Program Files\Autodesk")

        if "vrayformaya" in self.plugin_info:
            self.plugin_path = os.path.join(self.plugin_path, "vray",
                str(self.cfg_info["maya_version"]), self.plugin_info["vrayformaya"])

            print "set vrayformay plugin"
            os.environ["RAYVISION_VRAY_FOR_MAYA"] = self.plugin_path

            os.environ["MAYA_RENDER_DESC_PATH"] = os.path.join(self.plugin_path,
                r"maya_root\bin\rendererDesc")

            os.environ["VRAY_FOR_MAYA%s_MAIN_x64" % \
                (self.cfg_info["maya_version"])] = os.path.join(self.plugin_path,
                r"maya_vray")

            os.environ["VRAY_FOR_MAYA%s_PLUGINS_x64" % \
                (self.cfg_info["maya_version"])] = os.path.join(self.plugin_path,
                r"maya_vray\vrayplugins")

            os.environ["PATH"] = "%PATH%;" + os.path.join(self.plugin_path,
                r"maya_root\bin")

            os.environ["MAYA_PLUG_IN_PATH"] = os.path.join(self.plugin_path,
                r"maya_vray\plug-ins")

            os.environ["MAYA_SCRIPT_PATH"] = os.path.join(self.plugin_path,
                r"maya_vray\scripts")

            os.environ["XBMLANGPATH"] = os.path.join(self.plugin_path,
                r"maya_vray\icons\%B")

    def copy_mtoa(self):
        modules_path = r'C:\users\enfuzion\Documents\maya\%s-x64\modules' % (self.cfg_info["maya_version"])
        env_path = r'C:\users\enfuzion\Documents\maya\%s-x64' % (self.cfg_info["maya_version"])

        plugin_path = r"\\10.50.8.16\td\arnold_gongxiang\PLUGINS\maya\arnold\replace\maya%s\%s" % (self.cfg_info["maya_version"], self.plugin_info["mtoa"])

        if not os.path.exists(modules_path):
            os.makedirs(modules_path)
            print "create %s" % (modules_path)

        if not os.path.exists(env_path):
            os.makedirs(env_path)
            print "create %s" % (env_path)

        src = r"\\10.50.8.16\td\arnold_gongxiang\solidangle\mtoadeploy\%s_%s" % (self.cfg_info["maya_version"], self.plugin_info["mtoa"])
        dst = r"C:\solidangle\mtoadeploy\%s_%s" % (self.cfg_info["maya_version"], self.plugin_info["mtoa"])
        if os.path.exists(dst):
            print "%s exists, skip" % (dst)
        else:
            shutil.copytree(src, dst)
            print "copy %s to %s" % (src, dst)

        src = os.path.join(plugin_path, "modules", "mtoa.mod")
        dst = os.path.join(modules_path, "mtoa.mod")
        shutil.copy2(src, dst)
        print "copy %s to %s" % (src, dst)

        if os.path.exists(dst):
            print "module file %s exists" % (dst)
        else:
            print "module file %s is not exists" % (dst)

        print "module file info:"
        print open(dst, "r").read()

        src = os.path.join(plugin_path, "Maya.env")
        dst = os.path.join(env_path, "Maya.env")
        shutil.copy2(src, dst)
        print "copy %s to %s" % (src, dst)

        if os.path.exists(dst):
            print "env file %s exists" % (dst)
        else:
            print "env file %s is not exists" % (dst)

        print "env file info:"
        print open(dst, "r").read()

    def create_mtoa_module(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print "makedir %s" % (path)

        print "module file path is %s" % (path)

        module_file = os.path.join(path, "mtoa.mod")
        if os.path.exists(module_file):
            os.remove(module_file)
            print "delete the old module file %s" % (module_file)

        print "create the module file %s" % (module_file)

        with open(module_file, "w") as f:
            f.write(r"+ mtoa any C:\solidangle\mtoadeploy\%s_%s" % (self.cfg_info["maya_version"],
                    self.plugin_info["mtoa"]))
            f.write("\r\n")
            f.write(r"PATH +:= bin")

        if os.path.exists(module_file):
            print "module file %s exists" % (module_file)
        else:
            print "module file %s is not exists" % (module_file)

        print "module file info:"
        print open(module_file, "r").read()

    def create_mtoa_env(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print "makedir %s" % (path)
        print "env file path is %s" % (path)

        env_file = os.path.join(path, "Maya.env")
        if os.path.exists(env_file):
            os.remove(env_file)
            print "delete the old module file %s" % (env_file)

        print "create the module file %s" % (env_file)

        with open(env_file, "w") as f:
            f.write(r"MAYA_RENDER_DESC_PATH = C:\solidangle\mtoadeploy\%s_%s" % (self.cfg_info["maya_version"],
                    self.plugin_info["mtoa"]))
            f.write("\r\n")
            f.write(r"PATH = %s;C:\solidangle\mtoadeploy\%s_%s\bin" % ("%PATH%",
                    self.cfg_info["maya_version"], self.plugin_info["mtoa"]))

        if os.path.exists(env_file):
            print "env file %s exists" % (env_file)
        else:
            print "env file %s is not exists" % (env_file)

        print "env file info:"
        print open(env_file, "r").read()

    def render(self, start, end, by=1):
        self.pre_render()

        if self.cfg_info:
            self.cfg_info["start"] = start
            self.cfg_info["end"] = end
            self.cfg_info["by"] = by

            pprint.pprint(self.cfg_info)
#            for i in os.environ:
#                print i, os.environ[i]

            print "start maya render process..."
            if self.cfg_info["user_id"] in [961743]:
                cmd = "\"%(render_exe)s\" -s %(start)s -e %(end)s -b %(by)s " \
                    "-preRender \"setAttr \\\"miDefaultOptions.maxSamples\\\" 2;" \
                    "setAttr \\\"miDefaultOptions.finalGather\\\" 1;" \
                    "setAttr \\\"miDefaultOptions.finalGatherRays\\\" 200;" \
                    "setAttr \\\"miDefaultOptions.finalGatherPresampleDensity\\\" 2;" \
                    "setAttr \\\"miDefaultOptions.finalGatherPoints\\\" 30;\" " \
                    "-proj \"%(project)s\" -rd \"%(output)s\" -mr:art -mr:aml " \
                    "\"%(maya_file)s\"" % self.cfg_info
            else:
                cmd = "\"%(render_exe)s\" -s %(start)s -e %(end)s -b %(by)s " \
                    "-proj \"%(project)s\" -rd \"%(output)s\" -mr:art -mr:aml" \
                    % self.cfg_info

                if self.extra_info["renderableCamera"]:
                    if not "," in self.extra_info["renderableCamera"]:
                        cmd += " -cam \"%(renderableCamera)s\"" % self.extra_info

#                if "submit_mode" in self.cfg_info:
#                    if self.cfg_info["submit_mode"] == 2:
#                        self.extra_info = self.get_extra_info()
#                        cmd += " -cam \"%(renderableCamera)s\"" % self.extra_info

                if self.cfg_info["user_id"] in [962413]:
                    cmd += " -preRender \"python \\\"user_id=%s;execfile(\\\\\\\"//10.50.5.29/o5/py/model/prerender.py\\\\\\\")\\\"\"" % (self.cfg_info["user_id"])

#                    image_name = os.path.basename(self.cfg_info["maya_file"]).split("-")[0]
#                    image_name = "<RenderPass>/" + image_name + "_<RenderPass>"
#                    cmd += " -im \"%s\"" % image_name

                    if self.cfg_info["maya_version"] == 2013:
                        pre_bat = r"\\10.50.8.16\td\zhaoxiaofei\HQ_Animation\HQ_Setting.bat"
                        cmd = "\"%s\" && %s" % (pre_bat, cmd)

                    if self.cfg_info["maya_version"] == 2015:
                        pre_bat = r"\\10.50.8.16\td\zhaoxiaofei\HQ_Animation\2015_VFX\HQ_VFX_Setting.bat"
                        cmd = "\"%s\" && %s" % (pre_bat, cmd)

                if self.cfg_info["user_id"] in [120151, 100001]:
#                    if self.extra_info["projectSymbol"] == "moon":
                    pre_bat = r"\\10.50.8.16\td\zhaoxiaofei\ants_moon\moon.bat"
                    cmd = "\"%s\" && %s" % (pre_bat, cmd)

                if self.cfg_info["user_id"] in [962471]:
                    pre_bat = r"\\10.50.8.16\td\zhaoxiaofei\vj\vj.bat"
                    cmd = "\"%s\" && %s" % (pre_bat, cmd)

                cmd += " \"%(maya_file)s\"" % self.cfg_info

            print cmd
            sys.stdout.flush()

            if "single_frames" in self.cfg_info:
                if self.cfg_info["single_frames"]:
                    if self.cfg_info["start"] in self.cfg_info["single_frames"]:
                        print "Render this single frame."
                        subprocess.call(cmd)
                        return 0
                    else:
                        print "This frame doesn't need to be rendered."
                        return 0

            subprocess.call(cmd)

if __name__ == '__main__':
    render = MayaRender(sys.argv[1])
    render.render(*sys.argv[2:])


