# -*- coding: utf-8 -*-

TABLES = {
	'papers': '''
		id INTEGER PRIMARY KEY   AUTOINCREMENT  NOT NULL,
	    title     UNIQUE      TEXT    NOT NULL,
	    class INT,
	    conference       TEXT,
	    type        TEXT,
	    time         INT,
	    beref         INT,
	    refnum         INT,
	    database TEXT,
	    dbid TEXT,
	    main TEXT,
	    reference TEXT,
	    bibtex TEXT
		''',
	'list_class': '''
	    name  TEXT    NOT NULL UNIQUE,
	    rank         INT
		''',
	'list_type': '''
	    name    TEXT    NOT NULL UNIQUE
		''',
	'list_database': '''
	    name    TEXT    NOT NULL UNIQUE
		''',
	'list_conference': '''
	    name        TEXT    NOT NULL UNIQUE
		''',
}

TABLE_LABELS = {
	'papers': ['id', 'title', 'class', 'conference', 'type', 'time', 'beref', 'refnum', 'database', 'dbid', 'main', 'reference', 'bibtex'],
	'list_class': ['name', 'rank'],
	'list_type': ['name'],
	'list_database': ['name'],
	'list_conference': ['name'],
}

SHORTCUT_4_PAPER = [
	'id',
	'class',
	'time',
	'conference',
	'type',
	'title',
	'beref',
	'refnum',
]

COL_TITLE = {
	'id':'id',
	'title': '标题',
	'conference': '会议/期刊',
	'type': '等级',
	'time': '时间',
	'refnum': '参考文献数量',
	'beref': '被引量',
	'class': '分类',
}

COMBOBOXES = ['class', 'conference', 'type', 'database']

HOMEPAGE_FORMAT = {
	'ACM': "https://dl.acm.org/citation.cfm?id=%s",
	'IEEE': "https://ieeexplore.ieee.org/abstract/document/%d",
	'ARXIV': "https://arxiv.org/abs/%s"
}

DATABASE_ASSOSIATE = {
	'SIGCOMM': 'ACM',
	'CONEXT': 'ACM',
	'MM': 'ACM',
	'MMSYS': 'ACM',
	'INFOCOM': 'IEEE',
	'ICC': 'IEEE',
}

