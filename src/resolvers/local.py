# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：本地 HOST 表解析类。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

from twisted.names import dns, client, error, common
from twisted.names.dns import DomainError
from twisted.names.error import DNSNotImplementedError

import log
from resolvers import ResolveImmediateFailure

class LocalResolver(common.ResolverBase):
	"""
	根据本地 HOSTS 表，解析请求的域名。
	
	只能解析 A 记录以及 AAAA 记录，查询其他任何
	记录都会直接抛出 DNSNotImplementedError 异常。
	"""

	def __init__(self, config):
		"""
		创建一个 LocalResolver 的对象。
		
		参数：
		
		config -- 配置对象。
		"""
		
		# 初始化基类
		common.ResolverBase.__init__(self)
		
		# 记录参数
		self.config = config
		self.hosts = config.hosts
		self.ttl = config.hosts_ttl


	# 直接重载 _lookup，以定义所有查询。
	
	def _lookup(self, name, cls, type, timeout):
		if (type == dns.A):
			return self._my_lookup_A(name, cls, timeout)
		if (type == dns.AAAA):
			return self._my_lookup_AAAA(name, cls, timeout)
		raise DNSNotImplementedError()
	
	def _my_lookup_A(self, name, cls, timeout):
		value = self.hosts.lookupAddress(name)
		if value is not None:
			# 不存在这个域：立刻返回错误
			if value == 0:
				log.info("本地 HOSTS 表断言 %s 域的 A 记录不存在。" % name)
				raise ResolveImmediateFailure()
			# 正常匹配结果
			log.info("本地 HOSTS 表匹配 %s 域的 A 记录。" % name)
			return [
					(
						dns.RRHeader(name, dns.A, cls, self.ttl, dns.Record_A(value, self.ttl)),
					),
					(),
					(),
				]
		raise DomainError()
		
	def _my_lookup_AAAA(self, name, cls, timeout):
		value = self.hosts.lookupIPV6Address(name)
		if value is not None:
			# 不存在这个域：立刻返回错误
			if value == 0:
				log.info("本地 HOSTS 表断言 %s 域的 AAAA 记录不存在。" % name)
				raise ResolveImmediateFailure()
			# 正常匹配结果
			log.info("本地 HOSTS 表匹配 %s 域的 AAAA 记录。" % name)
			return [
					(
						dns.RRHeader(name, dns.AAAA, cls, self.ttl, dns.Record_AAAA(value, self.ttl)),
					),
					(),
					(),
				]
		raise DomainError()



