# -*-coding: utf-8 -*-
import nuke
import os
from pprint import pprint
import glob
import sys

"""
"C:\Program Files\Nuke8.0v3/Nuke8.0.exe" -t "d:/scripts/合并图片/merge_script.py" 1925 1083 9 d:/NEW1 d:/output 1868550 10000725
"C:\Program Files\Nuke10.0v4/Nuke10.0.exe" -t "d:/nuke_merge_script.py" 1920 1440 3 d:/30009694 d:/output/30009694 1801308 30009694
"C:\Program Files\Nuke8.0v3/Nuke8.0.exe" -t "d:/scripts/合并图片/nuke_merge_script.py" 2500 2313 6 d:/30012500 d:/output/30012500 1882956 30012500
_STP00001_A__STP00000_Renderbus_21944_0000.tga
"""


def make_list(path, prefix, file_list, tilecount):
    """
    :param path:
    :param prefix:
    :param file_list:
    :return:
    """
    # 找开头的文件, 用这个文件的名字拼出同一张图片所有分条的文件名
    result = []
    for file in file_list:
        s = file.split("_", 2)[-1]  # ['', 'STP00000', '0000.tga'] # '0000.tga'
        # fs = glob.glob("{}/*?{}".format(path, s))
        fs = []
        for i in range(tilecount):
            num = str(i)
            stp = "_STP{}_".format(num.zfill(5))
            f = "{}{}".format(stp, s)
            if "_STP00000_" in f:
                f = f.replace("_STP00000_", stp)
            fs.append(f)
        result.append(fs)
    return result


def merge(width, height, tilecount, inputpath, outputpath, user_id, task_id):
    row = tilecount

    alltex = []
    parentdir = inputpath
    subdirs = os.listdir(inputpath)

    prefix = '_STP00000'
    allow = ["tga", "exr", "tif", "jpg", "png"]
    for i in subdirs:
        if i.startswith(prefix):
            if i.split(".")[-1].lower() in allow:
                alltex.append(i)
    files_list = make_list(parentdir, prefix, alltex, tilecount)

    pprint("[merge file list: {}]".format(files_list))

    for files in files_list:
        delete_list = []
        merge = nuke.createNode("Merge2")
        constant = nuke.createNode("Constant")
        format_name, (width, height) = format_from_setting(width, height, user_id)
        print("format_name: ", format_name)
        constant['format'].setValue(format_name)
        merge.setInput(0, constant)
        merge['also_merge'].setValue('all')
        pics = []
        for index, f in enumerate(files):
            f = os.path.join(inputpath, f)
            read = read_file(f)
            xform = nuke.nodes.Transform(inputs=[read])
            k = xform['translate']
            trm = ((height / row) * (row - (index + 1)))
            remainder = height % row
            if index == len(files) - 1:
                k.setValue(trm, 1)
            else:
                k.setValue(trm + remainder, 1)
            pics.append(xform)
            delete_list.append(xform)
            delete_list.append(read)

        num = 1
        for pic in pics:
            if num == 2:
                num += 1
            merge.setInput(num, pic)
            num += 1

        s = files[-1].split("_", 2)[-1]
        basename = os.path.basename(s)
        fname, ext = os.path.splitext(basename)
        filename = fname + ext.lower()
        fullpath = os.path.join(outputpath, filename).replace("\\", '/')
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)
        save_pictures(merge, fullpath)
        delete(delete_list)


def delete(delete_list):
    """删除节点回收内存"""
    for n in delete_list:
        nuke.delete(n)


def standardize(filename):
    old = filename
    if '#' in filename:
        filename = filename.replace("#", ' ')
    if '@' in filename:
        filename = filename.replace("@", ' ')

    if old != filename:
        os.rename(old, filename)
    return filename


def read_file(filename):
    filename = standardize(filename)
    filename = filename.replace("\\", '/')
    read = nuke.nodes.Read(file=filename)
    if read.error() is True:
        nuke.delete(read)
        filename = filename.decode("gbk").encode('utf-8')
        read = nuke.nodes.Read(file=filename)

    return read


def save_pictures(merge, filename):
    try:
        filename1 = filename.encode("utf-8")
    except UnicodeDecodeError as e:
        # 处理中文
        filename1 = filename.decode("gbk").encode('utf-8')
    print("[merge] save file: {}".format(filename1))

    w = nuke.nodes.Write(file=filename1, inputs=[merge])
    w["channels"].setValue("all")

    ext = os.path.splitext(filename)[-1]
    if ext.lower() in ['.jpg', '.jpeg']:
        print('jpg quality set 1')
        w["file_type"].setValue("jpeg")
        w["_jpeg_quality"].setValue('1')

    nuke.render(w, 1, 1)


def new_format(width, height, user_id):
    name = "new_{}".format(user_id)
    new = '{} {} {}'.format(width, height, name)
    nuke.addFormat(new)
    return name


def format_from_setting(width, height, user_id):
    script_formats = nuke.formats()
    name = None
    for f in script_formats:
        w = f.width()
        h = f.height()
        if int(width) == w and int(height) == h:
            name = f.name()
            width = w
            height = h
            break
            # return name, (w, h)

    if name is None:
        name = new_format(width, height, user_id)
    return name, (width, height)


def test():
    width = 2000
    height = 1200
    row = 64
    tilecount = row
    inputpath = r"C:\work\render\30025118\block"
    outputpath = r'd:\output\30025118'
    user_id = '1867717'
    task_id = "30025118"
    merge(width, height, tilecount, inputpath, outputpath, user_id, task_id)


def main():
    argv = nuke.rawArgs[3:]
    print("argv:", argv)
    width = int(argv[0])
    height = int(argv[1])
    tilecount = int(argv[2])
    inputpath = argv[3]
    outputpath = argv[4]
    user_id = argv[5]
    task_id = argv[6]

    merge(width, height, tilecount, inputpath, outputpath, user_id, task_id)
    print("[merge] task end.")


if __name__ == '__main__':
    main()
    # test()
