# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：HOSTS 配置模块。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/9。
"""

from iptest import is_ipv4, is_ipv6
from domains import DomainMapper

class HostsTable:
	"""
	从字符串载入 HOSTS 表。
	
	HOSTS 表只能包含 A 记录和 AAAA 记录。
	"""
	
	def __init__(self, hosts):
		"""
		初始化 HostsTable 的对象。
		
		参数：
		
		hosts -- HOSTS 表的源文件。必须是可迭代
		  的对象（比如 list，还有 file）。
		"""
		
		self._A_table = {}
		self._AAAA_table = {}
		
		for line in hosts:
			# 跳过注释行
			if (line == '' or line.startswith(";")
					or line.startswith("#")):
				continue
			# 获取非空的两个部分
			line = line.replace('\t', ' ')
			parts = line.strip().split(' ')
			host, address = None, None
			for k in parts:
				if k <> '':
					if address is None:
						address = k
					else:
						host = k
						break
			if host is None or address is None:
				continue
			# 检测是 A 记录还是 AAAA 记录
			if is_ipv4(address):
				self._A_table[host] = address
			elif is_ipv6(address):
				self._AAAA_table[host] = address
			# 或者强制返回不存在
			elif address == '-':
				self._A_table[host] = 0
			elif address == '----':
				self._AAAA_table[host] = 0
				
		# 计算查找表。
		self._A_table_mapper = DomainMapper(self._A_table.keys())
		self._AAAA_table_mapper = DomainMapper(self._AAAA_table.keys())
		
	def lookupAddress(self, name):
		"""
		查找 A 记录。
		
		如果没有找到符合 name 的记录，则返回 None。
		"""
		kname = self._A_table_mapper.lookup(name)
		if kname is not None:
			return self._A_table[kname]
		return None
		
	def lookupIPV6Address(self, name):
		"""
		查找 AAAA 记录。
		
		如果没有找到符合 name 的记录，则返回 None。
		"""
		kname = self._AAAA_table_mapper.lookup(name)
		if kname is not None:
			return self._AAAA_table[kname]
		return None
	
