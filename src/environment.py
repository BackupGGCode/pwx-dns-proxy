# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：应用程序环境模块。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

import os
import sys

# 取得当前路径
currentPath = os.path.abspath(os.getcwd())

# 取得应用程序的上级路径
appPath = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]

# 供上层调用的 API
def set_current_path(path):
	global currentPath
	currentPath = path

def set_app_path(path):
	global appPath
	appPath = path
