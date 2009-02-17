import datetime; now=datetime.datetime.utcnow()
import uuid

db=SQLDB('sqlite://db.db')

db.define_table('person',SQLField('uuid',length=64,default=uuid.uuid4()), 
                         SQLField ('modified_on','datetime',default=now), 
                         SQLField('name'))  


id=uuid.uuid4()
