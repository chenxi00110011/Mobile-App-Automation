"""
# 模块名称：live_test
# 模块内容：基于安卓手机直播拉流测试
# 测试环境准备：
1、准备一台安卓手机，接上电脑串口，并打开开发者选项里的USB调试
2、开启电脑上的APPuim服务端
"""
# -*- coding: utf-8 -*-
import time
import os
import schedule
import threading
from xrs_app import MobieProject
import pytest
import xrs_adb
import environment_variable
import ntp_util


@pytest.mark.run(order=1)
@pytest.mark.live_streaming
@pytest.mark.repeat(300)
def test_live_streaming(setup_environment: MobieProject):
    """测试绑定解绑设备"""
    # 启动睿博士app，初始化测试环境
    project = setup_environment

    # 打开设备直播
    project.goto('直播页')
    time.sleep(10)

    # 手机截屏，保存到电脑
    shotPath = "C:\\Users\\Administrator\\Desktop\\自动化-appuim+python\\绑定截图\\"
    filename = ntp_util.timestamp_to_date(format="%H-%M-%S") + '.PNG'
    os.system(xrs_adb.command_dict['手机截屏'])
    os.system(f'adb pull {environment_variable.mobile_screen_capture}screenshot.png {shotPath}{filename}')

    # 退出
    project.driver.quit()
    time.sleep(4 * 60 - 10)


def job_01():
    # 直播
    pytest.main(["-s", "-v", "-k", "test_live_streaming"])
    # pytest.main(["-k", "test_bind_and_unbind_device"])


def run_threaded(job_func):
    """
    创建一个新线程来执行作业函数。

    参数:
    job_func (function): 要执行的作业函数。

    Returns:
    None
    """
    print(f'程序 {job_func} 开始执行')

    # 创建新线程并启动
    job_thread = threading.Thread(target=job_func)
    job_thread.start()


if __name__ == "__main__":
    # 定义每天的特定时间执行任务
    job_01()
    # schedule.every().day.at("01:00").do(run_threaded, job_01)
    # schedule.every().day.at("03:00").do(run_threaded, job_01)
    # schedule.every().day.at("06:00").do(run_threaded, job_01)

    while True:
        schedule.run_pending()
        time.sleep(15)
