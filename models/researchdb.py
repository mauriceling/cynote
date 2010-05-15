import datetime

now=datetime.datetime.utcnow()

researchdb=SQLDB('sqlite://researchdb.db')

researchdb.define_table('control',
                SQLField('tablename', 'text'))