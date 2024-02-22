# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
"""
为什么要封装代码?
1、提高代码复用性
封装可以将一些常用的功能封装成独立的模块或类，然后在需要的地方进行调用。这样可以避免重复编写相同的代码，提高了代码的复用性。
2、提高代码可维护性
封装可以将复杂的逻辑和细节隐藏起来，只暴露必要的接口。这样，当内部实现需要更改时，只要接口保持不变，外部代码就不需要修改，从而提高了代码的可维护性。
...
"""

"""
如何封装代码？
1、将代码封装为方法
关键字 def 
"""

import time
from appium import webdriver

appium_android_config = {'platformName': 'Android',
                         'platformVersion': '11',
                         'deviceName': 'xxx',
                         'appPackage': 'com.zwcode.p6slite',
                         'appActivity': '.activity.LoginActivity',
                         'unicodeKeyboard': True,
                         'resetKeyboard': True,
                         'noReset': True,
                         'newCommandTimeout': 6000,
                         'automationName': 'UiAutomator2'
                         }


def login(config=None):
    # 启动睿博士app
    if config is None:
        config = appium_android_config
    driver = webdriver.Remote('http://localhost:4723/wd/hub', config)

    # 输入账户
    driver.find_element('id', 'com.zwcode.p6slite:id/login_user').send_keys('13638601129')

    # 输入密码
    driver.find_element('id', 'com.zwcode.p6slite:id/login_pwd').send_keys('cx123456')

    # 勾选同意《用户协议》
    driver.find_element('id', 'com.zwcode.p6slite:id/read_privacy_check_box').click()

    # 点击登录
    driver.find_element('id', 'com.zwcode.p6slite:id/login_login').click()

    # 等待5秒
    time.sleep(5)

    # 退出app
    driver.quit()


login(appium_android_config)
