# -*- coding: utf-8 -*-
"""
Author:chenxi
Date:2024年2月7日
"""
# setup.py

import os
from setuptools import setup, find_packages

__version__ = '1.0'  # 版本号
requirements = open('requirements.txt').readlines()  # 依赖文件
pip_path = "C:\\Users\\Administrator\\AppData\\Roaming\\pip\\"
file_name = pip_path + "pip.ini"


# python版本校验，小于3.7返回错误
CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================
This version of Requests requires at least Python {}.{}, but
you're trying to install it on Python {}.{}. To resolve this,
consider upgrading to a supported Python version.

If you can't upgrade your Python version, you'll need to
pin to an older version of Requests (<2.28).
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

# 修改pip下载源为国内地址
# 清华镜像
if not os.path.exists(pip_path):
    os.makedirs(pip_path)
if not os.path.exists(file_name):
    content = """
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
    """
    with open(file_name, "w") as file:
        file.write(content)

# 更新pip
os.system("pip install --upgrade pip ")

setup(
    name='app_auto',  # 在pip中显示的项目名称
    version=__version__,
    author='chenxi',
    author_email='chenxi00110011.@163.com',
    url='',
    description='scr: Test Setup',
    packages=find_packages(exclude=["tests"]),  # 项目中需要拷贝到指定路径的文件夹
    python_requires='>=3.7.0',
    install_requires=requirements  # 安装依赖
)