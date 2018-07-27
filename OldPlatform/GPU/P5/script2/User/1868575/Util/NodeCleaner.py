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
import stat

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
        self.G_DEL_LOG=logging.getLogger('dellog'+str(hash(self.G_CLEAN_FOLDER)))
        self.G_DEL_LOG_DIR = os.path.join(self.G_CLEAN_FOLDER,'delLog')
        self.G_DEL_LOG_NAME = str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))) + ur'.txt'
        print '[NodeCleaner.init.end...]'
    
    def del_log(self):
        # delLog/20180108161000.txt
        del_log_dir = self.G_DEL_LOG_DIR
        if not os.path.exists(del_log_dir):
            os.makedirs(del_log_dir)
        # self.DEL_LOG_NAME = str(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))) + ur'.txt'
        
        fm = logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        del_log_path = os.path.join(del_log_dir,self.G_DEL_LOG_NAME)
        self.G_DEL_LOG.setLevel(logging.DEBUG)
        del_log_handler = logging.FileHandler(del_log_path)
        del_log_handler.setFormatter(fm)
        self.G_DEL_LOG.addHandler(del_log_handler)
    
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
    
    #use when shutil.rmtree can't delete file
    def remove_readonly(self,func, path, excinfo):
        # try:
            # os.chmod(path, stat.S_IWRITE)
            # func(path)
        # except Exception as e:
        # self.log_print(ur'[delete error1]  '+path)
        # self.log_print(sys.exc_info())
        # self.log_print(excinfo)
        try:
            self.G_DEL_LOG.info(ur'[delete error1]  '+path)
            self.G_DEL_LOG.info(excinfo)
        except:
            pass
    
    def clean_folder_by_stay_time(self,folder):
        if os.path.exists(folder) and os.path.isdir(folder):
            self.log_print(folder)
            current_time = time.time()
            sub_file_list = os.listdir(folder)
            for sub in sub_file_list:
                if sub == ur'delLog' or sub == self.G_DEL_LOG_NAME:
                    pass
                else:
                    sub_file = os.path.normpath(os.path.join(folder,sub))
                    
                    sub_file_modify_time = os.path.getmtime(sub_file)
                    sub_file_create_time = os.path.getctime(sub_file)
                    sub_file_modify_time_formater = self.format_time(sub_file_modify_time)#modify time
                    sub_file_create_time_formater = self.format_time(sub_file_create_time)#create time
                    
                    stay_hour = (current_time-sub_file_modify_time) / 3600 
                    
                    file_str = sub_file + '  |CreateTime|' + sub_file_create_time_formater + '|ModifyTime|' + sub_file_modify_time_formater + '|StayHours|' + str(stay_hour)
                    
                    if stay_hour > self.G_KEEP_HOUR:
                        try:
                            if os.path.isdir(sub_file):
                                shutil.rmtree(sub_file, onerror=self.remove_readonly)
                            else:
                                os.remove(sub_file)
                            # self.log_print(ur'[delete success]  '+file_str)
                            try:
                                self.G_DEL_LOG.info(ur'[delete completed]  '+file_str)
                            except:
                                pass
                        except Exception as e:
                            # self.log_print(ur'[delete error2]  '+file_str)
                            # self.log_print(e)
                            try:
                                self.G_DEL_LOG.info(ur'[delete error2]  '+file_str)
                                self.G_DEL_LOG.info(e)
                            except:
                                pass
                    else:
                        # self.log_print(ur'[stay]  '+file_str)
                        try:
                            self.G_DEL_LOG.info(ur'[stay]  '+file_str)
                        except:
                            pass
    
    @decorator_use_in_class
    def main(self):
        try:
            self.del_log()  #init G_DEL_LOG
            self.clean_folder_by_stay_time(self.G_DEL_LOG_DIR)
        except:
            self.log_print('[warn]del log init fail')
        
        self.clean_folder_by_stay_time(self.G_CLEAN_FOLDER)  # main
    
if __name__ == '__main__':
    path = raw_input('path>>>')
    hour = raw_input('hour>>>')
    aa = NodeCleaner(path,int(hour))
    aa.main()