import os
import copy

###############################################################################
# Support functions (from appadmin.py)
###############################################################################
global_env = copy.copy(globals())
global_env['datetime'] = datetime

def get_databases(request):
    dbs = {}
    for (key, value) in global_env.items():
        cond = False
        try:
            cond = isinstance(value, GQLDB)
        except:
            cond = isinstance(value, SQLDB)
        if cond:
            dbs[key] = value
    return dbs
    
databases = get_databases(None)

def eval_in_global_env(text):
    exec ('_ret=%s' % text, {}, global_env)
    return global_env['_ret']
    
def get_database(request):
    if request.args and request.args[0] in databases:
        return eval_in_global_env(request.args[0])
    else:
        session.flash = T('invalid request')
        redirect(URL(r=request, f='index'))
        
def get_table(request):
    db = get_database(request)
    if len(request.args) > 1 and request.args[1] in db.tables:
        return (db, request.args[1])
    else:
        session.flash = T('invalid request')
        redirect(URL(r=request, f='index'))
###############################################################################
# End - Support functions
###############################################################################

def create_table():
    if session.username == None:
        redirect(URL(r=request, c='account', f='log_in'))
    form = FORM(TABLE(
            TR('Table Name: ', INPUT(_type='text', _name='name', _size=80)),
            TR('Column Definition: ', TEXTAREA(_type='text', _name='definition')),
            TR('Description: ', TEXTAREA(_type='text', _name='description')),
            TR('', INPUT(_type='submit', _name='Submit'))))
    if form.accepts(request.vars, session):
        fields = [x.strip() 
                  for x in form.vars.definition.split(',')
                    if x.strip() != '']
        field_template = "SQLField('%s', 'text')"
        col_def = [field_template % x for x in fields]
        col_def.append("SQLField('datetime', 'datetime', default=now)")
        col_def = ',\n\t '.join(col_def)
        table_def = "researchdb.define_table('%s', \n\t" % form.vars.name
        table_def = table_def + col_def + ')'
        rdb_file = os.sep.join([os.getcwd(), 'applications', 
                                request.application, 'models',
                                'researchdb_adhoc.py'])
        f = open(rdb_file, 'a')
        f.write('\n' + table_def + '\n')
        f.close()
        researchdb.control.insert(tablename=form.vars.name,
                                  columndef=col_def,
                                  creator=session.username,
                                  description=form.vars.description)
        db.log.insert(event='New ad hoc table created. Definition = ' + 
                      table_def, user=session.username)
        redirect(URL(r=request, f='list_table'))
    return dict(form=form)
    
def list_table():
    records = researchdb(researchdb.control.archived==False) \
              .select(orderby=researchdb.control.tablename)
    return dict(tables=records)

def generic_insert():
    if session.username == None:
        redirect(URL(r=request, c='account', f='log_in'))
    (db, table) = get_table(request)
    form = SQLFORM(db[table], ignore_rw=True)
    print request
    if form.accepts(request.vars, session):
        response.flash = T('new record inserted')
    return dict(form=form, table=request.args[1])
    
