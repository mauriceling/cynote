import datetime; now=datetime.datetime.utcnow()
import uuid

db=SQLDB('sqlite://db.db')

db.define_table('log', SQLField('event', 'text'),
                       SQLField('user'), 
                       SQLField('modified_on', 'datetime', default=now))

db.define_table('user_event',
                SQLField('event', 'text'),
                SQLField('user'), 
                SQLField('modified_on', 'datetime', default=now))

db.define_table('entry_hash',
                SQLField('eid'),
                SQLField('edatetime'),
                SQLField('etitle', 'text'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('ehash', 'text'))
                
db.define_table('comment_hash',
                SQLField('cid'),
                SQLField('cdatetime'),
                SQLField('eid'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('chash', 'text'))

db.define_table('track_entry_hash',
                SQLField('eid'),
                SQLField('edatetime'),
                SQLField('etitle', 'text'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('ehash', 'text'))
                
db.define_table('track_comment_hash',
                SQLField('cid'),
                SQLField('cdatetime'),
                SQLField('eid'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('chash', 'text'))
                
db.define_table('file_hash',
                SQLField('filename'),
                SQLField('hashed', 'datetime', default=now),
                SQLField('fhash', 'text'))