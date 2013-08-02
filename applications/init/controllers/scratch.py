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
        redirect(URL(r=request, c='account', f='log_in'))
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

def show_results():
    # from cynote.py 
    """
    Called by results() function to show a specific result and 
    to generate a form to save the result as a new entry
    the result will be deleted after a new entry had been created.
    """
    option_checked = session.option_checked
    if len(option_checked) == 0: 
        id = 0 
    else: 
        id = option_checked[0]
    test = cynotedb(cynotedb.result.id == id).select()
    #the author is set to username
    cynotedb.entry.author.default = session.username    
    form = SQLFORM(cynotedb.entry,
                   fields = ['title','file','keywords',
                             'notebook','description'])
    if form.accepts(request.vars,session):
        cynotedb(cynotedb.result.id == id).delete()
        redirect(URL(r=request, f='entries'))
    return dict(result=session['form_vars'],
                test=test,
                form=form)
    #return dict(option_checked=option_checked)
        


def test():
    form = FORM(
            INPUT(_type='file', _name='uploadfile'),
            INPUT(_type='submit', _name='SUBMIT'))
    if form.accepts(request.vars, session):
        #f = open('d:/test.')
        print dir(form.vars.uploadfile)
        print form.vars.uploadfile.filename
    return dict(form=form)
    
def twobuttonform(): 
    form=FORM(INPUT(_type='hidden',_name='action',_id='action',_value='undefined'), 
              INPUT(_type='button',_value='Do something',
                    _onclick='''this.form.action.value=1;this.form.submit();''',), 
              INPUT(_type='button',_value='Do something else',
                    _onclick='''this.form.action.value=2;this.form.submit();''',), 
            ) 
    if form.accepts(request.vars): 
        response.flash='You clicked button %s'%request.vars.action 
    return dict(form=form)
