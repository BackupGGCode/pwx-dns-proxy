# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：日志模块。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/9。
"""

import sys
import traceback
import datetime

# 定义 Logger 的消息级别。
UNSET, DEBUG, INFO, WARNING, ERROR, FATAL = range(0, 60, 10)
level_str = {
	UNSET: "UNSET",
	DEBUG: "DEBUG",
	INFO: "INFO",
	WARNING: "WARNING",
	ERROR: "ERROR",
	FATAL: "FATAL",
}
level_map = { v:k for k,v in level_str.items() }

# 当前级别。
level = UNSET

def get_level_str(lv):
	if lv in level_str:
		return level_str[lv]
	else:
		return str(lv)
		
def set_level_str(s):
	global level
	if s in level_map:
		level = level_map[s]
	else:
		try:
			level = int(s)
		except ValueError:
			raise ValueError("日志级别 %s 未定义。" % s)

# 数据输出
def log(lv, message):
	"""
	记录一条日志消息。
	
	参数：
	
	lv -- 消息的级别。预定义的级别为 UNSET, DEBUG,
	  INFO, WARNING, ERROR, FATAL。
	message -- 消息的正文。
	"""
	if level <= lv:
		print unicode("%s: %s: %s" % (datetime.datetime.now().strftime("%H:%M:%S"), get_level_str(lv), message), 'utf-8')
		
def exception(message):
	"""
	记录一个异常。
	
	参数：
	
	message -- 程序的描述。
	"""
	error("%s\n%s" % (message, ''.join(traceback.format_exception(*sys.exc_info()))))

def debug(message):
	log(DEBUG, message)
	
def info(message):
	log(INFO, message)
	
def warning(message):
	log(WARNING, message)
	
def error(message):
	log(ERROR, message)
	
def fatal(message):
	log(FATAL, message)
	

