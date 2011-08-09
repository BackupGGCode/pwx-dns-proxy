# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：上游服务器委托解析类。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

from twisted.names import dns, client
from twisted.internet import defer
import log

#class DummyResolver(client.Resolver):
#	def __init__(self, *args, **kwargs):
#		client.Resolver.__init__(self, *args, **kwargs)
#		
#	def connectionLost(self, p):
#		pass
		
# def DummyCallback(d):
#	pass

class UpstreamResolver(client.Resolver):
	def __init__(self, address, port, is_tcp=False, timeout=None):
		"""
		创建一个 UpstreamResolver 的对象。
		
		参数：
		
		address -- 字符串。上游服务器的地址。
		port -- 数值。上游服务器的端口。
		is_tcp -- 布尔值。如果为 True，则使用 TCP 连接上游服务器。
		timeout -- 数值，上游服务器的查询超时时间。
		  如果为 None，则使用默认值 5 秒钟。
		"""
		
		# 记录参数
		self.address = address
		self.port = port
		self.is_tcp = is_tcp
		self.resolv_timeout = timeout
		if timeout is None:
			self.resolv_timeout = 5
		
		# 初始化基类
		client.Resolver.__init__(self, servers=[(address, port)])
		
	def _lookup(self, name, cls, type, timeout):
		#
		# 检查 timeout 设定
		#
		# Twisted 的 Resolver 真是恶搞，queryUDP 的 timeout 是 Sequence，
		# 而 queryTCP 是 int。所以 queryUDP 有超时重试（根据 Sequence 每次
		# 等待的时间变长），而 queryTCP 木有。这样就导致了我不得不舍弃 Retry。
		#
		if timeout is None:
			timeout = self.resolv_timeout
		if isinstance(timeout, tuple) or isinstance(timeout, list):
			if len(timeout) > 0:
				timeout = timeout[0]
			else:
				timeout = self.resolv_timeout
				
		# 建立 Query 对象
		query = dns.Query(name, type, cls)
				
		# 记录 LOG 信息
		via = "udp"
		if self.is_tcp:
			via = "tcp"
		log.info("通过 %(via)s 向 %(server)s:%(port)s 询问 %(query)s。" % 
			{"via": via, "server": self.address, "port": self.port,
			"query": query})
				
		# 
		# 以下是 0.1 alpha 的代码，已经废弃。
		#
		# 使用 self.queryTCP 的话，第二次查询会 timeout。
		# 因此我为每个查询生成一个 Resolver。
		# 
		# 请合理调整代码，以尽量减少对象数量。（可以考虑使用
		# 别的 dns 类库，比如 pydns）。
		#
		#resolver = DummyResolver(servers=[(self.address, self.port)])
		#if self.is_tcp:
		#	ret = resolver.queryTCP([query], timeout)
		#else:
		#	ret = resolver.queryUDP([query], [timeout])
		#ret.addCallback(resolver.filterAnswers)
		#return ret
		
		#
		# 执行查询。
		#
		# UDP 查询内部维护一个查询队列，同一瞬间内相同的查询将不会被重复执行。
		# TCP 连接拥有持久连接池，因此在段时间内可以进行大量 DNS 查询。
		#
		
		key = (name, type, cls)
		waiting = self._waiting.get(key)
		d = None
		
		if waiting is None:
			self._waiting[key] = []
			
			# 执行查询
			if self.is_tcp:
				d = self.queryTCP([query], timeout)
			else:
				d = self.queryUDP([query], [timeout])
			d.addCallback(self.filterAnswers)
			
			# 当结果返回的时候，发出信号
			def cbResult(result):
				for d in self._waiting.pop(key):
					d.callback(result)
				return result
			
			d.addBoth(cbResult)

		else:
			d = defer.Deferred()
			waiting.append(d)
		
		return d

	# 手工处理 ConnectionLost。
	# 实际上，我觉得这个是 Twisted 的 BUG，忘记实现这个函数。
	def connectionLost(self, p):
		if p in self.connections:
			log.info("与服务器 %s 的 TCP 连接已关闭，因此持久连接被移除。" % self.address)
			try:
				self.connections.remove(p)
			except ValueError:
				pass
		else:
			log.warning("未知 TCP 连接已关闭：%s。这是一个程序错误，请与作者联系。" % p)


