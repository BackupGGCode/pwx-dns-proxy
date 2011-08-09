# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：请求派发类。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

from twisted.names import dns, client, error, common
from twisted.names.dns import DomainError
from twisted.names.error import DNSNotImplementedError, DNSQueryTimeoutError
from twisted.internet import defer
from twisted.internet.error import TimeoutError

from resolvers.local import LocalResolver
from upstreamservers import UpstreamServers
from resolvers import ResolveImmediateFailure

class RequestDispatcher(common.ResolverBase):
	
	def __init__(self, config):
		"""
		初始化 RequestDispatcher 对象。
		
		参数：
		
		config -- 配置文件对象。
		"""
		
		# 初始化基类
		common.ResolverBase.__init__(self)
	
		# 记录参数
		self.config = config
	
		# 初始化 Resolver 对象。
		self.local = LocalResolver(config)
		self.upstream = UpstreamServers(config)

		
	def _lookup(self, name, cls, type, timeout):
		# 尝试使用 LocalResolver 解析。
		try:
			return self.local._lookup(name, cls, type, timeout)
		except DomainError:
			pass
		except ResolveImmediateFailure:
			return defer.fail(DomainError())
			
		# 尝试使用 Upstream Resolver 解析。
		try:
			resolver = self.upstream.select(name)
			if resolver != None:
				return resolver._lookup(name, cls, type, timeout)
		except DomainError as e:
			return defer.fail(e)
		except TimeoutError as e:
			return defer.fail(e)
		
		# 最终抛出异常
		return defer.fail(DomainError())

	
