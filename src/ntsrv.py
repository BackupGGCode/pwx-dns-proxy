# -*- encoding: utf-8 -*-

"""
平芜泫 DNS 代理服务器 WINNT 服务程序。

作者：平芜泫（airyai@gmail.com）。
时间：2011/8/8。
"""

# 设置模块寻找路径。
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入 Twisted 模块。
from twisted.application.app import startApplication
from twisted.internet import reactor

# 导入主程序
import dnsproxy

# 建立 WinNT 服务程序框架。
import win32serviceutil, win32service

class PwxDnsProxy(win32serviceutil.ServiceFramework):
	"""NT Service."""

	_svc_name_ = "PwxDnsProxy"
	_svc_display_name_ = "PWX Dns Proxy Server"

	def SvcDoRun(self):
		init_app()
		startApplication(dnsproxy.application, 0)
		reactor.run()

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		reactor.stop()

# 运行例程。
if __name__ == '__main__':
	win32serviceutil.HandleCommandLine(PwxDnsProxy)
