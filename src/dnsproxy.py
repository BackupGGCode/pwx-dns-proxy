# -*- encoding: utf-8 -*-

"""
基于 Twisted 框架的 DNS Proxy 服务器。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

#
# TODO:
#
# 因为 Twisted 事件循环、以及 Defered 对象（延迟计算）的原因，
# Timeout 异常无法捕获。（在 dispatcher.py：_my_dispatch）。
#
# 请合理修改这个文件的内容，以捕获这个异常。
#

# 设置模块寻找路径。
import sys, os
appPath = os.path.dirname(os.path.abspath(__file__))
currentPath = os.path.abspath(os.getcwd())

sys.path.insert(0, appPath)

# 加载 Twisted 模块。
from twisted.names import dns, server, client, cache
from twisted.application import service, internet

# 加载项目模块。
import log
from config import Config, LoadConfig, ConfigNotFound
from dispatcher import RequestDispatcher

# 解析命令行参数
import arguments

# 初始化配置文件。
config = None
try:
	config = LoadConfig(appPath, currentPath, arguments.CONFIG_FILE)
except ConfigNotFound as e:
	log.fatal(e.args[0])
	sys.exit(2)
except ValueError as e:
	log.fatal(e.args[0])
	sys.exit(3)
except Exception:
	log.exception("读取配置文件的时候发生了不可预料的异常。")
	sys.exit(100)

# 创建 Twisted 程序框架。
application = service.Application('dnsserver', 1, 1)

# 初始化 Resolver 对象。
resolver = RequestDispatcher(config)

# 初始化协议
f = server.DNSServerFactory(caches=[cache.CacheResolver()], clients=[resolver])
p = dns.DNSDatagramProtocol(f)
f.noisy = p.noisy = False

# 使用 Twisted 运行应用程序。
if __name__ == '__main__':
	from twisted.internet import reactor
	import twisted.internet.interfaces
	
	# 设置侦听端口
	for t in config.tcp_if:
		reactor.listenTCP(port=t[1], factory=f, interface=t[0])
	for u in config.udp_if:
		reactor.listenUDP(port=u[1], protocol=p, interface=u[0])
	
	reactor.run()


