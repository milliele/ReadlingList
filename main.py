# -*- coding: utf-8 -*-

"""
http://blog.csdn.net/chenghit
"""

import wx
import threading
from frames import *
from gui import GuiManager
from util import *
from core import *

class MainAPP(wx.App):

	@debug_name
	def OnInit(self):
		self.manager = GuiManager(self.UpdateUI)
		self.frame = self.manager.GetFrame('initframe', 'INIT')
		self.frame.Show()
		return True

	def UpdateUI(self, name, typ, **kwargs):
		self.frame.Show(False)
		# self.frame.DestroyLater()
		self.frame = self.manager.GetFrame(name, typ, **kwargs)
		self.frame.Show(True)
	#
	# @debug_name
	def MacOpenFile(self, filename):
		if filename.endswith('.rl'):
			# 获得一个db并连接
			filepath = filename
			# parent = event.GetEventObject()
			# is_new = parent.GetName() == 'newdb'
			# if is_new:
			# 	if not filepath.endswith(".rl"):
			# 		filepath += ".rl"
			# 	# import os
			# 	if os.path.exists(filepath):
			# 		res = wx.MessageBox("已存在同名Reading List，是否覆盖？", "Warning", wx.YES_NO | wx.ICON_EXCLAMATION)
			# 		if res == wx.NO:
			# 			event.SkipEvent()
			# 		else:
			# 			os.remove(filepath)
			# 创建连接
			res = core.safe_connect(filepath)
			if res != None:
				wx.MessageBox(u"连接到数据库失败，原因:%s" % res, "Error", wx.OK | wx.CENTRE | wx.ICON_ERROR)
			# 读取主界面需要的数据
			# OpenTable(DB_conn, '123')
			# 切换到主界面
			else:
				self.manager.UpdateUI('mainframe', 'MAIN')


app = MainAPP()
app.MainLoop()

