# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：日志模块。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/9。
"""

import sys
import datetime
import logging
import logging.config

# 初始化 logger 对象
_log_enabled = True
_log = logging.getLogger()

# 设置屏幕日志输出
_my_console_handler = logging.StreamHandler(sys.stdout)
_my_handlers = [
	_my_console_handler,
]
_my_formatter = logging.Formatter(
	fmt='%(asctime)s: %(levelname)s: %(message)s',
	datefmt=None
)
_my_console_handler.setFormatter(_my_formatter)

_log.addHandler(_my_console_handler)

# 启用 / 禁用 log
def enable_log():
	global _log_enabled
	_log_enabled = True
	
def disable_log():
	global _log_enabled
	_log_enabled = False

# 包装 logging 类型
def log(lvl, message):
	# 转换字符串格式
	if not isinstance(message, unicode):
		if not isinstance(message, str):
			message = str(message)
		message = unicode(message, 'utf-8')
	
	# 输出
	if _log_enabled:
		_log.log(lvl, message)
	
def exception(message):
	log(logging.ERROR, message)

def debug(message):
	log(logging.DEBUG, message)
	
def info(message):
	log(logging.INFO, message)
	
def warning(message):
	log(logging.WARNING, message)
	
def error(message):
	log(logging.ERROR, message)
	
def fatal(message):
	log(logging.CRITICAL, message)

# 日志级别的操作函数
def get_level_str(lv):
	return logging.getLevelName(lv)
		
def set_level_str(lv, name):
	logging.addLevelName(lv, name)
	
# 日志配置
def set_log_format(fmt, datefmt=None):
	global _my_formatter, _my_handlers
	_my_formatter = logging.Formatter(fmt, datefmt)
	
	for h in _my_handlers:
		h.setFormatter(_my_formatter)
	
def set_log_level(lvl):
	_log.setLevel(lvl)
	
def log_to_file(log_path):
	h = logging.FileHandler(filename=log_path)
	h.setFormatter(_my_formatter)
	_my_handlers.append(h)
	_log.addHandler(h)
