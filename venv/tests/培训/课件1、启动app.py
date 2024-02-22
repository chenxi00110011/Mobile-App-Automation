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

driver = webdriver.Remote('http://localhost:4723/wd/hub', appium_android_config)

time.sleep(5)
driver.quit()
