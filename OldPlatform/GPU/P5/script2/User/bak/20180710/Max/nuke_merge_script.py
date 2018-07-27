# -*-coding: utf-8 -*-
from __future__ import print_function
# import nuke
import os
from pprint import pprint
import glob
import sys

r"""
"C:\Program Files\Nuke8.0v3/Nuke8.0.exe" -t "d:/scripts/合并图片/merge_script.py" 1925 1083 9 d:/NEW1 d:/output 1868550 10000725
"C:\Program Files\Nuke10.0v4/Nuke10.0.exe" -t "d:/nuke_merge_script.py" 1920 1440 3 d:/30009694 d:/output/30009694 1801308 30009694
"C:\Program Files\Nuke8.0v3/Nuke8.0.exe" -t "d:/scripts/合并图片/nuke_merge_script.py" 2500 2313 6 d:/30012500 d:/output/30012500 1882956 30012500
_STP00001_A__STP00000_Renderbus_21944_0000.tga
"""


def make_list(file_list, tilecount, inputpath, height):
    """
    找开头的文件, 用这个文件的名字拼出同一张图片所有分条的文件名并计算好偏移量
    返回格式:
    [
        [
            {name: stp00000aaa, offset: 20, exist: True},
            {name: stp00001aaa, offset: 10, exist: True},
            {name: stp00002aaa, offset: 0, exist: True},
        ],
        [
            {name: stp00000bbb, offset: 20, exist: True},
            {name: stp00001bbb, offset: 10, exist: True},
            {name: stp00002bbb, offset: 0, exist: True},
        ],
        ...
    ]
    """
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
            # 计算
            offset = get_offset(tilecount, height, i)
            filename = os.path.join(inputpath, f)
            d = dict(
                name=filename,
                offset=offset,
                exist=os.path.exists(filename)
            )

            fs.append(d)
        result.append(fs)
    return result


def get_offset(tilecount, height, index):
    """
    移动分条到正确位置的算法, 相对分条左下角的点移动, 需要往上移(最下分条移动 0)
    如果高度不能整除分条数, 偏移量需加上取余的值
    """
    row = tilecount
    total = tilecount
    trm = ((height / row) * (row - (index + 1)))
    remainder = height % row
    if index == total - 1:
        value = trm
    else:
        value = trm + remainder
    return value


def find_missing_zero(inputpath, tilecount):
    counts = []

    for i in range(tilecount):
        prefix = "_STP{}".format(str(i).zfill(5))
        f = os.path.join(inputpath, prefix)
        fs = glob.glob(f + "*")  # 以 stp{n} 开头的所有文件
        counts.append(len(fs))

    n = counts[0]
    m = max(counts)
    result = []
    if n <= m:  # 说明第0条缺失, 需要确定是哪个名字缺失
        # 把最大的分条改成 stp0, 判断是否存在
        prefix = "_STP{}".format(str(m).zfill(5))
        f = os.path.join(inputpath, prefix)
        fs = glob.glob(f + "*")
        for f in fs:
            basename = os.path.basename(f)
            basename = basename.replace(prefix, "_STP00000")
            full_path = os.path.join(inputpath, basename)
            if not os.path.exists(full_path):
                result.append(basename)
    return result


def find_allow_pics(inputpath, tilecount):
    pics = []
    files = os.listdir(inputpath)
    prefix = '_STP00000'
    allow = ["tga", "exr", "tif", "jpg", "png"]

    # 找第 0 条的组成一组
    for i in files:
        if i.startswith(prefix):
            if i.split(".")[-1].lower() in allow:
                pics.append(i)
    # 找缺失的第0条
    missing_pics = find_missing_zero(inputpath, tilecount)
    pics.extend(missing_pics)
    return pics


def merge(width, height, tilecount, inputpath, outputpath, user_id, task_id, debug=False):
    alltex = find_allow_pics(inputpath, tilecount)
    files_list = make_list(alltex, tilecount, inputpath, height)

    for files in files_list:
        pprint(files)
        delete_list = []
        # 创建节点
        merge = nuke.createNode("Merge2")
        constant = nuke.createNode("Constant")
        # 获取格式
        format_name, (width, height) = format_from_setting(width, height, user_id)
        print("format_name: ", format_name)
        # 给 constant设置格式
        constant['format'].setValue(format_name)
        # 连线
        merge.setInput(0, constant)
        # TD
        merge['also_merge'].setValue('all')
        pics = []
        for index, d in enumerate(files):
            f = d["name"]
            if d["exist"] is False:
                # 如果丢失, pass: 让其报错; continue: 跳过该分条, 最终效果是图片有黑条
                # continue
                pass
            read = read_file(f)
            xform = nuke.nodes.Transform(inputs=[read])
            k = xform['translate']
            offset = d["offset"]
            k.setValue(offset, 1)
            pics.append(xform)
            delete_list.append(xform)
            delete_list.append(read)

        # 连线
        num = 1
        for pic in pics:
            if num == 2:
                num += 1
            merge.setInput(num, pic)
            num += 1
        # 找任一分条取得图片名字
        s = files[-1]["name"].split("_", 2)[-1]
        basename = os.path.basename(s)
        fname, ext = os.path.splitext(basename)
        filename = fname + ext.lower()
        fullpath = os.path.join(outputpath, filename).replace("\\", '/')
        if not os.path.exists(outputpath):
            os.makedirs(outputpath)
        save_pictures(merge, fullpath)

        if debug is False:
            delete(delete_list)


def delete(delete_list):
    """删除节点回收内存"""
    for n in delete_list:
        nuke.delete(n)


def standardize(filename):
    """如果名字带特殊符号, 替换成空格并保存"""
    old = filename
    if '#' in filename:
        filename = filename.replace("#", ' ')
    if '@' in filename:
        filename = filename.replace("@", ' ')

    if old != filename:
        os.rename(old, filename)
    return filename


def read_file(filename):
    """
    用 read 节点读取图片,
    return: read
    """
    filename = standardize(filename)
    filename = filename.replace("\\", '/')
    read = nuke.nodes.Read(file=filename)
    if read.error() is True:
        nuke.delete(read)
        filename = filename.decode("gbk").encode('utf-8')
        read = nuke.nodes.Read(file=filename)

    return read


def save_pictures(merge, filename):
    """
    保存图片
    如果是 jpg 图片, 把质量设为1(默认为0.75)
    """
    try:
        filename1 = filename.encode("utf-8")
    except UnicodeDecodeError as e:
        # 处理中文
        filename1 = filename.decode("gbk").encode('utf-8')
    print("[merge] save file: {}".format(filename1))

    w = nuke.nodes.Write(file=filename1, inputs=[merge])
    w["channels"].setValue("all")

    # TD
    ext = os.path.splitext(filename)[-1]
    if ext.lower() in ['.jpg', '.jpeg']:
        print('jpg quality set 1')
        w["file_type"].setValue("jpeg")
        w["_jpeg_quality"].setValue('1')

    nuke.render(w, 1, 1)


def new_format(width, height, user_id):
    """新建一个格式"""
    name = "new_{}".format(user_id)
    new = '{} {} {}'.format(width, height, name)
    nuke.addFormat(new)
    return name


def format_from_setting(width, height, user_id):
    """
    从 nuke 设置中获取 格式名字, 宽, 高
    如果宽高都一样就返回, 否则新建一个
    """
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
    width = 2427
    height = 1500
    row = 12
    tilecount = row
    inputpath = r"D:\30052966\block"
    outputpath = r'd:\output\30052966'
    user_id = '1867717'
    task_id = "30089040"
    merge(width, height, tilecount, inputpath, outputpath, user_id, task_id, debug=True)


def debug_print(width, height, tilecount, inputpath, outputpath, user_id, task_id):
    """Helps to merge manually"""
    s = """
def test():
    width = {width}
    height = {height}
    row = {tilecount}
    tilecount = row
    inputpath = r"{inputpath}"
    outputpath = r"{outputpath}"
    user_id = "{user_id}"
    task_id = "{task_id}"
    merge(width, height, tilecount, inputpath, outputpath, user_id, task_id, debug=True)
    """.format(
        width=width,
        height=height,
        tilecount=tilecount,
        inputpath=inputpath,
        outputpath=outputpath,
        user_id=user_id,
        task_id=task_id,
    )
    print("-" * 20 + "debug code for nuke merge manually" + "-" * 20)
    print(s)
    print("-" * 20 + "debug code for nuke merge manually" + "-" * 20)


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

    debug_print(width, height, tilecount, inputpath, outputpath, user_id, task_id)

    merge(width, height, tilecount, inputpath, outputpath, user_id, task_id, debug=False)
    print("[merge] task end.")


if __name__ == '__main__':
    main()
    # test()
