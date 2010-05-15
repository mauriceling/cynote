import datetime

now=datetime.datetime.utcnow()

researchdb=SQLDB('sqlite://researchdb.db')

researchdb.define_table('control',
                SQLField('tablename', 'text'),
                SQLField('columndef', 'text'),
                SQLField('creator', 'text'),
                SQLField('datetime', 'datetime', default=now),
                SQLField('description', 'text'),
                SQLField('archived', 'boolean', default=False))
