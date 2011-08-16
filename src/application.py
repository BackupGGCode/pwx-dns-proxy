# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：主程序模块。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/10。
"""

#
# TODO:
#
# 因为 Twisted 事件循环、以及 Defered 对象（延迟计算）的原因，
# Timeout 异常无法捕获。（在 dispatcher.py：_my_dispatch）。
#
# 请合理修改这个文件的内容，以捕获这个异常。
#

# 记录版本
VERSION = "0.1 alpha 3"

# 加载系统模块。
import sys, os

# 加载 Twisted 模块。
from twisted.names import dns, server, client, cache
from twisted.application import service, internet
from twisted.application.app import startApplication
from twisted.internet.error import CannotListenError
from twisted.internet import reactor

# 加载项目模块。
import log
import environment
from config import Config, LoadConfig, ConfigNotFound
from dispatcher import RequestDispatcher

# 应用程序框架
application = None
config = None
factory = None
protocol = None


# 程序控制
def init(config_file):
	global config, application, factory, protocol
	
	# 初始化配置文件。
	try:
		config = LoadConfig(environment.appPath, environment.currentPath,
						config_file)
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
	factory = server.DNSServerFactory(caches=[cache.CacheResolver()], clients=[resolver])
	protocol = dns.DNSDatagramProtocol(factory)
	factory.noisy = protocol.noisy = False
		
	# 设置侦听端口
	last_listen = None
	try:
		for t in config.tcp_if:
			last_listen = ["tcp"] + list(t)
			reactor.listenTCP(port=t[1], factory=factory, interface=t[0])
		for u in config.udp_if:
			last_listen = ["udp"] + list(u)
			reactor.listenUDP(port=u[1], protocol=protocol, interface=u[0])
	except CannotListenError:
		log.fatal("无法打开侦听端口 %s，程序退出。" % last_listen)
		sys.exit(4)
	except Exception:
		log.exception("打开代理服务器端口的时候发生了异常。")
		sys.exit(100)
		
def dispose():
	global config, application, factory, protocol
	
def run():
	startApplication(application, 0)
	reactor.run()
	
def stop():
	reactor.stop()


