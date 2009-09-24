import datetime; now=datetime.datetime.utcnow()
import uuid

db=SQLDB('sqlite://db.db')

db.define_table('log', SQLField('event'),
                       SQLField('user'), 
                       SQLField('modified_on','datetime',default=now))

db.define_table('user_event',
                SQLField('event'),
                SQLField('user'), 
                SQLField('modified_on','datetime',default=now))
