# -*- coding: utf-8 -*-
import sqlite3
from util import *

DB_conn = None
Working_Dir = None
Project_Name = None

def OpenTable(name):
	global DB_conn, Working_Dir, Project_Name
	if DB_conn == None:
		import os.path
		DB_conn = sqlite3.connect(os.path.join(Working_Dir, Project_Name+'.rl'))
	c = DB_conn.cursor()
	c.execute('''select count(*) from sqlite_master where type='table' and name = '%s';''' % name)
	if c.fetchone()[0] <= 0:
		if name in config.TABLES:
			# print "create table %s (%s);" % (name, config.TABLES[name])
			c.execute("create table %s (%s);" % (name, config.TABLES[name]))
			DB_conn.commit()
			return True
		else:
			warn("Invalid Table Name!")
	else:
		return True
	return False

def safe_connect(filepath):
	# print filepath
	global Working_Dir, Project_Name
	try:
		# DB_conn = sqlite3.connect(filepath)
		import os.path
		Working_Dir = os.path.dirname(filepath)
		Project_Name = os.path.basename(filepath)
		Project_Name = Project_Name[:Project_Name.find('.')]
		# print Project_Name
		return None
	except Exception, e:
		return str(e)

def Get_Lists(table):
	global DB_conn
	if OpenTable(table):
		c = DB_conn.cursor()
		# print '''select name from %s%s;''' % (table," ORDER BY rank ASC" if table=='list_class' else "")
		c.execute('''select name from %s%s;''' % (table," ORDER BY rank ASC" if table=='list_class' else ""))
		res = c.fetchall()
		DB_conn.close()
		DB_conn = None
		if len(res)<=0:
			return []
		else:
			return list(zip(*res)[0])
	else:
		return []

def Get_Paper_Data(id, is_all=True):
	global DB_conn
	cols = ', '.join(config.SHORTCUT_4_PAPER)
	if OpenTable('papers'):
		c = DB_conn.cursor()
		c.execute('''select %s from papers where id=%s;''' % ('*' if is_all else cols, str(id)))
		keys = config.TABLE_LABELS['papers'] if is_all else config.SHORTCUT_4_PAPER
		data = c.fetchone()
		res = dict(zip(keys, data))
		DB_conn.close()
		DB_conn = None
		return res
	else:
		return None

def Get_Class_Data(cls, labels=None, is_all = False, search=""):
	global DB_conn
	if cls == u'未分类':
		cls = ""
	cols = ', '.join(config.SHORTCUT_4_PAPER)
	searchtext = u''' AND (title LIKE '%%%s%%' OR main LIKE '%%%s%%')''' % (search, search) if search != "" else ""
	# print searchtext
	if OpenTable('papers'):
		c = DB_conn.cursor()
		try:
			if cls==None:
				res = []
				for k in labels:
					# print '''select %s from papers where class='%s'%s;''' % ('*' if is_all else cols, k, searchtext)
					c.execute('''select %s from papers where class='%s'%s;''' % ('*' if is_all else cols, k, searchtext))
					res += c.fetchall()
				# print '''select %s from papers where class=''%s;''' % ('*' if is_all else cols, searchtext)
				c.execute('''select %s from papers where class=''%s;''' % ('*' if is_all else cols, searchtext))
				res += c.fetchall()
				DB_conn.close()
				DB_conn = None
				return res
			else:
				# print '''select %s from papers where class='%s'%s;''' % ('*' if is_all else cols, cls, searchtext)
				c.execute('''select %s from papers where class='%s'%s;''' % ('*' if is_all else cols, cls, searchtext))
				res = c.fetchall()
				DB_conn.close()
				DB_conn = None
				return res
		except Exception, e:
			import traceback
			# traceback.print_exc(e)
			DB_conn.close()
			DB_conn = None
			return []
	else:
		return []

def Set_Paper_Data(id, data):
	global DB_conn
	if len(data)<=0:
		return ""
	cont = ""
	if OpenTable('papers'):
		try:
			c = DB_conn.cursor()
			if id==None:
				# 创建新条目
				# print u'''insert into papers %s values %s;''' % (str(tuple(data.keys())), ProperTuple(data.values()))
				# wx.MessageBox(u'''insert into papers %s values %s;''' % (str(tuple(data.keys())), ProperTuple(data.values())))
				c.execute(u'''insert into papers %s values %s;''' % (str(tuple(data.keys())), ProperTuple(data.values())))
			else:
				# 更新条目
				cont = u', '.join([u"%s = %s" % (str(k),ProperString(v)) for k,v in data.iteritems()])
				# wx.MessageBox( u'''update papers set %s where id=%s;''' % (cont, str(id)))
				c.execute(u'''update papers set %s where id=%s;''' % (cont, str(id)))
			DB_conn.commit()
			DB_conn.close()
			DB_conn = None
			return ""
		except Exception, e:
			import traceback
			# traceback.print_exc(e)
			DB_conn.close()
			DB_conn = None
			return traceback.format_exc(e)
	else:
		return u"Failed to Access DataBase!"

def Set_List(table, name):
	global DB_conn
	if name == "":
		return ""
	if OpenTable(table):
		try:
			c = DB_conn.cursor()
			# print '''insert into %s %s values %s;''' % (table, "(name)", "('%s')" % name)
			c.execute(u'''replace into %s %s values %s;''' % (table, "(name)","('%s')" % name))
			DB_conn.commit()
			DB_conn.close()
			DB_conn = None
			return ""
		except Exception, e:
			# print str(e)
			DB_conn.close()
			DB_conn = None
			import traceback
			return traceback.format_exc(e)
	else:
		return "Failed to Access DataBase!"

def Delete_Table_Item(table, key, value):
	global DB_conn
	if OpenTable(table):
		try:
			c = DB_conn.cursor()
			# print '''delete from %s WHERE %s = %s;''' % (table, key, ProperString(value))
			c.execute('''delete from %s WHERE %s = %s;''' % (table, key, ProperString(value)))
			DB_conn.commit()
			DB_conn.close()
			DB_conn = None
			return ""
		except Exception, e:
			# print str(e)
			DB_conn.close()
			DB_conn = None
			return str(e)
	else:
		return "Failed to Access DataBase!"

def Get_Ids(table, key, value):
	global DB_conn
	if OpenTable(table):
		try:
			c = DB_conn.cursor()
			# print '''select id from %s WHERE %s = %s;''' % (table, key, ProperString(value))
			c.execute('''select id from %s WHERE %s = %s;''' % (table, key, ProperString(value)))
			res = c.fetchall()
			DB_conn.close()
			DB_conn = None
			return list(zip(*res)[0])
		except Exception, e:
			# print str(e)
			DB_conn.close()
			DB_conn = None
			return []
	else:
		return []

def Set_Class_Sort(labels):
	global DB_conn
	if len(labels)<=0:
		return ""
	if OpenTable('list_class'):
		try:
			c = DB_conn.cursor()
			# cont = ', '.join(["%s = %s" % (str(k),str(v)) for k,v in enumerate(labels)])
			# print '''update list_class set %s where id=%s;''' % (cont, str(id))
			for i, k in enumerate(labels):
				if k == u'全部' or k==u'未分类':
					continue
				c.execute('''update list_class set %s = %s where name='%s';''' % ('rank', str(i), unicode(k)))
			DB_conn.commit()
			DB_conn.close()
			DB_conn = None
			return ""
		except Exception, e:
			# print str(e)
			DB_conn.close()
			DB_conn = None
			return str(e)
	else:
		return "Failed to Access DataBase!"

def Set_Papers_Attr(paperids, key, value):
	global DB_conn
	# print paperids
	if len(paperids)<=0:
		return ""
	if OpenTable('papers'):
		try:
			c = DB_conn.cursor()
			if len(paperids)==1:
				# print '''update papers set %s = %s where id = %s;''' % (key, ProperString(value), str(paperids[0]))
				c.execute('''update papers set %s = %s where id = %s;''' % (key, ProperString(value), str(paperids[0])))
			else:
				# print '''update papers set %s = %s where id IN %s;''' % (key, ProperString(value), str(tuple(paperids)))
				c.execute('''update papers set %s = %s where id IN %s;''' % (key, ProperString(value), str(tuple(paperids))))
			DB_conn.commit()
			DB_conn.close()
			DB_conn = None
			return ""
		except Exception, e:
			# print str(e)
			DB_conn.close()
			DB_conn = None
			return str(e)
	else:
		return "Failed to Access DataBase!"

def Get_Paper_Addr(id):
	global DB_conn
	if OpenTable('papers'):
		c = DB_conn.cursor()
		c.execute('''select database, dbid from papers where id=%s;''' % (str(id)))
		data = c.fetchone()
		DB_conn.close()
		DB_conn = None
		if data[0] in config.HOMEPAGE_FORMAT:
			return config.HOMEPAGE_FORMAT[data[0]] % data[1]
		else:
			return None
	else:
		return None

def Get_Paper_Title(id):
	global DB_conn
	if OpenTable('papers'):
		c = DB_conn.cursor()
		c.execute('''select title from papers where id=%s;''' % (str(id)))
		res = c.fetchone()[0]
		DB_conn.close()
		DB_conn = None
		return res
	else:
		return None



