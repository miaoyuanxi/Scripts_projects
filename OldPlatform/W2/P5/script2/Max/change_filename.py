# -*-coding: utf-8 -*-
import os
import time
import string
import sys
import glob
import random
import json
import shutil
from pprint import pprint

"""
python3
"""
d = {}
encoding = "utf-8"


def gen_word():
    s = string.ascii_lowercase
    word = ''
    for i in range(12):
        c = random.choice(s)
        word += c
    return word


def change_name(input_path, output_path):
    fs = glob.glob((os.path.join(input_path, '_STP00000*')))
    fs1 = glob.glob((os.path.join(input_path, '_STP*')))
    count = len(fs)
    count1 = len(fs1)
    try:
        tilecount = count1 // count
    except ZeroDivisionError as e:
        # print(u"{}没有_STP00000开头的文件!".format(input_path))
        return

    for f in fs:
        basename = os.path.basename(f)
        name, ext = os.path.splitext(basename)  # '_STP00000_大厅_91945_0000', '.tga'  # '_STP00000_A__STP00000_Renderbus_191045_0000', '.tga'
        _, stp, n = name.split("_", 2)  # ['', 'STP00000', '大厅_91945_0000']   # ['', 'STP00000', 'A__STP00000_Renderbus_191045_0000']
        filename = n + ext  # A__STP00000_Renderbus_191045_0000.tga
        word = gen_word()
        for i in range(tilecount):
            num = str(i)
            stp = "_STP{}_".format(num.zfill(5))
            full_name = stp + filename
            if "_STP00000_" in f:
                full_name = full_name.replace("_STP00000_", stp)  #
            old_name = os.path.join(input_path, full_name)
            new_name = os.path.join(input_path, stp + word + ext)
            rename(old_name, new_name)
            # print(u"[check encoding rename] {} --> {}".format(old_name, new_name))
            d[old_name] = new_name

    save_name(output_path)


def save_raw_name(name):
    j = "raw_name.json"
    with open(j, "a", encoding=encoding) as fp:
        fp.write(name + "\n")


def rename(old, new):
    try:
        os.rename(old, new)
    except Exception as e:
        # print(u"[rename] error: {}, old: {}, new:{}".format(e, old, new))
        pass


def save_name(output_path):
    j = "name.json"
    filename = os.path.join(output_path, j)
    with open(filename, 'w', encoding=encoding) as fp:
        json.dump(d, fp, indent=2)


def load_name(output_path):
    global d
    j = "name.json"
    filename = os.path.join(output_path, j)
    with open(filename, 'r', encoding=encoding) as fp:
        d = json.load(fp)


def restore_name(input_path, output_path):
    load_name(output_path)
    for old, new in d.items():
        rename(new, old)
        # print("[check encoding rename] {} --> {}".format(new, old))
        new_basename = os.path.basename(new)
        old_basename = os.path.basename(old)

        if new_basename.startswith("_STP00000"):
            now_name = new_basename.split("_", 2)[-1]
            old_name = old_basename.split("_", 2)[-1]
            rename(
                os.path.join(output_path, now_name),
                os.path.join(output_path, old_name),
            )
            # print(u"[check encoding rename] {} --> {}".format(now_name, old_name))


def main():
    print(sys.argv)
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    mode = sys.argv[3]

    if mode == "change":
        # os.chdir(input_path)
        change_name(input_path, output_path)
    elif mode == "restore":
        # os.chdir(output_path)
        restore_name(input_path, output_path)


if __name__ == '__main__':
    main()
