import time
import ntplib
from time import mktime, strptime
import pytz
from datetime import datetime, timezone


def get_ntp_time(ntp_server):
    """
    获取NTP服务器的当前时间

    :param ntp_server: NTP服务器地址
    :return: 当前时间（时间戳形式）
    """
    try:
        client = ntplib.NTPClient()
        response = client.request(ntp_server)
        return response.tx_time
    except Exception as e:
        return None


def get_ntp_timestamp(ntp_server="pool.ntp.org", int_val=None):
    """
    获取NTP服务器的当前时间，返回格式为时间戳

    :param int_val: 标记结果是否取整
    :param ntp_server: NTP服务器地址
    :return: 当前时间（时间戳形式）
    """
    ntp_time = get_ntp_time(ntp_server)
    for i in range(3):
        if ntp_time:
            if int_val is None:
                return int(ntp_time)
            else:
                return ntp_time
        else:
            time.sleep(3)
            ntp_time = get_ntp_time(ntp_server)


def get_formatted_ntp_time(dateTimeStr="%Y-%m-%d %H:%M:%S", timeZone='Asia/Shanghai', timestamp=None):
    """
    获取NTP服务器的当前时间，返回格式化后的日期字符串（本地时间）

    :param timestamp:
    :param dateTimeStr: 格式字符串，默认为"%Y-%m-%d %H:%M:%S"
    :param timeZone: 时区，默认为"Asia/Shanghai"
    :return: 当前时间的格式化字符串
    """
    try:
        if not timestamp:
            # 创建一个NTP客户端对象
            client = ntplib.NTPClient()

            # 向NTP服务器请求时间信息，并获得返回的时间戳（UTC时间）
            response = client.request('pool.ntp.org')
            utc_time = datetime.utcfromtimestamp(response.tx_time)  # 将时间戳转换为UTC时间
        else:
            utc_time = datetime.utcfromtimestamp(timestamp)
        # 将UTC时间转换为本地时间
        local_tz = pytz.timezone(timeZone)  # 设置时区为上海
        local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)

        return local_time.strftime(dateTimeStr)  # 格式化输出

    except Exception as e:
        print(e)
        # 如果遇到异常，返回None
        return None


def str_time_to_timestamp(time_str, format="%Y-%m-%d %H:%M:%S"):
    """
    将时间字符串转换为时间戳形式

    :param time_str: 时间字符串
    :param format: 时间字符串的格式，默认为 "%Y-%m-%d %H:%M:%S"
    :return: 时间戳
    """
    if format == '%H:%M':
        t = datetime.strptime(time_str, '%H:%M').replace(tzinfo=timezone.utc)
        timestamp = int(t.timestamp())
        return timestamp
    else:
        time_tuple = strptime(time_str, format)
        return mktime(time_tuple)


def compare_time(time1, time2):
    # 将时间字符串转换为 datetime.time 对象
    dt1 = datetime.strptime(time1, '%H:%M').time()
    dt2 = datetime.strptime(time2, '%H:%M').time()

    # 比较时间大小
    if dt1 < dt2:
        return True
    else:
        return False


def get_coordinates(first_interval: tuple, second_interval: tuple, first_coordinate: tuple):
    """输入两个时间区间和第一个时间区间的X轴坐标，输出第二个时间区间的X轴坐标"""
    timestamp_1 = str_time_to_timestamp(first_interval[0], '%H:%M')
    timestamp_2 = str_time_to_timestamp(first_interval[1], '%H:%M')
    timestamp_3 = str_time_to_timestamp(second_interval[0], '%H:%M')
    timestamp_4 = str_time_to_timestamp(second_interval[1], '%H:%M')
    seceond_coordinate_1 = (timestamp_3-timestamp_1)/(timestamp_2-timestamp_1) * (
            first_coordinate[1]-first_coordinate[0]) + first_coordinate[0]
    seceond_coordinate_2 = (timestamp_4 - timestamp_1) / (timestamp_2 - timestamp_1) * (
                first_coordinate[1] - first_coordinate[0]) + first_coordinate[0]
    return int(seceond_coordinate_1), int(seceond_coordinate_2)


def timestamp_to_date(format="%Y-%m-%d", today=0):
    """以%y-%m-%d形式输出当前时间"""
    timestamp = time.time() + today * 86400
    formatted_date = time.strftime(format, time.localtime(timestamp))
    return formatted_date

if __name__ == "__main__":
    # print(get_formatted_ntp_time('%Y-%m-%d'))
    # print(compare_time('00:00','01:00'))
    # print(str_time_to_timestamp('10:00', '%H:%M'))
    # print(get_coordinates(('10:00','13:00'), ('12:30','13:00'),(70,880)))
    print(timestamp_to_date('%m'))