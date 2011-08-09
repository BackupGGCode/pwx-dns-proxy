# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：上游服务器管理类。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

from resolvers.upstream import UpstreamResolver

class UpstreamServers:

	def __init__(self, config):
		"""
		初始化 UpstreamServers 的类型。
		
		参数：
		
		config -- 配置文件对象。
		"""
		
		# 记录参数
		self.config = config
		
		# 创建 UpstreamResolver 对象。
		self.resolvers = {}
		for k, v in self.config.servers.items():
			self.resolvers[k] = UpstreamResolver(*v)
		self.default_resolver = UpstreamResolver(*self.config.default_server)
		
	def select(self, name):
		"""
		根据域名选择上游 DNS 服务器。
		
		参数：
		
		name -- 域名。
		"""
		kname = self.config.lookups_mapper.lookup(name)
		if kname is None:
			return self.default_resolver
		return self.resolvers[self.config.lookups[kname]]
		

