import time
from datetime import datetime, timedelta
import locale
import re
import easygui
import sys

locale.setlocale(locale.LC_CTYPE, 'chinese')

'''
该模块用于提供时间转换的功能
'''
dict_re = {
    'date_ymdhms': re.compile(r'\d+[\/-]\d+[\/-]\d+ \d+[:-]\d+[:-]\d+'),
    'date_ymd': re.compile("\d{4}[\/-]\d{1,2}[\/-]\d{1,2}")
}


def logToDate(compile, log):
    # 找出日志中的日期
    return re.findall(compile, log)[0]


def get_current_time():
    #:return:返回当前时间戳，格式为年月日时分秒
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def convert_to_timestamp(str):
    '''
    将时间xx-xx-xx xx:xx:xx 格式转变为时间戳
    将时间xx/xx/xx xx:xx:xx 格式转变为时间戳
    将时间xx年xx月xx日 xx:xx:xx 格式转变为时间戳
    :param str:
    :return:
    '''
    if len(str) < 12:
        str = str + " 00:00:00"
    if '-' in str:
        s_t = time.strptime(str, "%Y-%m-%d %H:%M:%S")  # 返回元祖
    elif '/' in str:
        s_t = time.strptime(str, "%Y/%m/%d %H:%M:%S")  # 返回元祖
    elif '年' in str:
        s_t = time.strptime(str, "%Y年%m月%d日 %H:%M:%S")  # 返回元祖
    mkt = int(time.mktime(s_t))
    # print(mkt)
    return mkt


def returnDate(timestamp, mode="%Y-%m-%d %H:%M:%S"):
    time_local = time.localtime(timestamp)
    # 转换成新的时间格式(精确到秒)
    dt = time.strftime(mode, time_local)
    return dt  # 2021-11-09 09:46:48


def today(num=0, mode="%Y-%m-%d"):
    '''
    :param num:输入整数，与当前日期进行天数加减
    :return: 返回该日期的时间戳，格式为年月日
    '''
    now = datetime.now() + timedelta(num)
    res = now.strftime(mode)
    return res


def current_time(num=0, mod=None):
    '''
    :param
    :return:
    '''
    now = datetime.now() + timedelta(num)
    if mod == None:
        return now.strftime("%Y-%m-%d %H:%M:%S")
    elif mod == 'log':
        return now.strftime("%Y-%m-%d_%H%M%S")
    else:
        raise Exception('参数输入错误')


def write(file_path, content):
    with open(file_path, 'w') as file_read:
        file_read.write(content)


def read(file_path):
    with open(file_path, 'r') as file_read:
        return file_read.read()


def multenterbox_c(list):
    '''
    建议输入框，判空和判None处理
    :param list:输入元组或列表
    :return:返回列表
    '''
    while True:
        napes = list
        keys = easygui.multenterbox(fields=napes)
        # print(type(keys))
        if keys is None:
            print('程序结束')
            sys.exit()
        if keys[0] == '' or keys[1] == '':
            continue
    print(type(keys))
    return keys


def get_content(str1, str2, text):
    res = re.findall(rf'{str1}.*{str2}', text)
    res = re.sub(str1, '', res[0])
    res = re.sub(str2, '', res)
    return res


if __name__ == '__main__':
    print(returnDate(1682524800))
