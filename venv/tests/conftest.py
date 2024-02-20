# 模块名称：conftest
# 模块内容：fixture函数集合
# 作者: 陈 熙
# -*- coding: utf-8 -*-
from xrs_app import MobieProject
from arp_scan import get_ip
from xrs_serial import serial_bitstream
import pytest
import xrs_adb
import xrs_cgi
import os
import time


@pytest.fixture(scope="function")
def setup_environment():
    """初始化测试环境"""
    # 在这里进行测试环境的初始化操作
    try:
        project = MobieProject('睿博士')
        assert project.pwd() == "首页"
        return project
    except Exception as e:
        print(e)
        setup_environment()


@pytest.fixture(scope="session", autouse=True)
def mobile_phone_reboot():
    # (仅在会话开始时执行一次)
    print("重启手机")

    # 重启手机
    os.system("adb shell settings put global adb_enabled 1")
    os.system("adb reboot")
    time.sleep(60)

    # 点亮屏幕和解锁
    xrs_adb.wakeUpScreen()  # 点亮屏幕
    os.system(xrs_adb.command_dict['滑屏解锁'])  # 解锁
    while not xrs_adb.check_device_connection():
        time.sleep(10)
    os.system("adb shell input tap 100 100")  # 取消提示弹窗


@pytest.fixture(scope="session", autouse=True)
def device_reboot():
    # 设备重启，会话级别(仅在会话开始时执行一次)
    print("设备上电")
    # 设备上电
    try:
        serial_bitstream('COM36', '断电', 1)
        serial_bitstream('COM36', '上电', 1)
    except Exception as e:
        print(e)


@pytest.fixture(scope="function")
def device_factoryDefault():
    # 设备恢复出厂，函数级别
    print("设备恢复出厂")
    dev_ip = get_ip("34:7D:E4:99:03:74")
    xrs_cgi.system_factoryDefault(dev_ip)
