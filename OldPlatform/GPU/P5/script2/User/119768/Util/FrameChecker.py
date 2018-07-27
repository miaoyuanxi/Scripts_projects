#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Function:
    1.Check whether the output directory of the node machine is empty.
    2.Check whether the pictures in the output directory of node machine are correctly copied to user storage.
"""

import os
import sys
import time

class FrameChecker(object):
    def __init__(self, src_directory, dest_directory, my_log=None):
        self.my_log = my_log
        self.log_print('[FrameChecker.start...]')
        self.system_sep = os.sep
        self.src_directory = self.str_to_unicode(os.path.normpath(src_directory).rstrip(self.system_sep))
        self.dest_directory = self.str_to_unicode(os.path.normpath(dest_directory).rstrip(self.system_sep))
    
    def log_print(self, log_str):
        """
        Write log to file or just print log.
        :param str log_str: The log that needs to be printed.
        """
        if self.my_log == None:
            print log_str
        else:
            self.my_log.info(log_str)
    
    def str_to_unicode(self, str1, str_decode='default'):  
        if not isinstance(str1, unicode):
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
                self.log_print('[err]str_to_unicode:decode %s to unicode failed' % (str1))
                self.log_print(e)
        return str1
    
    def error_exit_log(self, log_str, exit_code=-1, is_exit=True):
        """
        Format the error/warning log.
        :param str log_str: The error/warning information that needs to be printed.
        :param int exit_code: The exit code.
        :param bool is_exit: Whether or not to exit directly.
        """
        big_info = '[error]' if is_exit else '[warning]'
        self.log_print('---------------------------------%s---------------------------------' % big_info)
        self.log_print(log_str)
        self.log_print('-------------------------------------------------------------------------\r\n')
        if is_exit:
            sys.exit(exit_code)
    
    def check_path_exist(self, path, retry_times=3, sleep_time=5):
        """
        Check whether the path exists, and reduce the impact of network factors by retrying.
        :param str path: The path to be checked.
        :param int retry_times: If the path does not exist, the number of retries.default is 3 times.
        :param int sleep_time: Sleep time before each retrial.default is 5 seconds.
        """
        current_times = 1
        while current_times <= retry_times:
            if os.path.exists(path):
                break
            else:
                current_times += 1
                if current_times == retry_times:
                    self.error_exit_log('The path is not exist:%s' % path)
                time.sleep(sleep_time)
    
    def check_output_empty(self):
        """
        1.Check whether the output directory of the node machine is empty.
        """
        # src_directory_list = os.listdir(self.src_directory)
        is_empty_output = True
        for root, dirs, files in os.walk(self.src_directory):
            if len(files) > 0:
                is_empty_output = False
                break
        if is_empty_output:
            self.error_exit_log('The output is empty:%s' % self.src_directory)
        
    def check_correctly_copy(self):
        """
        2.Check whether the pictures in the output directory of node machine are correctly copied to user storage.
        """
        for root, dirs, files in os.walk(self.src_directory):
            for file_name in files:
                src_file_path = os.path.join(root, file_name)
                src_file_size = os.path.getsize(src_file_path)
                file_relative_path = src_file_path.replace(self.src_directory, '').lstrip(self.system_sep)
                dest_file_path = os.path.join(self.dest_directory, file_relative_path)
                
                if src_file_size > 0:
                    if os.path.exists(dest_file_path):
                        dest_file_size = os.path.getsize(dest_file_path)
                        if src_file_size == dest_file_size:
                            self.log_print('{}==size:{}'.format(src_file_path, src_file_size))
                            continue
                        else:
                            self.error_exit_log('Size Different:\nsrc:    %s - %sB\ndest:   %s - %sB' % (src_file_path, str(src_file_size), dest_file_path, str(dest_file_size)), is_exit=False)
                    else:
                        self.error_exit_log('The path is not exist:%s' % dest_file_path, is_exit=False)
                else:
                    self.error_exit_log('The size of file is abnormal:%s : %sB' % (src_file_path, str(src_file_size)), is_exit=False)
    
    def run(self):
        self.check_path_exist(self.src_directory)
        self.check_output_empty()
        self.check_path_exist(self.dest_directory)
        self.check_correctly_copy()
        self.log_print('[FrameChecker.end...]')

def main(*args, **kwargs):
    fc = FrameChecker(*args, **kwargs)
    fc.run()
    
if __name__ == '__main__':
    main()