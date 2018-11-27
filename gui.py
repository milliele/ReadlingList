# -*- coding: utf-8 -*-

from registry import FRAMES

class GuiManager():
	def __init__(self, UpdateUI):
		self.UpdateUI = UpdateUI
		self.frameDict = {} # 用来装载已经创建的Frame对象

	def GetFrame(self, name, typ, **kwargs):
		frame = self.frameDict.get(name)

		if frame is None:
			frame = self.CreateFrame(name,typ, **kwargs)
			self.frameDict[name] = frame
		return frame

	def CreateFrame(self, name,typ, **kwargs):
		return FRAMES[typ](None, self, name=name, **kwargs)

	def DestroyFrame(self, name):
		frame = self.frameDict.get(name)
		if frame is not None:
			frame.DestroyLater()
			self.frameDict.pop(name)
