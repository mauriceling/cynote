import datetime

now=datetime.datetime.utcnow()

cynotedb=SQLDB('sqlite://cynotedb.db')

#the notebook table
cynotedb.define_table('notebook',
                SQLField('name', 'text'),
                SQLField('description', 'text'),
                SQLField('type','text', default='ledger'),
                SQLField('archived', 'boolean', default=False))

#the new entry table
#file upload
#link to notebook table
#using datetime
cynotedb.define_table('entry',
                SQLField('title', 'text'),
                SQLField('author'),
                SQLField('file', 'upload'),
                SQLField('filename'),
                SQLField('keywords', length=256),
                SQLField('notebook', cynotedb.notebook),
                SQLField('datetime', 'datetime', default=now),
                SQLField('description', 'text'))

#the comment table
#entry_id link to entry table
cynotedb.define_table('comment', 
                SQLField('author'),
                SQLField('file','upload'),
                SQLField('filename'),
                SQLField('body', 'text'),
                SQLField('datetime', 'datetime', default=now),
                SQLField('entry_id', cynotedb.entry))
                
cynotedb.define_table('result',
                SQLField('author', default=session.username),
                SQLField('testresult','text'))  
         
#most of the text requires to be type and can't be empty
#when link to other table "is_in_db" must be added         
cynotedb.notebook.name.requires=[IS_NOT_EMPTY(),IS_NOT_IN_DB(cynotedb,'notebook.name')]
cynotedb.entry.title.requires=[IS_NOT_EMPTY()]
cynotedb.entry.description.requires=[IS_NOT_EMPTY()]
#cynotedb.entry.keywords.requires=IS_NOT_EMPTY()
cynotedb.entry.notebook.requires=IS_IN_DB(cynotedb,'notebook.id','notebook.name')
cynotedb.entry.datetime.requires=IS_DATETIME()
cynotedb.comment.datetime.requires=IS_DATETIME()
cynotedb.comment.entry_id.requires=IS_IN_DB(cynotedb,'entry.id','entry.title')
cynotedb.comment.author.requires=IS_NOT_EMPTY()
#cynotedb.comment.body.requires=IS_NOT_EMPTY()
#for oldest to newest
entry=cynotedb().select(cynotedb.entry.datetime,orderby=cynotedb.entry.datetime)
comment=cynotedb().select(cynotedb.comment.datetime,orderby=cynotedb.comment.datetime)
#for newest to oldest
#entry=cynotedb().select(cynotedb.entry.datetime,orderby=~cynotedb.entry.datetime)
#comment=cynotedb().select(cynotedb.comment.datetime,orderby=~cynotedb.comment.datetime)
