# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：配置模块。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/9。
"""

import os
import sys

from hosts import HostsTable
from domains import DomainMapper

import log

class Config:
	
	def __init__(self, config_file):
		"""
		初始化 Config 对象。
		
		参数：
		
		config_file -- 配置文件路径。
		
		异常：
		
		如果配置文件有错误，则抛出 ValueError 异常。
		"""
		# 定位配置文件的路径。
		self.config_file = os.path.abspath(config_file)
		self.config_path = os.path.dirname(self.config_file)
		
		
		# 初始化配置变量。
		self.default_server = None
		self.servers = {}
		self.lookups = {}
		self.hosts = HostsTable([])
		self.hosts_ttl = 3600
		self.tcp_if = []
		self.udp_if = []
		
		# 读取配置文件
		execfile(self.config_file, self.expose_functions())
		if self.default_server is None:
			raise ValueError("配置错误：没有指定默认 DNS 服务器。")
		
		# 计算 lookups 映射。
		self.lookups_mapper = DomainMapper(self.lookups.keys())
		
		# 创建 UpstreamResolver 对象。
		# self.resolvers = {}
		# for k, v in self.servers.items():
		# 	self.resolvers[k] = UpstreamResolver(*v)
		# self.default_resolver = UpstreamResolver(*self.default_server)
		
	#
	# 暴露给配置文件的函数。
	#
	
	def expose_functions(self):
		def add_server(name, address, port, tcp, timeout=5):
			"""
			向配置文件里面加入一个 DNS 服务器。
		
			参数：
		
			name -- 字符串。服务器的名称。
			address -- 字符串。服务器的地址。
			port -- 整数。服务器的端口。
			tcp -- 布尔值。是否使用 tcp 链接。
			timeout -- 整数。表示上游服务器的超时秒数。
			  如果没有指定，则为默认 5 秒钟。
			"""
			self.servers[name] = (address, port, tcp, timeout)
			if self.default_server is None:
				self.default_server = self.servers[name]
			
		def set_default_server(name):
			"""
			设置默认服务器。
		
			参数：
		
			name -- 默认服务器的名称。
			  如果服务器不存在，则抛出 ValueError。
			"""
			if not (name in self.servers):
				raise ValueError("配置错误：服务器 '%s' 未定义。" % name)
			self.default_server = self.servers[name]
		
		def add_lookups(server, hosts):
			"""
			增加域名解析策略。
		
			参数：
		
			server -- 上游 DNS 服务器的名称。
			  如果服务器不存在，则抛出 ValueError。
			hosts -- 目标域名。
			"""
			if not (server in self.servers):
				raise ValueError("配置错误：服务器 '%s' 未定义。" % name)
			if not isinstance(hosts, tuple) and not isinstance(hosts, list):
				hosts = ( hosts, )
			for h in hosts:
				self.lookups[h.lower()] = server
			
		def init_hosts(hosts_source):
			"""
			使用字符串初始化 HOSTS 表。
		
			参数：
			
			hosts_source -- 字符串。包含了完整的 HOSTS 文件内容。
			"""
			self.hosts = HostsTable(hosts_source.split("\n"))
			
		
		def init_hosts_file(hosts_file):
			"""
			从文件读取 HOSTS 表。
			
			参数：
			
			hosts_file -- 字符串。HOSTS 文件的路径。
			"""
			
			with open(os.path.join(self.config_path, hosts_file), 'r') as f:
				self.hosts = HostsTable(f)
				
		def set_hosts_ttl(ttl):
			"""
			设置 HOSTS 表的 TTL。
			
			参数：
			
			ttl -- 存活时间。（秒数）
			"""
			self.hosts_ttl = ttl
				
		def chroot(path):
			"""
			更改配置文件所在的目录。
			
			参数：
			
			path -- 字符串。配置文件的路径名。 
			"""
			self.config_path = path
			
		def listenTCP(port, address=''):
			"""
			在指定地址上监听 TCP 端口。
			
			参数：
			
			port -- 端口号。
			address -- 监听地址。如果为''，则监听全部。
			  默认为 ''。
			"""
			self.tcp_if.append( (address, port) )
		
		def listenUDP(port, address=''):
			"""
			在指定地址上监听 TCP 端口。
			
			参数：
			
			port -- 端口号。
			address -- 监听地址。如果为''，则监听全部。
			  默认为 ''。
			"""
			self.udp_if.append( (address, port) )
			
		return {
			# 路径配置
			"chroot": chroot,
			
			# 侦听设置
			"listen_tcp": listenTCP,
			"listen_udp": listenUDP,
		
			# UpstreamServers 配置
			"add_server": add_server,
			"set_default_server": set_default_server,
			"add_lookups": add_lookups,
			
			# HOSTS 配置
			"init_hosts": init_hosts,
			"init_hosts_file": init_hosts_file,
			"set_hosts_ttl": set_hosts_ttl,
			
			# 日志设置
			"enable_log": log.enable_log,
			"disable_log": log.disable_log,
			"get_level_str": log.get_level_str,
			"set_level_str": log.set_level_str,
			"set_log_format": log.set_log_format,
			"set_log_level": log.set_log_level,
			"log_to_file": log.log_to_file,
		}


class ConfigNotFound(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)

def LoadConfig(appPath, currentPath, param=None):
	"""
	根据命令行参数以及操作系统特性，按照以下顺序搜索可用的配置文件。
	
	1、命令行参数 param。
	2、当前目录下的 dnsproxy.conf 文件。
	3、当前目录下的 data/dnsproxy.conf 文件。
	4、程序目录下的 dnsproxy.conf 文件。
	5、程序目录下的 data/dnsproxy.conf 文件。
	6、如果是 Posix 操作系统，则依次查 /etc/pwx-dns-proxy.conf
	   和 /etc/pwx-dns-proxy/dnsproxy.conf。
	
	如果没有一个可用的配置文件被找到，则汇报错误。
	"""
	
	# 优先处理命令行参数
	if param is not None:
		if not os.path.isfile(param):
			raise ConfigNotFound("文件 %s 不存在。" % param)
		return Config(param)
		
	# 确定可疑的配置文件地址
	path_to_search = (
		os.path.join(currentPath, 'dnsproxy.conf'),
		os.path.join(currentPath, 'data/dnsproxy.conf'),
		os.path.join(appPath, 'dnsproxy.conf'),
		os.path.join(appPath, 'data/dnsproxy.conf'),
		'/etc/pwx-dns-proxy.conf',
		'/etc/pwx-dns-proxy/dnsproxy.conf',
	)
	
	for p in path_to_search:
		if os.path.isfile(p):
			return Config(p)
			
	raise ConfigNotFound("未能在以下路径找到有效的配置文件：\n\n%s" % "\n".join(path_to_search))
	

