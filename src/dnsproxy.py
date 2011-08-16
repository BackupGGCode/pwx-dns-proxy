# -*- encoding: utf-8 -*-

"""
基于 Twisted 框架的 DNS Proxy 服务器。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

# 设置模块寻找路径。
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载项目模块。
import application

# 解析命令行参数
import getopt, sys
from application import VERSION

# 命令行用法
def usage():
	print unicode("平芜泫 DNS 代理服务器 %s" % VERSION, 'utf-8')
	print ""
	print u"命令行：dnsproxy [-c config-file | --config=config-file] [--version]" + \
			u" [-h | --help]"
	print u""
	print u"参数说明："
	print u"--version：输出版本号。"
	print u"-h, --help：输出命令行帮助。"
	print u"-c, --config：指定配置文件。"

# 解析参数
optlist = None
args = None

try:
	optlist, args = getopt.getopt(sys.argv[1:], "c:h", 
		["help", "version", "config="])
except getopt.GetoptError as err:
	print str(err)
	sys.exit(1)

# 记录参数
CONFIG_FILE = None

for o,a in optlist:
	if o == '--version':
		print unicode("平芜泫 DNS 代理服务器 %s" % VERSION, 'utf-8')
		sys.exit(0)
	elif o in ('-h', '--help'):
		usage()
		sys.exit(0)
	elif o in ('-c', '--config'):
		CONFIG_FILE = a
	
# 运行主程序
if __name__ == '__main__':
	application.init(CONFIG_FILE)
	application.run()


