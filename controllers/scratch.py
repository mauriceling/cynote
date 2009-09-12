##################################################################
# holding file for old codes that I may not want to discard yet
##################################################################

def new_entry():
    # from cynote.py
    """
    Create a new entry, if successful, it will redirect to the TOC page 
    (entries function).
    Possible to have duplicate titles
    The author is set to username
    Event is logged in db.log table as "New entry created."
    """
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    cynotedb.entry.author.default = session.username
    form = SQLFORM(cynotedb.entry,
                   fields=['title','file','keywords','notebook','description'])
    if form.accepts(request.vars,session):
        db.log.insert(event='New entry created. %s. Title = %s'% \
                            (cynotedb(
                            cynotedb.notebook.id==request.vars.notebook)\
                            .select(cynotedb.notebook.name),
                            request.vars.title), 
                      user=session.username)
        redirect(URL(r=request, f='entries'))
    return dict(form=form)
    
def archived_entries(): 
    # from cynote.py
    """
    Return the archived notebook itself - Table of contents
    This function re-runs itself. At the first run, records is None;
    hence, does not show the records, only show the form.
    When a notebook was selected, this function will repeat itself
    to give the TOC "records" needs to run before SQLFORM in order to 
    list the notebooks available.
    """
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    else:
        records = cynotedb(cynotedb.entry.notebook == request.vars.notebook) \
            (cynotedb.entry.notebook == cynotedb.notebook.id) \
            (cynotedb.notebook.archived == True) \
            .select(cynotedb.entry.ALL, orderby = ~cynotedb.entry.id) 
        form = SQLFORM(cynotedb.entry, fields=['notebook'])
    return dict(form=form, records=records)
    
def test():
    form = FORM(
            INPUT(_type='file', _name='uploadfile'),
            INPUT(_type='submit', _name='SUBMIT'))
    if form.accepts(request.vars, session):
        #f = open('d:/test.')
        print dir(form.vars.uploadfile)
        print form.vars.uploadfile.filename
    return dict(form=form)