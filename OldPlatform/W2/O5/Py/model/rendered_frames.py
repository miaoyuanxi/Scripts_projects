# ! /usr/bin/env python
# coding=utf-8
import os
try:
    import pymel.core as pm
except Exception as e:
    pass


def set_rendered_frame(save_path):
    with open(save_path + "/" + str(int(pm.currentTime())), "w"):
        ''


def get_rendered_frames(save_path):
    # "C:\Program Files\Autodesk\Maya2014\bin\render.exe" -rd "c:\test" -postFrame "python \"execfile(\\\"C:/Users/admin/Documents/GitHub/rayvision-websubmit/rendered_frames.py\\\");set_rendered_frame(\\\"C:/test/rendered_frames\\\")\"" E:\test_files\2014_ball.ma
    if os.path.exists(save_path):
        return [int(i) for i in os.listdir(save_path) if i.isalnum()]

    return []


def get_retry_frames(start, end, save_path):
    # execfile("C:/Users/admin/Documents/GitHub/rayvision-websubmit/rendered_frames.py")
    # get_retry_frames(1, 10, save_path)
    rendered = get_rendered_frames(save_path)
    return [i for i in range(int(start), int(end) + 1) if i not in rendered]
def del_frames(start, end, save_path):
    if os.path.exists(save_path):
        for i in os.listdir(save_path):
            if i.isalnum() and int(i) in range(int(start), int(end) + 1):
                os.remove(save_path + "/" + i)
