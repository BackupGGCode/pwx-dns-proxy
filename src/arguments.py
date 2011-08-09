# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：命令行参数解析模块。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/9。
"""

import getopt, sys

# 记录版本
VERSION = "0.1 alpha 2"

# 输出参数用法
def usage():
	print "平芜泫 DNS 代理服务器 %s" % VERSION
	print ""
	print "命令行：dnsproxy [--version] [-h] [--help] [-c config-file] [--config=config-file]"
	print ""
	print "参数说明："
	print "--version：输出版本号。"
	print "-h, --help：输出命令行帮助。"
	print "-c, --config：指定配置文件。"

# 解析参数
try:
	_optlist, _args = getopt.getopt(sys.argv[1:], "c:h", ["help", "version", "config="])
except getopt.GetoptError as err:
	print str(err)
	sys.exit(1)

# 记录参数
CONFIG_FILE = None

for o,a in _optlist:
	if o == '--version':
		print "平芜泫 DNS 代理服务器 %s" % VERSION
		sys.exit(0)
	elif o in ('-h', '--help'):
		usage()
		sys.exit(0)
	elif o in ('-c', '--config'):
		CONFIG_FILE = a

		
	
