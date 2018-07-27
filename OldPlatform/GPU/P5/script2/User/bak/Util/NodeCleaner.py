#!/usr/bin/env python
#encoding:utf-8
# -*- coding:utf-8 -*-
'''
    Function:
        1.clean directory
        2.cross platform
        3.support multithreading
'''

import sys
import os
import subprocess
import logging
import time
import datetime
import shutil

def decorator_use_in_class(f):
    def wrapper(self,*args, **kwargs):
        log_info_start = ur'[%s.%s.start.....]' % (self.__class__.__name__, f.__name__)
        log_info_end = ur'[%s.%s.end.....]' % (self.__class__.__name__, f.__name__)
        self.log_print(log_info_start)
        out = f(self,*args, **kwargs)
        self.log_print(log_info_end)
        return out
    return wrapper

def str_to_unicode(str1,str_decode = 'default'):
    if not isinstance(str1,unicode):
        try:
            if str_decode != 'default':
                str1 = str1.decode(str_decode.lower())
            else:
                try:
                    str1 = str1.decode('utf-8')                        
                except:
                    try:
                        str1 = str1.decode('gbk')
                    except:                            
                        str1 = str1.decode(sys.getfilesystemencoding())
        except Exception as e:
            print '[err]str_to_unicode:decode %s to unicode failed' % (str1)
            print e
    return str1
    
    
class NodeCleaner(object):
    def __init__(self,clean_folder,keep_hour=720,my_log=None):
        print '[NodeCleaner.init.start...]'
        self.G_CLEAN_FOLDER = str_to_unicode(clean_folder)
        self.G_KEEP_HOUR = keep_hour
        self.G_LOG = my_log
        print '[NodeCleaner.init.end...]'
    
    def log_print(self,log_str):
        my_log = self.G_LOG
        if my_log == None:
            try:
                print log_str
            except Exception as e:
                print ur'[err log_print]',e
        else:
            try:
                my_log.info(log_str)
            except Exception as e:
                print ur'[err log_print]',e
    
    def format_time(self,timestamp):
        time_array = time.localtime(timestamp)
        date = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        return str(date)
    
    @decorator_use_in_class
    def clean_folder_by_stay_time(self):
        if os.path.exists(self.G_CLEAN_FOLDER) and os.path.isdir(self.G_CLEAN_FOLDER):
            self.log_print(self.G_CLEAN_FOLDER)
            current_time = time.time()
            sub_file_list = os.listdir(self.G_CLEAN_FOLDER)
            for sub in sub_file_list:
                sub_file = os.path.normpath(os.path.join(self.G_CLEAN_FOLDER,sub))
                
                sub_file_modify_time = os.path.getmtime(sub_file)
                sub_file_create_time = os.path.getctime(sub_file)
                sub_file_modify_time_formater = self.format_time(sub_file_modify_time)#modify time
                sub_file_create_time_formater = self.format_time(sub_file_create_time)#create time
                
                stay_hour = (current_time-sub_file_modify_time) / 3600 
                
                file_str = sub_file + '  |CreateTime|' + sub_file_create_time_formater + '|ModifyTime|' + sub_file_modify_time_formater + '|StayHours|' + str(stay_hour)
                
                if stay_hour > self.G_KEEP_HOUR:
                    try:
                        if os.path.isdir(sub_file):
                            shutil.rmtree(sub_file)
                        else:
                            os.remove(sub_file)
                        # self.log_print(ur'[delete success]  '+file_str)
                    except Exception as e:
                        self.log_print(ur'[delete error]  '+file_str)
                        self.log_print(e)
                # else:
                    # self.log_print(ur'[stay]  '+file_str)
    
    @decorator_use_in_class
    def main(self):
        self.clean_folder_by_stay_time()
    
if __name__ == '__main__':
    path = raw_input('path>>>')
    hour = raw_input('hour>>>')
    aa = NodeCleaner(path,int(hour))
    aa.main()