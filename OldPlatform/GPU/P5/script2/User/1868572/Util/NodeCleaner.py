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

    def clean_texture_cache_dir(self, folder):
        """
        2018.02.01
        删除目录改需求
        针对范围：所有平台（W0、W2、W8、W9、GPU、PIC），主要是GPU
        需求修改来源：李玉光
        功能描述：判断Textures目录的创建时间，如果是在一周以前创建的，则删除
        G0、G1是根据GPU核心标志判断
        D:\Temp\REDSHIFT\CACHE\Redshift\Cache\Textures
        D:\Temp\REDSHIFT\CACHE\G0\Redshift\Cache\Textures
        D:\Temp\REDSHIFT\CACHE\G1\Redshift\Cache\Textures
        环境变量里 有 gpuid 这个 key 的话, 就有 D:\Temp\REDSHIFT\CACHE\Redshift\Cache\Textures 目录
        如果 gpuid=1 就有 D:\Temp\REDSHIFT\CACHE\G0\Redshift\Cache\Textures 目录
        如果连 key 都没有, 那就没有这个目录.
        """
        try:
            self.del_log()  #init G_DEL_LOG
            self.clean_folder_by_stay_time(self.G_DEL_LOG_DIR)
        except:
            self.log_print(u'[Textures][warn]del log init fail')
            return

        self.G_DEL_LOG.info(u"[Textures][delete] start: {}".format(folder))
        if not os.path.isdir(folder):
            self.G_DEL_LOG.info(u"[Textures][delete] 没有找到文件夹: {}, 跳过..".format(folder))
            return

        current_time = time.time()
        sub_file_list = os.listdir(folder)
        # 找这底下的文件/文件夹, 如果修改时间大于7天, 就全部删除
        #                        如果不大于7天, 就遍历找创建时间大于7天的文件删除.
        for sub in sub_file_list:

            if sub == u'delLog' or sub == self.G_DEL_LOG_NAME:
                pass
            else:
                sub_file = os.path.normpath(os.path.join(folder, sub))
                try:
                    create_time = os.path.getatime(sub_file)
                except WindowsError as e:
                    self.G_DEL_LOG.info(ur'[Textures][delete error3]  {}'.format(e))
                    return
                create_time_formater = self.format_time(create_time)

                stay_hour = (current_time - create_time) / 3600

                file_str = sub_file + '  |CreateTime|' + create_time_formater + '|StayHours|' + str(stay_hour)
                # 修改时间大于7天直接删除
                if stay_hour > self.G_KEEP_HOUR:
                    try:
                        if os.path.isdir(sub_file):
                            shutil.rmtree(sub_file)
                        else:
                            os.remove(sub_file)
                    except Exception as e:
                        try:
                            self.G_DEL_LOG.info(ur'[Textures][delete error2]  {}'.format(file_str))
                            self.G_DEL_LOG.info(e)
                        except Exception as e:
                            self.G_DEL_LOG.info(e)
                    self.G_DEL_LOG.info(u"[Textures][delete complete]  {}".format(file_str))
                # 修改时间小于7天, 就找里面 创建时间大于7天的删除
                else:
                    if os.path.isdir(sub_file):
                        for root, dirs, files in os.walk(sub_file):
                            for file in files:
                                f = os.path.join(root, file)
                                try:
                                    create_time = os.path.getctime(f)
                                except WindowsError as e:
                                    self.G_DEL_LOG.info(ur'[Textures][delete error3.1]  {}'.format(e))
                                    return
                                create_time_formater = self.format_time(create_time)
                                stay_hour = (current_time - create_time) / 3600
                                file_str = sub_file + '  |CreateTime|' + create_time_formater + '|StayHours|' + str(
                                    stay_hour)
                                if stay_hour > self.G_KEEP_HOUR:
                                    try:
                                        os.remove(f)
                                    except Exception as e:
                                        try:
                                            self.G_DEL_LOG.info(ur'[Textures][delete error2]  {}'.format(file_str))
                                            self.G_DEL_LOG.info(e)
                                        except Exception as e:
                                            self.G_DEL_LOG.info(e)
                                else:
                                    try:
                                        self.G_DEL_LOG.info(ur'[Textures][stay]  {}'.format(file_str))
                                    except Exception as e:
                                        self.G_DEL_LOG.info(e)
        self.G_DEL_LOG.info(u"[Textures][delete] end..")

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