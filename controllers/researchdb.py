import os

def create_table():
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(TABLE(
            TR('Table Name: ', INPUT(_type='text', _name='name', _size=80)),
            TR('Column Definition: ', TEXTAREA(_type='text', _name='definition')),
            TR('Description: ', TEXTAREA(_type='text', _name='description')),
            TR('', INPUT(_type='submit', _name='Submit'))))
    if form.accepts(request.vars, session):
        fields = [x.strip() 
                  for x in form.vars.definition.split(',')
                    if x.strip() != '']
        field_template = "SQLField('%s')"
        col_def = [field_template % x for x in fields]
        col_def.append("SQLField('datetime', 'datetime', default=now)")
        col_def = ',\n\t '.join(col_def)
        table_def = "researchdb.define_table('%s', \n\t" % form.vars.name
        table_def = table_def + col_def + ')'
        rdb_file = os.sep.join([os.getcwd(), 'applications', 
                                request.application, 'models',
                                'researchdb.py'])
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