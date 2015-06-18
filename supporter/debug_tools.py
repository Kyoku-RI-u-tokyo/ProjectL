# coding:utf-8
import time


def console_print(debug_info):
    print("[Debug Info] {time_now}: {debug_info}".format(time_now=time.strftime("%Y %b %d %H:%M:%S", time.localtime()),
                                                         debug_info=str(debug_info)))
