# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：域名匹配类。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

class DomainMapper:
	"""
	这个类的作用是检查传入的 Domain，将其与
	Domain List 中的规则进行比较，并返回匹
	配的规则。
	
	规则匹配如下：
	
	tld -- 精确匹配“tld”这个字符串。
	.tld -- 匹配“tld”，以及“xxx.tld”等所有子域名。
	example.tld -- 精确匹配”example.tld“。
	.example.tld -- 匹配 example.tld，以及所有子域名。
	"""

	def __init__(self, domains):
		# 记录参数
		self._tree = {}
		self._hash = {}
		self._domains = domains
		
		# 计算域名匹配树。
		for d in domains:
			d = d.lower()
			if d == '':
				continue
			
			if d.startswith("."):
				# 匹配 .example.tld
				dd = d[1:]
				if dd == '':
					continue
				# 将 example.tld 加入 hash 表。
				self._hash[dd] = d
				# 填写 tree[tld][example] 的查找树。
				tree = self._tree
				dparts = dd.split('.')
				dparts.reverse()
				for k in dparts:
					if k == '':
						continue
					if k in tree:
						tree = tree[k]
					else:
						tree[k] = {}
						tree = tree[k]
				# 写入匹配信息
				tree['@'] = d
				
			else:
				# 只写入 example.tld
				self._hash[d] = d
				
	def lookup(self, domain):
		domain = domain.lower()
		
		# 查找 hash 表。
		if domain in self._hash:
			return self._hash[domain]
			
		# 查找树。
		dparts = domain.split('.')
		dparts.reverse()
		tree = self._tree
		last_tree = tree
		for k in dparts:
			if k == '':
				continue
			if k in tree:
				tree = tree[k]
				if "@" in tree:
					last_tree = tree
			else:
				break

		if "@" in last_tree:
			return last_tree["@"]
		else:
			return None
		

