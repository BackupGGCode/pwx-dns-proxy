# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器：Resolver 模块。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/9。
"""

class ResolveImmediateFailure(Exception):
	def __init__(self, *args, **kwargs):
		Exception.__init__(self, *args, **kwargs)
