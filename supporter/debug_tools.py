# coding:utf-8

import time

def console_print(s):
    print("[Debug Info] {time_now}".format(time_now=time.strftime("%Y %b %d %H:%M:%S", time.localtime())))
    print(s)
