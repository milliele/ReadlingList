# -*- coding: utf-8 -*-

from registry import register_frame
import core
import config
from util import MyGridTable,Markdown2HTML, AutoCompleteComboBox, debug_name
import pic

# 1. 加回调函数
# 2. 加装饰器
# 3. 修改init函数的参数
# 4. 加上更新UI的句子

###########################################################################
## Python code generated with wxFormBuilder (version Nov 15 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid
import wx.html2

import os,os.path

###########################################################################
## Class InitFrame
###########################################################################

@register_frame('INIT')
class InitFrame ( wx.Frame ):

	def __init__( self, parent, guimanager, name, **kwargs):
		self.GUIManager = guimanager

		self.initUI(parent)
		self.SetName(name)

	def initUI(self, parent):
		wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"开始", pos=wx.DefaultPosition, size=wx.Size(370, 135),
						  style=wx.CAPTION | wx.CLOSE_BOX | wx.MAXIMIZE_BOX | wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.Size(370, 135), wx.Size(370, 135))

		bSizer4 = wx.BoxSizer(wx.VERTICAL)

		bSizer4.Add((0, 0), 0, wx.ALL, 5)

		bSizer8 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText6 = wx.StaticText(self, wx.ID_ANY, u"选择已有的Reading List：", wx.DefaultPosition, wx.DefaultSize,
										   0)
		self.m_staticText6.Wrap(-1)

		bSizer8.Add(self.m_staticText6, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.m_filePicker4 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"选择一个Reading List", u"*.rl",
											   wx.DefaultPosition, wx.DefaultSize, wx.FLP_FILE_MUST_EXIST | wx.FLP_OPEN,
											   wx.DefaultValidator, u"existed")
		bSizer8.Add(self.m_filePicker4, 0, wx.ALL, 5)

		bSizer4.Add(bSizer8, 0, wx.ALIGN_CENTER, 5)

		self.m_staticline3 = wx.StaticLine(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL)
		bSizer4.Add(self.m_staticline3, 0, wx.EXPAND | wx.ALL, 5)

		bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText7 = wx.StaticText(self, wx.ID_ANY, u"或者新建一个新Reading List：", wx.DefaultPosition, wx.DefaultSize,
										   0)
		self.m_staticText7.Wrap(-1)

		bSizer6.Add(self.m_staticText7, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.m_filePicker5 = wx.FilePickerCtrl(self, wx.ID_ANY, wx.EmptyString, u"输入Reading List名字", u"*.rl",
											   wx.DefaultPosition, wx.Size(-1, -1),
											   wx.FLP_CHANGE_DIR | wx.FLP_SAVE | wx.FLP_SMALL, wx.DefaultValidator,
											   u"newdb")
		bSizer6.Add(self.m_filePicker5, 0, wx.ALL, 5)

		bSizer4.Add(bSizer6, 1, wx.ALIGN_CENTER_HORIZONTAL, 5)

		bSizer4.Add((0, 0), 0, wx.ALL, 5)

		self.SetSizer(bSizer4)
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.m_filePicker4.Bind(wx.EVT_FILEPICKER_CHANGED, self.InitHandler)
		self.m_filePicker5.Bind(wx.EVT_FILEPICKER_CHANGED, self.InitHandler)

	def __del__(self):
		pass

	# Virtual event handlers, overide them in your derived class
	def InitHandler(self, event):
		# 获得一个db并连接
		filepath = event.GetPath()
		parent = event.GetEventObject()
		is_new = parent.GetName() == 'newdb'
		if is_new:
			if not filepath.endswith(".rl"):
				filepath += ".rl"
			# import os
			if os.path.exists(filepath):
				res = wx.MessageBox("已存在同名Reading List，是否覆盖？","Warning", wx.YES_NO|wx.ICON_EXCLAMATION)
				if res == wx.NO:
					event.SkipEvent()
				else:
					os.remove(filepath)
		# 创建连接
		res = core.safe_connect(filepath)
		if res != None:
			wx.MessageBox(u"连接到数据库失败，原因:%s" % res, "Error", wx.OK|wx.CENTRE|wx.ICON_ERROR)
		# 读取主界面需要的数据
		# OpenTable(DB_conn, '123')
		# 切换到主界面
		else:
			self.GUIManager.UpdateUI('mainframe', 'MAIN')


###########################################################################
## Class MainFrame
###########################################################################
@register_frame('MAIN')
class MainFrame ( wx.Frame ):

	def __init__( self, parent,guimanager, name, **kwargs):
		self.initUI(parent)


		# # 加个右键菜单
		# self.RClickMenu = wx.Menu()
		# self.RClickMenu1 = wx.MenuItem(self.RClickMenu, wx.ID_ANY, u"删除当前分类并将条目移入未分类", wx.EmptyString, wx.ITEM_NORMAL)
		# self.RClickMenu.Append(self.RClickMenu1)
		#
		# self.RClickMenu2 = wx.MenuItem(self.RClickMenu, wx.ID_ANY, u"删除当前分类及所有条目", wx.EmptyString, wx.ITEM_NORMAL)
		# self.RClickMenu.Append(self.RClickMenu2)
		#
		# # Connect Events
		# self.Bind(wx.EVT_MENU, self.OnDeleteClass, id=self.RClickMenu1.GetId())
		# self.Bind(wx.EVT_MENU, self.OnDeleteAll, id=self.RClickMenu2.GetId())
		# self.Classes.Bind(wx.EVT_CONTEXT_MENU, self.OnPoPListBoxMenu)

		self.GUIManager = guimanager
		self.SetName(name)

		# 那些要选中才能有效的按钮
		self.ChooseCell = [
			self.EditPaper,
			self.ViewPaper,
			self.DeletePaper,
			self.SortAsc,
			self.SortDesc,
		]

		map(lambda x:x.Enable(False), self.ChooseCell)

		self.Classes.SetSelection(0)

		# 拖拽
		self.droplisttarget = ListTarget(self.Classes)
		self.Classes.SetDropTarget(self.droplisttarget)

	def getSeletedPaper(self):
		return self.MainGrid.GetCellValue(self.GridSelectedRow, 0)

	def refresh_Grid(self, data):
		gridbase = MyGridTable(data, config.SHORTCUT_4_PAPER)
		self.MainGrid.SetTable(gridbase, takeOwnership=True)
		self.OnSizeChange(None)
		# self.MainGrid.HideCol(0)

	def initUI(self,parent):
		wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Reading List", pos=wx.DefaultPosition,
						  size=wx.Size(749, 492), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

		self.m_toolBar1 = self.CreateToolBar(wx.TB_HORIZONTAL | wx.TB_TEXT, wx.ID_ANY)
		self.m_toolBar1.SetMargins(wx.Size(2, 2))
		self.NewPapaer = self.m_toolBar1.AddTool(wx.ID_ANY, u"添加条目", pic.add.GetBitmap(),
													  wx.NullBitmap, wx.ITEM_NORMAL, u"新建论文条目", wx.EmptyString, None)

		self.EditPaper = self.m_toolBar1.AddTool(wx.ID_ANY, u"编辑条目",
													  pic.edit.GetBitmap(), wx.NullBitmap,
													  wx.ITEM_NORMAL, u"编辑选中条目", wx.EmptyString, None)

		self.ViewPaper = self.m_toolBar1.AddTool(wx.ID_ANY, u"详细信息",
													  pic.view.GetBitmap(), wx.NullBitmap,
													  wx.ITEM_NORMAL, u"查看选中条目详情", wx.EmptyString, None)

		self.DeletePaper = self.m_toolBar1.AddTool(wx.ID_ANY, u"删除条目",
														pic.delete.GetBitmap(), wx.NullBitmap,
														wx.ITEM_NORMAL, u"删除选中条目", wx.EmptyString, None)

		self.m_toolBar1.AddSeparator()

		self.SortAsc = self.m_toolBar1.AddTool(wx.ID_ANY, u"递增排序", pic.asc.GetBitmap(),
													wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

		self.SortDesc = self.m_toolBar1.AddTool(wx.ID_ANY, u"递减排序", pic.desc.GetBitmap(),
													 wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString,
													 None)

		self.UnSort = self.m_toolBar1.AddTool(wx.ID_ANY, u"清除排序", pic.NoSort.GetBitmap(),
												   wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

		self.m_toolBar1.AddSeparator()

		self.SearchCtrl = wx.SearchCtrl(self.m_toolBar1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
										0)
		self.SearchCtrl.ShowSearchButton(True)
		self.SearchCtrl.ShowCancelButton(True)
		self.m_toolBar1.AddControl(self.SearchCtrl)
		self.m_toolBar1.Realize()

		bSizer6 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_splitter5 = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.SP_LIVE_UPDATE)
		self.m_splitter5.Bind(wx.EVT_IDLE, self.m_splitter5OnIdle)

		self.m_panel5 = wx.Panel(self.m_splitter5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
		bSizer7 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText4 = wx.StaticText(self.m_panel5, wx.ID_ANY, u"分类", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText4.Wrap(-1)

		bSizer7.Add(self.m_staticText4, 0, wx.ALL, 5)

		ClassesChoices = [u"全部", u"未分类"]
		self.Classes = wx.ListBox(self.m_panel5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ClassesChoices,
								  wx.LB_SINGLE)
		bSizer7.Add(self.Classes, 3, wx.EXPAND, 5)

		self.m_panel5.SetSizer(bSizer7)
		self.m_panel5.Layout()
		bSizer7.Fit(self.m_panel5)
		self.m_panel6 = wx.Panel(self.m_splitter5, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
		bSizer8 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText6 = wx.StaticText(self.m_panel6, wx.ID_ANY, u"条目", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText6.Wrap(-1)

		bSizer8.Add(self.m_staticText6, 0, wx.ALL, 5)

		self.MainGrid = wx.grid.Grid(self.m_panel6, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
									 wx.HSCROLL | wx.VSCROLL)

		# Grid
		self.MainGrid.CreateGrid(5, 6)
		self.MainGrid.EnableEditing(False)
		self.MainGrid.EnableGridLines(True)
		self.MainGrid.EnableDragGridSize(False)
		self.MainGrid.SetMargins(0, 0)

		# Columns
		self.MainGrid.EnableDragColMove(True)
		self.MainGrid.EnableDragColSize(False)
		self.MainGrid.SetColLabelSize(30)
		self.MainGrid.SetColLabelValue(0, u"时间")
		self.MainGrid.SetColLabelValue(1, u"会议/期刊")
		self.MainGrid.SetColLabelValue(2, u"等级")
		self.MainGrid.SetColLabelValue(3, u"被引量")
		self.MainGrid.SetColLabelValue(4, u"参考文献量")
		self.MainGrid.SetColLabelValue(5, u"标题")
		self.MainGrid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

		# Rows
		self.MainGrid.EnableDragRowSize(False)
		self.MainGrid.SetRowLabelSize(0)
		self.MainGrid.SetRowLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

		# Label Appearance

		# Cell Defaults
		self.MainGrid.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER)
		bSizer8.Add(self.MainGrid, 3, wx.ALL | wx.EXPAND, 5)

		self.m_panel6.SetSizer(bSizer8)
		self.m_panel6.Layout()
		bSizer8.Fit(self.m_panel6)
		self.m_splitter5.SplitVertically(self.m_panel5, self.m_panel6, 100)
		bSizer6.Add(self.m_splitter5, 1, wx.EXPAND, 5)

		self.SetSizer(bSizer6)
		self.Layout()
		self.m_menubar1 = wx.MenuBar(0)
		self.File = wx.Menu()
		self.Open = wx.MenuItem(self.File, wx.ID_ANY, u"打开" + u"\t" + u"ctrl+O", wx.EmptyString, wx.ITEM_NORMAL)
		self.File.Append(self.Open)

		self.New = wx.Menu()
		self.NewEntry = wx.MenuItem(self.New, wx.ID_ANY, u"条目" + u"\t" + u"alt+ctrl+N", wx.EmptyString, wx.ITEM_NORMAL)
		self.New.Append(self.NewEntry)

		self.NewFile = wx.MenuItem(self.New, wx.ID_ANY, u"Reading List" + u"\t" + u"ctrl+N", wx.EmptyString,
								   wx.ITEM_NORMAL)
		self.New.Append(self.NewFile)

		self.File.AppendSubMenu(self.New, u"新建")

		self.m_menubar1.Append(self.File, u"文件")

		self.Edit = wx.Menu()
		self.EditEntry = wx.MenuItem(self.Edit, wx.ID_ANY, u"编辑条目" + u"\t" + u"ctrl+E", wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.EditEntry)

		self.DeleteEntry = wx.MenuItem(self.Edit, wx.ID_ANY, u"删除条目" + u"\t" + u"ctrl+D", wx.EmptyString,
									   wx.ITEM_NORMAL)
		self.Edit.Append(self.DeleteEntry)

		self.Edit.AppendSeparator()

		self.DeleteClassItem = wx.MenuItem(self.Edit, wx.ID_ANY, u"删除当前分类并将条目移入未分类" + u"\t" + u"ctrl+alt+D",
										   wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.DeleteClassItem)

		self.DeleteClassAllItem = wx.MenuItem(self.Edit, wx.ID_ANY, u"删除当前分类及所有条目" + u"\t" + u"ctrl+alt+shift+D",
											  wx.EmptyString, wx.ITEM_NORMAL)
		self.Edit.Append(self.DeleteClassAllItem)

		self.m_menubar1.Append(self.Edit, u"编辑")

		self.View = wx.Menu()
		self.ViewEntry = wx.MenuItem(self.View, wx.ID_ANY, u"查看详细", wx.EmptyString, wx.ITEM_NORMAL)
		self.View.Append(self.ViewEntry)

		self.ViewReadingListItem = wx.MenuItem(self.View, wx.ID_ANY, u"查看Reading List" + u"\t" + u"ctrl+shift+L",
											   wx.EmptyString, wx.ITEM_NORMAL)
		self.View.Append(self.ViewReadingListItem)

		self.View.AppendSeparator()

		self.ToHomePageItem = wx.MenuItem(self.View, wx.ID_ANY, u"打开主页" + u"\t" + u"ctrl+shift+H", wx.EmptyString,
										  wx.ITEM_NORMAL)
		self.View.Append(self.ToHomePageItem)

		self.ToScholarSearch = wx.MenuItem(self.View, wx.ID_ANY, u"使用谷歌学术搜索当前条目" + u"\t" + u"ctrl+S", wx.EmptyString,
										   wx.ITEM_NORMAL)
		self.View.Append(self.ToScholarSearch)

		self.View.AppendSeparator()

		self.Export = wx.Menu()
		self.Export_MarkDown = wx.MenuItem(self.Export, wx.ID_ANY, u"导出为MarkDown文件" + u"\t" + u"Ctrl+B", wx.EmptyString,
										   wx.ITEM_NORMAL)
		self.Export.Append(self.Export_MarkDown)

		self.ExportHTML = wx.MenuItem(self.Export, wx.ID_ANY, u"导出为HTML文件" + u"\t" + u"alt+ctrl+B", wx.EmptyString,
									  wx.ITEM_NORMAL)
		self.Export.Append(self.ExportHTML)

		self.View.AppendSubMenu(self.Export, u"导出")

		self.m_menubar1.Append(self.View, u"查看")

		self.Help = wx.Menu()
		self.NoHelp = wx.MenuItem(self.Help, wx.ID_ANY, u"没有帮助", wx.EmptyString, wx.ITEM_NORMAL)
		self.Help.Append(self.NoHelp)

		self.m_menubar1.Append(self.Help, u"帮助")

		self.SetMenuBar(self.m_menubar1)

		self.Centre(wx.BOTH)

		# Connect Events
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		self.Bind(wx.EVT_SHOW, self.OnShow)
		self.Bind(wx.EVT_TOOL, self.OnCreateEntry, id=self.NewPapaer.GetId())
		self.Bind(wx.EVT_TOOL, self.OnEditEntry, id=self.EditPaper.GetId())
		self.Bind(wx.EVT_TOOL, self.OnViewEntry, id=self.ViewPaper.GetId())
		self.Bind(wx.EVT_TOOL, self.OnDeleteEntry, id=self.DeletePaper.GetId())
		self.Bind(wx.EVT_TOOL, self.OnSortAsc, id=self.SortAsc.GetId())
		self.Bind(wx.EVT_TOOL, self.OnSortDesc, id=self.SortDesc.GetId())
		self.Bind(wx.EVT_TOOL, self.OnUnSort, id=self.UnSort.GetId())
		self.SearchCtrl.Bind(wx.EVT_SEARCHCTRL_CANCEL_BTN, self.OnSearchCancel)
		self.SearchCtrl.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnContentSearch)
		self.Classes.Bind(wx.EVT_LEFT_DCLICK, self.OnListBeginDrag)
		self.Classes.Bind(wx.EVT_LISTBOX, self.OnChooseClass)
		self.MainGrid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnViewEntry)
		self.MainGrid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.OnPoPMenu)
		self.MainGrid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.ActivateEntry)
		self.MainGrid.Bind(wx.EVT_SIZE, self.OnSizeChange)
		self.Bind(wx.EVT_MENU, self.ReOpen, id=self.Open.GetId())
		self.Bind(wx.EVT_MENU, self.OnCreateEntry, id=self.NewEntry.GetId())
		self.Bind(wx.EVT_MENU, self.OnNewFile, id=self.NewFile.GetId())
		self.Bind(wx.EVT_MENU, self.OnEditEntry, id=self.EditEntry.GetId())
		self.Bind(wx.EVT_MENU, self.OnDeleteEntry, id=self.DeleteEntry.GetId())
		self.Bind(wx.EVT_MENU, self.MenuDeleteClass, id=self.DeleteClassItem.GetId())
		self.Bind(wx.EVT_MENU, self.MenuDeleteAll, id=self.DeleteClassAllItem.GetId())
		self.Bind(wx.EVT_MENU, self.OnViewEntry, id=self.ViewEntry.GetId())
		self.Bind(wx.EVT_MENU, self.OnViewRL, id=self.ViewReadingListItem.GetId())
		self.Bind(wx.EVT_MENU, self.ToHomePage, id=self.ToHomePageItem.GetId())
		self.Bind(wx.EVT_MENU, self.ScholarSearch, id=self.ToScholarSearch.GetId())
		self.Bind(wx.EVT_MENU, self.OnExportMD, id=self.Export_MarkDown.GetId())
		self.Bind(wx.EVT_MENU, self.OnExportHTML, id=self.ExportHTML.GetId())

	def __del__(self):
		pass

	# Virtual event handlers, overide them in your derived class
	def OnListBeginDrag(self, event):
		index = self.Classes.HitTest(event.GetPosition())
		# print index
		if index != wx.NOT_FOUND:
			import json
			my_data = wx.TextDataObject(
				json.dumps({'type': 'list', 'content': self.Classes.GetString(index)}))
			dragSource = wx.DropSource(self)
			dragSource.SetData(my_data)
			result = dragSource.DoDragDrop(True)
			if result == wx.DragCopy:
				if self.Classes.GetSelection() == 0:
					# print 'tr'
					self.refresh_Grid(core.Get_Class_Data(None, self.Classes.GetItems()))
				return None
		event.Skip()

	def OnSizeChange(self, event):
		colwid = self.MainGrid.GetSize().GetWidth()/(len(config.SHORTCUT_4_PAPER)+2)
		# print colwid
		arr = [colwid if k!='title' else colwid*4 for k in config.SHORTCUT_4_PAPER]
		if len(arr):
			arr[0] = 0
		# self.MainGrid.GetTable().SetWid(colwid*4)
		self.MainGrid.SetColSizes(wx.grid.GridSizesInfo(30, arr))

	def ReOpen(self, event):
		# otherwise ask the user what new file to open
		with wx.FileDialog(self, u"选择一个Reading List", wildcard=u"*.rl",
						   style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return  # the user changed their mind

			# Proceed loading the file chosen by the user
			pathname = fileDialog.GetPath()
			self.Close()
			frame = self.GUIManager.GetFrame('initframe', 'INIT')
			frame.m_filePicker4.SetPath(pathname)
			evt = wx.FileDirPickerEvent(wx.FileDirPickerEvent, None, frame.m_filePicker4.GetId(), pathname)
			frame.GetEventHandler().ProcessEvent(evt)

	def OnNewFile(self, event):
		with wx.FileDialog(self, u"输入Reading List名字", wildcard=u"*.rl",
						   style=wx.FD_SAVE) as fileDialog:

			if fileDialog.ShowModal() == wx.ID_CANCEL:
				return  # the user changed their mind

			# Proceed loading the file chosen by the user
			pathname = fileDialog.GetPath()
			self.Close()
			frame = self.GUIManager.GetFrame('initframe', 'INIT')
			frame.m_filePicker5.SetPath(pathname)

	def MenuDeleteClass(self, event):
		self.DeleteClass(self.Classes.GetString(self.Classes.GetSelection()))

	def MenuDeleteAll(self, event):
		self.DeleteAll(self.Classes.GetString(self.Classes.GetSelection()))

	def ToHomePage(self, event):
		paperid = self.getSeletedPaper()
		if paperid == -1:
			return None
		url = core.Get_Paper_Addr(paperid)
		if url != None:
			import webbrowser
			webbrowser.open(url)

	def ScholarSearch(self, event):
		paperid = self.getSeletedPaper()
		if paperid == -1:
			return None
		import webbrowser
		webbrowser.open(
			"""https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%%2C5&q=%s&btnG=""" %
		core.Get_Paper_Title(paperid))

	def AbleToDelete(self, cls):
		if cls == wx.NOT_FOUND:
			return False
		return cls!=u'全部' and cls!=u'未分类'

	def DeleteClass(self, cls):
		# print self.Classes.GetFirstSelected()
		# cls = self.Classes.GetString(self.Classes.GetSelection())
		if not self.AbleToDelete(cls):
			return None
		# print 'delete', cls
		res = core.Set_Papers_Attr(core.Get_Ids('papers','class',cls), 'class', "")
		if res == "":
			res = core.Delete_Table_Item('list_class', 'name', cls)
			if res != "":
				res = "删除分类时: " + res
			else:
				self.Classes.SetSelection(0)
				self.GUIManager.UpdateUI('mainframe', 'MAIN')
				return None
		if res != "":
			wx.MessageBox("删除分类失败！原因:%s" % res, "确认")

	def DeleteAll(self, cls):
		# cls = self.Classes.GetString(self.Classes.GetSelection())
		if not self.AbleToDelete(cls):
			return None
		# print 'delete',cls
		res = core.Delete_Table_Item('papers','class',cls)
		if res == "":
			res = core.Delete_Table_Item('list_class', 'name', cls)
			if res != "":
				res = "删除分类时: " + res
			else:
				self.Classes.SetSelection(0)
				self.GUIManager.UpdateUI('mainframe', 'MAIN')
				return None
		if res != "":
			wx.MessageBox("删除分类失败！原因:%s" % res, "确认")

	def OnSortAsc(self, event):
		# print 'in'
		self.MainGrid.GetTable().Sort(self.GridSelectedCol)
		self.OnSizeChange(None)

	def OnSortDesc(self, event):
		# print 'in'
		self.MainGrid.GetTable().Sort(self.GridSelectedCol, False)
		self.OnSizeChange(None)

	def OnUnSort(self, event):
		self.MainGrid.GetTable().UnSort()
		self.OnSizeChange(None)

	def OnClose(self, event):
		lists = self.Classes.GetItems()
		core.Set_Class_Sort(lists)
		core.DB_conn.close()
		self.GUIManager.DestroyFrame(self.GetName())
		self.GUIManager.UpdateUI('initframe', 'INIT')

	def Screen_Class_Data(self, choice):
		search = self.SearchCtrl.GetValue()
		# print search

		if choice == u'全部':
			return core.Get_Class_Data(None, self.Classes.GetItems()[1:-1], search=search)
		else:
			return core.Get_Class_Data(choice, search=search)

	def OnShow(self, event):
		if not event.IsShown():
			event.Skip()
			return None

		# 更新选择Box
		classes = core.Get_Lists('list_class')
		oldchoice = self.Classes.GetString(self.Classes.GetSelection())
		# print 'classes=', classes
		# print 'oldchoice=', oldchoice
		self.Classes.SetItems([u'全部']+classes+[u'未分类'])
		self.Classes.SetSelection(self.Classes.FindString(oldchoice))

		# 更新Grid
		data = self.Screen_Class_Data(oldchoice)
		# print data
		self.refresh_Grid(data)

	# Virtual event handlers, overide them in your derived class
	def OnCreateEntry(self, event):
		frame = self.GUIManager.CreateFrame('newpaper', 'EDIT')
		frame.Show(True)

	def OnEditEntry(self, event):
		# 获得现在选中的行的paperid
		paperid = self.getSeletedPaper()
		# print str(paperid)
		frame = self.GUIManager.CreateFrame('Edit-%s' % str(paperid), 'EDIT', id=paperid)
		frame.Show(True)

	def OnViewEntry(self, event):
		# 获得现在选中的行的paperid
		paperid = self.getSeletedPaper()
		frame = self.GUIManager.CreateFrame('View-%s' % str(paperid), 'EDIT', id=paperid, readonly=True)
		frame.Show(True)

	# def OnPoPListBoxMenu(self, event):
	# 	# print wx.DefaultPosition
	# 	# item = self.Classes.HitTest(wx.DefaultPosition)
	# 	# print item
	# 	print self.Classes.HitTest(event.GetPosition())
	# 	self.PopupMenu(self.RClickMenu)

	def OnPoPMenu(self, event):
		event.Skip()

	def OnChooseClass(self, event):
		# print 'choos'
		cls = self.Classes.GetString(self.Classes.GetSelection())
		# print cls
		self.refresh_Grid(self.Screen_Class_Data(cls))

	def OnDeleteEntry(self, event):
		# 获得现在选中的行的paperid
		paperid = self.getSeletedPaper()
		# 写入数据库
		res = core.Delete_Table_Item('papers', 'id', str(paperid))
		if res == "":
			# wx.MessageBox(u"%s成功！" % u"新建" if self.id==None else u"修改",u"确认")
			self.GUIManager.UpdateUI('mainframe', 'MAIN')
			# self.GUIManager.DestroyFrame(self.GetName())
		else:
			wx.MessageBox("%s失败！原因:%s" % ("新建" if self.id == None else "修改", res), "确认")

	def OnSearchCancel(self, event):
		self.GUIManager.UpdateUI('mainframe', 'MAIN')

	def OnContentSearch(self, event):
		self.GUIManager.UpdateUI('mainframe', 'MAIN')


	def ActivateEntry(self, event):
		# print self.MainGrid.GetSize()
		self.GridSelectedRow = event.GetRow()
		self.GridSelectedCol = event.GetCol()
		map(lambda x: x.Enable(True) if not x.IsEnabled() else None, self.ChooseCell)
		event.Skip()

		import json
		my_data = wx.TextDataObject(json.dumps({'type': 'grid', 'content': self.getSeletedPaper()}))
		dragSource = wx.DropSource(self)
		dragSource.SetData(my_data)
		result = dragSource.DoDragDrop(wx.Drag_AllowMove|wx.Drag_DefaultMove)
		# print 'res=', result
		# print wx.DragError,wx.DragNone, wx.DragCopy, wx.DragMove, wx.DragLink, wx.DragCancel
		if result==wx.DragCopy:
			self.GUIManager.UpdateUI('mainframe','MAIN')

	def OnExportMD(self, event):
		try:
			classes = self.Classes.GetItems()
			# import os.path
			filename = os.path.join(core.Working_Dir, core.Project_Name+'.md')
			# print filename
			# with open(filename, "w") as fobj:
			# 	fobj.write("[TOC]\n")
			for cls in classes[1:]:
				raw_list = core.Get_Class_Data(cls, None, True)
				if len(raw_list):
					with open(filename, "a+") as fobj:
						fobj.write("\n# %s\n" % cls.encode('utf-8'))
					for paper in raw_list:
						with open(filename, "a+") as fobj:
							fobj.write("\n%s\n" % core.Single_Paper_MarkDown(paper))
			wx.MessageBox(u'成功导出MarkDown文件到：%s' % filename, u"提示")
		except Exception,e:
			wx.MessageBox(u'导出MarkDown文件失败，原因为：%s' % unicode(str(e)),u"Warning")

	def OnExportHTML(self, event):
		try:
			classes = self.Classes.GetItems()
			# import os, os.path
			filename = os.path.join(core.Working_Dir, "."+core.Project_Name+'.md')
			# print filename
			with open(filename, "w") as fobj:
				fobj.write("[TOC]\n")
			for cls in classes[1:]:
				raw_list = core.Get_Class_Data(cls, None, True)
				if len(raw_list):
					with open(filename, "a+") as fobj:
						fobj.write("\n# %s\n" % cls.encode('utf-8'))
					for paper in raw_list:
						with open(filename, "a+") as fobj:
							fobj.write("\n%s\n" % core.Single_Paper_MarkDown(paper))
			realfile = os.path.join(core.Working_Dir, ("%s" % '.' if event == None else "")+core.Project_Name+'.html')
			result = Markdown2HTML(filename).encode('utf-8')
			os.remove(filename)
			with open(realfile,"w") as wobj:
					wobj.write(result)
					if event is not None:
						wx.MessageBox(u'成功导出HTML文件到：%s' % realfile, u"提示")
					else:
						return realfile
		except Exception,e:
			wx.MessageBox('导出HTML文件失败，原因为：%s' % str(e),u"Warning")

	def OnViewRL(self, event):
		# print filename
		import os,os.path
		frame = self.GUIManager.CreateFrame('browser', 'BROWSER', filename = self.OnExportHTML(None))
		# frame.HTMLWindow.LoadURL(filename)
		frame.Show(True)
		# os.remove(filename)

	def m_splitter5OnIdle(self, event):
		self.m_splitter5.SetSashPosition(100)
		self.m_splitter5.Unbind(wx.EVT_IDLE)

###########################################################################
## Class EditFrame
###########################################################################
@register_frame('EDIT')
class EditFrame ( wx.Frame ):

	def __init__(self, parent, guimanager, name,  id=None, readonly=False, **kwargs):
		self.initUI(parent)
		self.GUIManager = guimanager

		self.inputs = {
			'title': self.Titile,
			'class': self.Class,
			'conference': self.Conference,
			'type': self.Type,
			'time': self.Time,
			'database': self.Database,
			'dbid': self.DBID,
			'refnum': self.RefNum,
			'beref': self.BeRef,
			'main': self.MainContent,
			'reference': self.WordRef,
			'bibtex': self.BibRef,
		}
		for k in config.COMBOBOXES:
			self.inputs[k].SetIgnoreCase(True)

		self.id = id
		self.readonly = readonly
		self.DataInject()
		if readonly:
			self.EditButtonsOK.Hide()
			self.EditButtonsCancel.Hide()
		else:
			self.ReadonlyTool.Hide()
		self.SetSize(self.GetBestSize())
		self.SetName(name)

	def DataInject(self):
		# 先初始化
		# 设置一下时间的范围
		import datetime
		year = datetime.datetime.now().year
		self.inputs['time'].SetMax(year)
		# ComboBox选项初始化
		for k in config.COMBOBOXES:
			# 更新选择Box
			lists = core.Get_Lists('list_%s' % k)
			# oldchoice = self.inputs[k].GetStringSelection()
			# print '%s=' % k, lists
			self.inputs[k].SetChoices(lists)
			self.inputs[k].SetSelection(wx.NOT_FOUND)

		if self.id != None:
			self.data = core.Get_Paper_Data(self.id)
			# print self.data
			for k in self.inputs:
				# print k, self.data[k]
				if isinstance(self.inputs[k], AutoCompleteComboBox):
					self.inputs[k].SafeSetChoice(self.data[k])
				else:
					self.inputs[k].SetValue(self.data[k])
				if self.readonly:
					self.inputs[k].Disable()
		else:
			self.inputs['time'].SetValue(year)
		return False

	def initUI(self, parent):
		wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"编辑条目", pos=wx.DefaultPosition, size=wx.Size(680, 344),
						  style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

		self.SetSizeHints(wx.Size(680, 344), wx.DefaultSize)

		self.ReadonlyTool = self.CreateToolBar(wx.TB_HORIZONTAL | wx.TB_TEXT, wx.ID_ANY)
		self.EditPaper = self.ReadonlyTool.AddLabelTool(wx.ID_ANY, u"编辑文章",
														pic.edit.GetBitmap(), wx.NullBitmap,
														wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

		self.OpenHomePage = self.ReadonlyTool.AddLabelTool(wx.ID_ANY, u"打开主页",
														   pic.home.GetBitmap(),
														   wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString,
														   wx.EmptyString, None)

		self.Search = self.ReadonlyTool.AddLabelTool(wx.ID_ANY, u"学术搜索", pic.view.GetBitmap(),
													 wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString,
													 None)

		self.ReadonlyTool.Realize()

		bSizer9 = wx.BoxSizer(wx.VERTICAL)

		bSizer9.Add((0, 5), 0, wx.EXPAND, 5)

		bSizer12 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText171 = wx.StaticText(self, wx.ID_ANY, u"标题：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText171.Wrap(-1)

		bSizer12.Add(self.m_staticText171, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.Titile = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer12.Add(self.Titile, 1, wx.ALL | wx.EXPAND, 5)

		self.m_staticText151 = wx.StaticText(self, wx.ID_ANY, u"分类：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText151.Wrap(-1)

		bSizer12.Add(self.m_staticText151, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		ClassChoices = []
		self.Class = AutoCompleteComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, ClassChoices, 0)
		bSizer12.Add(self.Class, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		bSizer9.Add(bSizer12, 1, wx.EXPAND, 5)

		bSizer17 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText17 = wx.StaticText(self, wx.ID_ANY, u"会议/期刊：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText17.Wrap(-1)

		bSizer17.Add(self.m_staticText17, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		ConferenceChoices = []
		self.Conference = AutoCompleteComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
									  ConferenceChoices, 0)
		bSizer17.Add(self.Conference, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		bSizer17.Add((30, 0), 0, 0, 5)

		self.m_staticText18 = wx.StaticText(self, wx.ID_ANY, u"类型：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText18.Wrap(-1)

		bSizer17.Add(self.m_staticText18, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		TypeChoices = []
		self.Type = AutoCompleteComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, TypeChoices, 0)
		bSizer17.Add(self.Type, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		bSizer17.Add((30, 0), 0, 0, 5)

		self.m_staticText19 = wx.StaticText(self, wx.ID_ANY, u"时间：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText19.Wrap(-1)

		bSizer17.Add(self.m_staticText19, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.Time = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
								wx.SP_ARROW_KEYS | wx.SP_WRAP, 0, 10, 0)
		bSizer17.Add(self.Time, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		bSizer9.Add(bSizer17, 1, wx.EXPAND, 5)

		bSizer171 = wx.BoxSizer(wx.HORIZONTAL)

		self.m_staticText20 = wx.StaticText(self, wx.ID_ANY, u"数据库：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText20.Wrap(-1)

		bSizer171.Add(self.m_staticText20, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		DatabaseChoices = []
		self.Database = AutoCompleteComboBox(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(100, -1),
									DatabaseChoices, 0)
		bSizer171.Add(self.Database, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.m_staticText21 = wx.StaticText(self, wx.ID_ANY, u"ID：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText21.Wrap(-1)

		bSizer171.Add(self.m_staticText21, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.DBID = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
		bSizer171.Add(self.DBID, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.m_staticText15 = wx.StaticText(self, wx.ID_ANY, u"被引量：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText15.Wrap(-1)

		bSizer171.Add(self.m_staticText15, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.BeRef = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(60, -1),
								 wx.SP_ARROW_KEYS | wx.SP_WRAP, 0, 10000, 0)
		bSizer171.Add(self.BeRef, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.m_staticText16 = wx.StaticText(self, wx.ID_ANY, u"参考文献数量：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText16.Wrap(-1)

		bSizer171.Add(self.m_staticText16, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		self.RefNum = wx.SpinCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size(50, -1),
								  wx.SP_ARROW_KEYS | wx.SP_WRAP, 0, 500, 0)
		bSizer171.Add(self.RefNum, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5)

		bSizer9.Add(bSizer171, 1, wx.EXPAND, 5)

		bSizer16 = wx.BoxSizer(wx.HORIZONTAL)

		bSizer9.Add(bSizer16, 1, wx.EXPAND, 5)

		self.m_staticText8 = wx.StaticText(self, wx.ID_ANY, u"主要内容：", wx.DefaultPosition, wx.DefaultSize, 0)
		self.m_staticText8.Wrap(-1)

		bSizer9.Add(self.m_staticText8, 0, wx.ALIGN_CENTER_VERTICAL | wx.TOP | wx.LEFT, 5)

		self.MainContent = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
									   wx.TE_MULTILINE)
		self.MainContent.SetMinSize(wx.Size(-1, 100))

		bSizer9.Add(self.MainContent, 3, wx.ALL | wx.EXPAND, 5)

		self.BibtexCtrl = wx.CollapsiblePane(self, wx.ID_ANY, u"Reference：", wx.DefaultPosition, wx.DefaultSize,
											 wx.CP_DEFAULT_STYLE)
		self.BibtexCtrl.Collapse(True)

		bSizer13 = wx.BoxSizer(wx.VERTICAL)

		self.m_staticText81 = wx.StaticText(self.BibtexCtrl.GetPane(), wx.ID_ANY, u"文字引用：", wx.DefaultPosition,
											wx.DefaultSize, 0)
		self.m_staticText81.Wrap(-1)

		bSizer13.Add(self.m_staticText81, 0, wx.ALL, 5)

		self.WordRef = wx.TextCtrl(self.BibtexCtrl.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
								   wx.Size(-1, 50), wx.TE_MULTILINE)
		bSizer13.Add(self.WordRef, 0, wx.ALL | wx.EXPAND, 5)

		self.m_staticText811 = wx.StaticText(self.BibtexCtrl.GetPane(), wx.ID_ANY, u"Bibtex：", wx.DefaultPosition,
											 wx.DefaultSize, 0)
		self.m_staticText811.Wrap(-1)

		bSizer13.Add(self.m_staticText811, 0, wx.ALL, 5)

		self.BibRef = wx.TextCtrl(self.BibtexCtrl.GetPane(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
								  wx.Size(-1, 50), wx.TE_MULTILINE)
		bSizer13.Add(self.BibRef, 0, wx.ALL | wx.EXPAND, 5)

		self.BibtexCtrl.GetPane().SetSizer(bSizer13)
		self.BibtexCtrl.GetPane().Layout()
		bSizer13.Fit(self.BibtexCtrl.GetPane())
		bSizer9.Add(self.BibtexCtrl, 0, wx.ALL | wx.EXPAND, 5)

		EditButtons = wx.StdDialogButtonSizer()
		self.EditButtonsOK = wx.Button(self, wx.ID_OK)
		EditButtons.AddButton(self.EditButtonsOK)
		self.EditButtonsCancel = wx.Button(self, wx.ID_CANCEL)
		EditButtons.AddButton(self.EditButtonsCancel)
		EditButtons.Realize();

		bSizer9.Add(EditButtons, 1, wx.EXPAND, 5)

		self.SetSizer(bSizer9)
		self.Layout()

		self.Centre(wx.BOTH)

		# Connect Events
		self.Bind(wx.EVT_TOOL, self.OnEditPaper, id=self.EditPaper.GetId())
		self.Bind(wx.EVT_TOOL, self.OnOpenHome, id=self.OpenHomePage.GetId())
		self.Bind(wx.EVT_TOOL, self.OnSearch, id=self.Search.GetId())
		self.Conference.Bind(wx.EVT_KILL_FOCUS, self.OnConfCompleteType)
		self.EditButtonsCancel.Bind(wx.EVT_BUTTON, self.EditCancel)
		self.EditButtonsOK.Bind(wx.EVT_BUTTON, self.EditOK)

	def __del__(self):
		pass

	# Virtual event handlers, overide them in your derived class
	def OnEditPaper(self, event):
		self.readonly = False
		for k in self.inputs:
			self.inputs[k].Enable()
		self.EditButtonsOK.Show()
		self.EditButtonsCancel.Show()
		self.ReadonlyTool.Hide()
		self.SetSize(self.GetBestSize())

	def OnOpenHome(self, event):
		format = config.HOMEPAGE_FORMAT.get(self.data['database'])
		if format and self.data['dbid']!="":
			import webbrowser
			webbrowser.open( format % self.data['dbid'])

	def OnSearch(self, event):
		import webbrowser
		webbrowser.open("""https://scholar.google.com.hk/scholar?hl=zh-CN&as_sdt=0%%2C5&q=%s&btnG=""" % self.data['title'])

	# @debug_name
	def OnConfCompleteType(self, event):
		conf = self.Conference.GetValue().upper()
		if conf in config.DATABASE_ASSOSIATE:
			self.Database.SafeSetChoice(config.DATABASE_ASSOSIATE[conf])
				# self.Database.SetValue(db)
		event.Skip()

	# Virtual event handlers, overide them in your derived class
	def EditCancel(self, event):
		self.Close()

	def EditOK(self, event):
		# 获取输入
		newdata = {}
		is_new = {}
		for k in self.inputs:
			value = self.inputs[k].GetValue()
			if hasattr(self, 'data') and self.data[k] == value:
				continue
			newdata[k] = value
			# if isinstance(self.inputs[k], AutoCompleteComboBox) and self.inputs[k].GetValue()!="":
			# 	if k != 'class':
			# 		newdata[k] = newdata[k].upper()
			# 	is_new[k] = self.inputs[k].GetCurrentSelection()==wx.NOT_FOUND
			# 	# print k, is_new[k]
		# 检查输入
		# 	是否合法
		is_ok = True
		if 'title' in newdata and newdata['title'] == "":
			wx.MessageBox(u"标题不能为空!", "Warn", wx.OK | wx.CENTRE | wx.ICON_EXCLAMATION)
			is_ok = False
		if 'dbid' in newdata and newdata['dbid']!='' and not newdata['dbid'].isdigit():
			wx.MessageBox(u"数据库ID必须是全数字!", "Warn", wx.OK|wx.CENTRE|wx.ICON_EXCLAMATION)
			is_ok = False

		if is_ok:
			# 写入数据库
			res = core.Set_Paper_Data(self.id, newdata)
			if res == "":
				for k in config.COMBOBOXES:
					if k in newdata:
						res2 = core.Set_List("list_%s" % k, newdata[k])
						if res2!="":
							res += ("更新类名%s: %s\n" % k, res2)
				if res != "":
					wx.MessageBox("%s有问题！原因:%s" % ("新建" if self.id == None else "修改", res), "Warning", wx.OK|wx.CENTRE|wx.ICON_EXCLAMATION)
				self.Hide()
				self.GUIManager.UpdateUI('mainframe', 'MAIN')
				self.GUIManager.DestroyFrame(self.GetName())
			else:
				wx.MessageBox("%s失败！原因:%s" % ("新建" if self.id == None else "修改", res), "Error", wx.OK|wx.CENTRE|wx.ICON_ERROR)


@register_frame('BROWSER')
class BrowserFrame ( wx.Frame ):

	def __init__(self, parent, guimanager, name, filename="",  **kwargs):
		self.initUI(parent)
		self.GUIManager = guimanager
		self.filename = filename
		self.HTMLWindow.LoadURL(os.path.realpath(self.filename))
		# self.SetSize(self.GetBestSize())
		self.SetName(name)

	def initUI(self, parent):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"预览", pos = wx.DefaultPosition, size = wx.Size( 784,558 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer14 = wx.BoxSizer( wx.VERTICAL )

		self.HTMLWindow = wx.html2.WebView.New(self)
		bSizer14.Add( self.HTMLWindow, 3, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer14 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.Bind(wx.EVT_CLOSE, self.OnClose )

	def __del__( self ):
		pass

	def OnClose(self,event):
		if os.path.exists(self.filename):
			os.remove(self.filename)
		event.Skip()

class ListTarget(wx.TextDropTarget):

	def __init__(self, object):
		wx.TextDropTarget.__init__(self)
		self.__object = object

	def IsInValid(self,string):
		return string == u'全部' or string == u'未分类'

	def OnDropText(self, x, y, data):
		# print 'in'
		target_id = self.__object.HitTest(x,y)
		if target_id == wx.NOT_FOUND:
			return False
		target = self.__object.GetString(self.__object.HitTest(x,y))
		if self.IsInValid(target):
			return False
		# print data
		import json
		data = json.loads(data[:data.find('}') + 1])
		if data['type'] == 'list':
			begin = data['content']
			# print begin
			if self.IsInValid(begin):
				return False
			index = self.__object.FindString(target)
			oldchoice = self.__object.GetString(self.__object.GetSelection())
			# print oldchoice
			lists = self.__object.GetItems()
			if index<0 or index>len(lists):
				return False
			# print lists
			lists.remove(begin)
			# print lists
			lists.insert(index,begin)
			# print lists
			self.__object.SetItems(lists)
			self.__object.SetSelection(self.__object.FindString(oldchoice))
			return True
		elif data['type']== 'grid':
			paperid = int(data['content'])
			core.Set_Papers_Attr([paperid], 'class', target)
			return True
		return False
