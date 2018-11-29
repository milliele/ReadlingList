# -*- coding: utf-8 -*-

import wx
import wx.grid
import wx.html
import config
import pandas as pd
import markdown, codecs, string

from registry import register_decorator


def warn(message, title='Warning', icon=wx.ICON_EXCLAMATION, button=wx.OK):
	wx.MessageBox(message, title,
				  button | icon)


def ProperString(element):
	if isinstance(element, int):
		return str(element)
	else:
		return u"'%s'" % unicode(element.replace("'", "''"))


def ProperTuple(tu):
	items = []
	for element in tu:
		items.append(ProperString(element))
	return "(%s)" % ', '.join(items)


def TruncatedString(m_str, width):
	le = int((width - 5) / 1.6)
	if len(m_str) > le:
		return m_str[:le] + "..."
	return m_str


class MyGridTable(wx.grid.GridTableBase):
	EVEN_ROW_COLOUR = '#CCE6FF'
	GRID_LINE_COLOUR = '#ccc'

	def __init__(self, data, col_labels):
		wx.grid.GridTableBase.__init__(self)
		# self.headerRows = 1
		self.__data = pd.DataFrame(data, columns=col_labels)
		# print self.__data
		self.n_rows = len(self.__data)
		self.n_cols = len(self.__data.columns)

	# self.__data = data
	# self.__labels = col_labels
	# print self.__data
	# print self.__labels
	# print self.n_cols, self.n_rows

	# def SetWid(self, width):
	# 	self.width = width

	def AppendRows(self, numRows=1):
		pass

	def AppendCols(self, numCols=1):
		pass

	def GetColLabelValue(self, col):
		# print 'GetColLabelValue', col
		return str(config.COL_TITLE[self.__data.columns[col]]) if self.IsColSave(col) else ""

	def GetValue(self, row, col):
		# print row,col, unicode(self.__data[row][col])
		return unicode(self.__data.iloc[row, col]) if self.IsCellSave(row, col) else ""

	def GetNumberCols(self):
		# print 'GetNumberCol'
		return self.n_cols

	def GetNumberRows(self):
		# print 'GetNumberRows'
		return self.n_rows

	def GetTypeName(self, row, col):
		return wx.grid.GRID_VALUE_STRING

	def GetAttr(self, row, col, prop):
		attr = wx.grid.GridCellAttr()
		if row % 2 == 1:
			attr.SetBackgroundColour(self.EVEN_ROW_COLOUR)
		return attr

	def IsColSave(self, col):
		# print 'IsColSav', col
		return col >= 0 and col < self.n_cols

	def IsRowSave(self, row):
		# print 'IsRowSav', row
		return row >= 0 and row < self.n_rows

	def IsCellSave(self, row, col):
		# print 'IsCellSave', row,col
		return self.IsColSave(col) and self.IsRowSave(row)

	def IsEmptyCell(self, row, col):
		# print 'IsEmptyCell', row,col
		return not self.IsCellSave(row, col)

	def Sort(self, col, asc=True):
		self.__data.sort_values(by=self.__data.columns[col], inplace=True, ascending=asc)

	def UnSort(self):
		self.__data.sort_index(inplace=True)


def Single_Paper_MarkDown(data):
	data = dict(
		zip(config.TABLE_LABELS['papers'], map(lambda x: x.encode('utf-8') if isinstance(x, unicode) else x, data)))
	return "\n## %s\n\n时间 | 会议 / 期刊 | 被引量 | 参考文献数量\n----|------|----|---\n%d | %s %s | %d | %d\n\n%s" % \
		   (data['title'], data['time'], data['conference'], data['type'], data['beref'], data['refnum'], data['main'])


def Markdown2HTML(filename, width=25, nonumber=False):
	htmlTemplate = string.Template('''
	<!DOCTYPE html>
	<html>
	<head>
	<meta charset=utf-8>
		<style>
		html, body {width: 100%}
		body {margin: 0px;}
		aside.toc { position:fixed; top:0px; left: 0px; width: ${asideWidth}%; border-right: 2px solid grey; overflow: scroll}
		main { position: relative; width: ${mainWidth}%; left: ${asideWidth}%; margin-left: 25px; }
		${css_for_header_number}
		table{margin-top:0;margin-bottom:1pc;border-collapse:collapse;border-spacing:0}table th{font-weight:700}table td,table th{padding:6px 13px;border:1px solid #ddd}table tr{border-top:1px solid #ccc}table tr:nth-child(even){background-color:#f8f8f8}
		</style>
	</head>
	<body>
	<aside class="toc">$toc</aside>
	<main>$mainContent</main>
	<script>
		var tocElem = document.querySelector("aside.toc");
		tocElem.style.setProperty("height", window.innerHeight+'px');

		window.addEventListener("resize", resizeThrottler, false);

		var resizeTimeout;
		function resizeThrottler() {
		// ignore resize events as long as an actualResizeHandler execution is in the queue
		if ( !resizeTimeout ) {
			resizeTimeout = setTimeout(function() {
			resizeTimeout = null;
			actualResizeHandler();
		   }, 300);
		}
	  }

	  function actualResizeHandler() {
		tocElem.style.setProperty("height", window.innerHeight+'px');
	  }
	</script>
	<body>
	''')

	css_for_header_number = ''
	if not nonumber:
		css_for_header_number = '''
	body { counter-reset: h1counter}
		h1 { counter-reset: h2counter}  /* cannot use the same counter as h2 is not the child of h1*/
		h1::before {counter-increment: h1counter; content: counter(h1counter) " ";}
		h2 { counter-reset: h3counter}
		h2::before {counter-increment: h2counter; content: counter(h1counter) "." counter(h2counter) " "}
		h3 { counter-reset: h4counter}
		h3::before {counter-increment: h3counter; content: counter(h1counter) "." counter(h2counter) "." counter(h3counter) " "}
		h4::before {counter-increment: h4counter; content: counter(h1counter) "." counter(h2counter) "." counter(h3counter) "." counter(h4counter) " "}
		aside ul { counter-reset: section;  list-style-type: none; }
		aside li::before { counter-increment: section; content: counters(section,".") " "; }
		aside ul ul ul ul ul li::before {content: none}   /* number depth : 4 */
	'''

	md = markdown.Markdown(extensions=['markdown.extensions.toc', 'markdown.extensions.tables'], output_format="html5")

	# md.convert() accepts only unicode
	infile = codecs.open(filename, mode="r", encoding="utf-8")
	mdtext = infile.read()

	# use convert() instead of convertFile() as convertFile() output the result to either a file or stdout.
	mainContent = md.reset().convert(mdtext)

	# warning: there should not be a marker such as [TOC] for toc in the converted .md file,
	# or else md would not have attribute toc
	# 100-3 : 3 percent for margin

	html = htmlTemplate.substitute(asideWidth=width, mainWidth=(100 - 3 - width), toc=md.toc,
								   mainContent=mainContent, css_for_header_number=css_for_header_number)

	infile.close()

	return html


# Decorators
# 打印函数名字
def debug_name(func):
	def wrapper(*args, **kwargs):
		print "[DEBUG]: enter {}()".format(func.__name__)
		return func(*args, **kwargs)

	return wrapper


class SuggestionsPopup(wx.Frame):
	__keyboard_funcs = {}
	__keyboard_funcs[wx.WXK_ESCAPE] = wx.Frame.Hide
	__keyboard_decorator = register_decorator(__keyboard_funcs)

	def __init__(self, parent):
		wx.Frame.__init__(
			self, parent,
			style=wx.FRAME_NO_TASKBAR | wx.FRAME_FLOAT_ON_PARENT | wx.STAY_ON_TOP
		)
		self._suggestions = self._listbox(self)
		self._suggestions.SetItemCount(0)
		self._unformated_suggestions = None

		self.Sizer = wx.BoxSizer()
		self.Sizer.Add(self._suggestions, 1, wx.EXPAND)

	class _listbox(wx.html.HtmlListBox):
		items = None

		def OnGetItem(self, n):
			return self.items[n]

	def SetSuggestions(self, suggestions, unformated_suggestions):
		self._suggestions.items = suggestions
		self._suggestions.SetItemCount(len(suggestions))
		self._suggestions.SetSelection(0)
		self._suggestions.Refresh()
		self._unformated_suggestions = unformated_suggestions

	@__keyboard_decorator(wx.WXK_UP)
	def CursorUp(self):
		l = self._suggestions.GetItemCount()
		selection = self._suggestions.GetSelection()
		self._suggestions.SetSelection((l + selection - 1) % l)

	@__keyboard_decorator(wx.WXK_DOWN)
	def CursorDown(self):
		l = self._suggestions.GetItemCount()
		selection = self._suggestions.GetSelection()
		# last = self._suggestions.GetItemCount() - 1
		self._suggestions.SetSelection((selection + 1) % l)

	@__keyboard_decorator(wx.WXK_HOME)
	def CursorHome(self):
		if self.IsShown():
			self._suggestions.SetSelection(0)

	@__keyboard_decorator(wx.WXK_END)
	def CursorEnd(self):
		if self.IsShown():
			self._suggestions.SetSelection(self._suggestions.GetItemCount() - 1)

	def GetSelectedSuggestion(self):
		return self._unformated_suggestions[self._suggestions.GetSelection()]

	def GetSuggestion(self, n):
		return self._unformated_suggestions[n]

	@property
	def keyboard_funcs(self):
		return self.__keyboard_funcs


class AutocompleteTextCtrl(wx.TextCtrl):
	__keyboard_funcs = {}
	__keyboard_decorator = register_decorator(__keyboard_funcs)

	def __init__(self, *args, **kwargs):
		if 'style' in kwargs:
			kwargs['style'] |= wx.TE_PROCESS_ENTER
		if len(args) >= 6:
			args[5] |= wx.TE_PROCESS_ENTER
		wx.TextCtrl.__init__(self, *args, **kwargs)
		self.height = 300
		self.frequency = 250
		self.queued_popup = False
		self.skip_event = False

	def SetCompleter(self, completer):
		"""
		Initializes the autocompletion. The 'completer' has to be a function
		with one argument (the current value of the control, ie. the query)
		and it has to return two lists: formated (html) and unformated
		suggestions.
		"""
		self.completer = completer

		frame = self.Parent
		while not isinstance(frame, wx.Frame):
			frame = frame.Parent

		self.popup = SuggestionsPopup(frame)

		frame.Bind(wx.EVT_MOVE, self.OnMove)
		self.Bind(wx.EVT_TEXT, self.OnTextUpdate)
		self.Bind(wx.EVT_SIZE, self.OnSizeChange)
		self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
		self.popup._suggestions.Bind(wx.EVT_LEFT_DOWN, self.OnSuggestionClicked)
		self.popup._suggestions.Bind(wx.EVT_KEY_DOWN, self.OnSuggestionKeyDown)

	def AdjustPopupPosition(self):
		self.popup.Move(self.ClientToScreen((0, self.Size.height)).Get())
		self.popup.Layout()
		self.popup.Refresh()

	def OnMove(self, event):
		self.AdjustPopupPosition()
		event.Skip()

	def OnTextUpdate(self, event):
		if self.skip_event:
			self.skip_event = False
		elif not self.queued_popup:
			wx.CallLater(self.frequency, self.AutoComplete)
			self.queued_popup = True
		event.Skip()

	def AutoComplete(self):
		self.queued_popup = False
		if self.Value != "":
			formated, unformated = self.completer(self.Value)
			if len(formated) > 0:
				self.popup.SetSuggestions(formated, unformated)
				self.AdjustPopupPosition()
				self.Unbind(wx.EVT_KILL_FOCUS)
				self.popup.ShowWithoutActivating()
				self.SetFocus()
				self.Bind(wx.EVT_KILL_FOCUS, self.OnKillFocus)
			else:
				self.popup.Hide()
		else:
			self.popup.Hide()

	def OnSizeChange(self, event):
		self.popup.Size = (self.Size[0], self.height)
		event.Skip()

	@__keyboard_decorator(wx.WXK_RETURN)
	@__keyboard_decorator(wx.WXK_NUMPAD_ENTER)
	def OnKeyboardReturn(self):
		if self.popup.Shown():
			self.skip_event = True
			self.SetValue(self.popup.GetSelectedSuggestion())
			self.SetInsertionPointEnd()
			self.popup.Hide()

	def OnKeyDown(self, event):
		key = event.GetKeyCode()
		is_happen = False
		if key in self.popup.keyboard_funcs:
			self.popup.keyboard_funcs[key](self.popup)
			is_happen = True
		if key in self.__keyboard_funcs:
			self.__keyboard_funcs[key](self)
		elif not is_happen:
			event.Skip()

	def OnSuggestionClicked(self, event):
		self.skip_event = True
		n = self.popup._suggestions.HitTest(event.Position)
		self.Value = self.popup.GetSuggestion(n)
		self.SetInsertionPointEnd()
		wx.CallAfter(self.SetFocus)
		event.Skip()

	def OnSuggestionKeyDown(self, event):
		key = event.GetKeyCode()
		if key in (wx.WXK_RETURN, wx.WXK_NUMPAD_ENTER):
			self.skip_event = True
			self.SetValue(self.popup.GetSelectedSuggestion())
			self.SetInsertionPointEnd()
			self.popup.Hide()
		event.Skip()

	def OnKillFocus(self, event):
		if not self.popup.IsActive():
			self.popup.Hide()
		event.Skip()


class AutoCompleteComboBox(wx.ComboBox):
	__keyboard__funcs = {}
	__keyboard__decorator = register_decorator(__keyboard__funcs)

	def __init__(self, *args, **kwargs):
		wx.ComboBox.__init__(self, *args, **kwargs)
		self.choices = self.GetItems()
		self.Bind(wx.EVT_TEXT, self.EvtText)
		self.Bind(wx.EVT_KEY_DOWN, self.EvtKeydown)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnKeyReturn)
		self.Bind(wx.EVT_COMBOBOX, self.EvtCombobox)
		self.Bind(wx.EVT_COMBOBOX_DROPDOWN, self.EvtDropdown)
		self.Bind(wx.EVT_COMBOBOX_CLOSEUP, self.EvtCloseup)
		# self.Bind(wx.EVT_KILL_FOCUS, self.EvtKillFocus)

		self.last_match = ""
		self.ignoreEvtText = False
		self.is_matching = False
		self.is_ignorecase = False

	def SetIgnoreCase(self, flag):
		self.is_ignorecase = bool(flag)

	def SetChoices(self, choices):
		self.choices = choices
		if not self.is_matching:
			self.SafeSetItems(self.choices)

	def GetChoices(self):
		return self.choices

	def SafeSetItems(self, choices):
		self.ignoreEvtText = True
		string = self.Value
		self.SetItems(choices)
		self.SafeSetChoice(string)
		self.ignoreEvtText = False

	# @debug_name
	# def EvtKillFocus(self, event):
	# 	if self.is_matching:
	# 		self.is_matching = False
	# 	event.Skip()

	# @debug_name
	def EvtDropdown(self, event):
		if not self.is_matching:
			self.SafeSetItems(self.choices)
		event.Skip()

	def AutoFindString(self, string):
		if self.is_ignorecase:
			string = string.upper()
		return self.FindString(string)

	def SafeSetChoice(self, string):
		self.ignoreEvtText = True
		index = self.AutoFindString(string)
		if index != wx.NOT_FOUND:
			self.SetSelection(index)
		else:
			self.Select(wx.NOT_FOUND)
			self.SetValue(string)
			self.SetInsertionPointEnd()
		self.ignoreEvtText = False

	# @debug_name
	def EvtCloseup(self, event):
		if self.is_matching:
			self.is_matching = False
			# return
		event.Skip()

	# @debug_name
	def EvtCombobox(self, event):
		# self.SetInsertionPointEnd()
		event.Skip()

	# @__keyboard__decorator(wx.WXK_BACK)
	# # @debug_name
	# def OnKeyDelete(self, event):
	# 	event.Skip()

	@__keyboard__decorator(wx.WXK_SPACE)
	@debug_name
	def OnKeySpace(self, event):
		if self.is_matching:
			# fr, to = self.GetTextSelection()
			# self.ignoreEvtText = True
			self.SafeSetChoice(self.GetString(0))
			self.is_matching = False
			self.Dismiss()
			return
			# self.ignoreEvtText = False
		event.Skip()

	# @debug_name
	@__keyboard__decorator(wx.WXK_RETURN)
	def OnKeyReturn(self, event):
		if self.is_matching:
			# self.SetInsertionPointEnd()
			self.Dismiss()
			# return
		event.Skip()

	# @debug_name
	def EvtKeydown(self, event):
		key = event.GetKeyCode()
		if event.ControlDown():
			if unichr(key).lower() == 'a':
				# 全选
				self.SelectAll()
			elif unichr(key).lower() == 'x':
				# textobject = wx.TextDataObject()
				dataObj = wx.TextDataObject()
				fr, to = self.GetTextSelection()
				dataObj.SetText(self.Value[fr:to])
				if wx.TheClipboard.Open():
					wx.TheClipboard.SetData(dataObj)
					wx.TheClipboard.Close()
					self.SafeSetChoice(self.Value[:fr]+self.Value[to:])
				else:
					wx.MessageBox("Unable to open the clipboard", "Error")
			elif unichr(key).lower() == 'v':
				# textobject = wx.TextDataObject()
				dataObj = wx.TextDataObject()
				fr, to = self.GetTextSelection()
				if wx.TheClipboard.Open():
					wx.TheClipboard.GetData(dataObj)
					wx.TheClipboard.Close()
					# self.ignoreEvtText = True
					self.SafeSetChoice(self.Value[:fr]+dataObj.GetText()+self.Value[to:])
				else:
					wx.MessageBox("Unable to open the clipboard", "Error")
		if key in self.__keyboard__funcs:
			self.__keyboard__funcs[key](self, event)
			return
		else:
			event.Skip()

	def IsAutoCompleteTime(self):
		# 自动补全的时机
		# 1. 光标在最后
		#
		# 3. 字符串在列表中没有
		return self.GetInsertionPoint() == len(self.Value) \
			   and self.Value != self.last_match
			# \ and self.AutoFindString(self.Value) == wx.NOT_FOUND

	def Head_Completer(self, query):
		res = []
		if self.is_ignorecase:
			query = query.upper()
		for choice in self.choices:
			new_choice = choice.upper() if self.is_ignorecase else choice
			if new_choice.startswith(query):
				res.append(choice)
		return res

	def AutoComplete(self):
		self.last_match = self.Value
		if self.last_match == "":
			return False
		choices = self.Head_Completer(self.last_match)
		if len(choices) > 0:
			# self.ignoreEvtText = True
			self.is_matching = True
			# self.SetItems(choices)
			self.SafeSetItems(choices)
			# self.SafeSetChoice(self.last_match)
			# self.SetSelection(wx.NOT_FOUND)
			# self.SetTextSelection(len(self.last_match), len(self.Value))
			self.Popup()
			# self.ignoreEvtText = False
			return True
		return False

	# @debug_name
	def EvtText(self, event):
		# print self.ignoreEvtText
		if self.ignoreEvtText:
			# self.ignoreEvtText = False
			event.Skip()
			return
		elif self.IsAutoCompleteTime():
			# print 'autobegin'
			if self.AutoComplete():
				return
			else:
				self.Dismiss()
		else:
			self.Dismiss()
		event.Skip()
