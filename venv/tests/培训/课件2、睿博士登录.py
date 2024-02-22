# -*- coding: utf-8 -*-
"""
-
Author:
Date:
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

# 启动睿博士app
driver = webdriver.Remote('http://localhost:4723/wd/hub', appium_android_config)

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
