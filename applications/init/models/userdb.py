# try something like
userdb=SQLDB("sqlite://userdb.db")

#the username table
userdb.define_table('user',
                SQLField('username', 'string', unique=True),
                SQLField('password', 'string'),
                SQLField('aging', 'integer'),
                SQLField('authorized', 'boolean'))
                
userdb.user.username.requires=IS_NOT_EMPTY()
userdb.user.username.requires=IS_NOT_IN_DB(userdb, 'user.username')
