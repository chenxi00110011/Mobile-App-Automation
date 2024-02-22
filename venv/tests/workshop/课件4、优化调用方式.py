# -*- coding: utf-8 -*-
"""
-
Author:
Date:
"""
import time
import xrs_app


driver = xrs_app.MobieProject('睿博士')
driver.goto('首页')
driver.goto('登录页')
driver.goto('设置页')
time.sleep(10)
