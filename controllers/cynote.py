def entries(): 
    # return the notebook itself - Table of contents
    # This function re-runs itself. At the first run, records is None;
    # hence, does not show the records, only show the form.
    # When a notebook was selected, this function will repeat itself
    # to give the TOC
    # "records" needs to run before SQLFORM in order to list the 
    # notebooks available
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    else:
        records = cynotedb(cynotedb.entry.notebook == request.vars.notebook) \
            (cynotedb.entry.notebook == cynotedb.notebook.id) \
            (cynotedb.notebook.archived == False) \
            .select(cynotedb.entry.ALL, orderby = ~cynotedb.entry.id) 
        form = SQLFORM(cynotedb.entry ,fields=['notebook'])
    return dict(form=form,
                records=records)

def archived_entries(): 
    # return the archived notebook itself - Table of contents
    # This function re-runs itself. At the first run, records is None;
    # hence, does not show the records, only show the form.
    # When a notebook was selected, this function will repeat itself
    # to give the TOC
    # "records" needs to run before SQLFORM in order to list the 
    # notebooks available
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    else:
        records = cynotedb(cynotedb.entry.notebook == request.vars.notebook) \
            (cynotedb.entry.notebook == cynotedb.notebook.id) \
            (cynotedb.notebook.archived == True) \
            .select(cynotedb.entry.ALL, orderby = ~cynotedb.entry.id) 
        form = SQLFORM(cynotedb.entry, fields=['notebook'])
    return dict(form=form,
                records=records)
        
def show():
    # called to show one entry and its linked comments based on 
    # the entry.id
    # called by TOC in order to provide an entry.id
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    else: 
        id = request.args[0]
    entries = cynotedb(cynotedb.entry.id == id).select()
    # to prevent showing a 'None' (null) entry
    if not len(entries):
        redirect(URL(r=request, f='entries'))  
    # form to post new comments
    #the author is set to username
    cynotedb.comment.author.default = session.username
    comments = SQLFORM(cynotedb.comment, fields=['file','body'])
    # give entry.id for comment output
    comments.vars.entry_id = id;
    # return the comment that is listed with the entry id 
    records = cynotedb(cynotedb.comment.entry_id == id) \
              .select(orderby = cynotedb.comment.entry_id)
    # show a flash when comment is posted
    if comments.accepts(request.vars,session): 
         response.flash = "comment posted"
         db.log.insert(event='New comment created. %s' % \
                            (cynotedb(cynotedb.entry.id==id)\
                            .select(cynotedb.entry.title)), 
                      user=session.username)
         # refresh page after adding a comment by calling itself (show)
         redirect(URL(r=request, f='show', args=[id]))                 
    return dict(entry=entries[0],
                comments=comments,
                records=records)
    
def new_entry():
    # create a new entry, if successful, it will redirect to the TOC
    # page (entries function).
    # Possible to have duplicate titles
    #the author is set to username
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    cynotedb.entry.author.default = session.username
    form = SQLFORM(cynotedb.entry,
                   fields=['title','file','keywords','notebook','description'])
    if form.accepts(request.vars,session):
        db.log.insert(event='New entry created. %s. Title = %s'% \
                            (cynotedb(cynotedb.notebook.id==request.vars.notebook)\
                            .select(cynotedb.notebook.name),
                            request.vars.title), 
                      user=session.username)
        redirect(URL(r=request, f='entries'))
    return dict(form=form)
    
def new_notebook():
    # create a new notebook, if successful, it will redirect to the TOC
    # page (entries function).
    # Not possible to have duplicate notebook titles
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    form = SQLFORM(cynotedb.notebook, fields=['name','description'])
    if form.accepts(request.vars,session):
        db.log.insert(event='New notebook created. Notebook = ' + request.vars.name, 
                      user=session.username)
        redirect(URL(r=request,f='entries'))
    return dict(form=form)
    
def download():
    # called by cynote.show() function
    # used to stream a file from uploads directory 
    # request.args[0] given by an entry (entry.filename) 
    # or a comment (comment.filename)
    import os
    import gluon.contenttype
    filename = request.args[0]
    response.headers['Content-Type'] = gluon.contenttype.contenttype(filename)
    file = os.path.join(request.folder, 'uploads/',  filename)
    return response.stream(file)
      
def notarize_bysystem(username=None):
    # function to bulk notarize all entries by inserting a notarization comment
    # for each entry
    session.username = username
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    for entry_id in cynotedb().select(cynotedb.entry.id):
        id = entry_id['id']
        cynotedb.comment.insert(author='system',
                                body='notarize by system',
                                entry_id=id)
    cynotedb.commit()
    
def notarize_bymanual():
    # user to notarize one entry
    # user identified during login
    # redirected to TOC page (entries function)
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    cynotedb.comment.body.default = 'Notarize'
    cynotedb.comment.file.default = ''
    cynotedb.comment.author.default = session.username 
    comments = SQLFORM(cynotedb.comment, fields=['entry_id'])
    if comments.accepts(request.vars,session):
        redirect(URL(r=request, f='entries'))
    return dict(comments=comments)

def results(): 
    # show the contents of cynotedb.result table
    # cynotedb.result table stores results from analysis functions
    # generates a form to allow user to show a specific result for 
    # saving into a new entry
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    records = cynotedb(cynotedb.result.id == cynotedb.result.id) \
              (cynotedb.result.author == session.username) \
              .select(orderby = cynotedb.result.id)
    form = FORM(
            TABLE(
                *[TR("Result "+str(id['id']),
                     INPUT(_type="checkbox",
                           _name=str(id['id']),
                           value=False,_value='on'))
                  for id in cynotedb(cynotedb.result.author == \
                                     session.username) \
                                    .select(cynotedb.result.id)] + \
             [TR("",INPUT(_type="submit", _value="SUBMIT"))]))       
    id_list = []
    if form.accepts(request.vars,session):
        session['form_vars'] = form.vars
        option_checked = [id['id']
                          for id['id']in form.vars.keys()
                          if form.vars[id['id']]]
        session.option_checked = option_checked
        redirect(URL(r=request, f='show_results')) 
    return dict(records=records,
                form=form)
    
def show_results(): 
    # called by results() function to show a specific result and 
    # to generate a form to save the result as a new entry
    # the result will be deleted after a new entry had been created
    option_checked = session.option_checked
    if len(option_checked) == 0: id = 0 
    else: id = option_checked[0]
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

def archive_notebook():   
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))          
    form = FORM(
            TABLE(*[TR(""+str(id['name']), 
                INPUT(_type="checkbox", _name=str(id['name']),
                      value=False, _value='on'))
            for id in cynotedb(cynotedb.notebook.archived == "False") \
                    .select(cynotedb.notebook.name)] + \
            [TR("",INPUT(_type="submit", _value="Archive"))]))    
    if form.accepts(request.vars,session):
        for notebook in form.vars.keys():
            cynotedb(cynotedb.notebook.name == notebook).update(archived=True)
        redirect(URL(r=request, f='archive_notebook'))
    return dict(form=form)

def unarchive_notebook():  
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))           
    form = FORM(
            TABLE(*[TR(""+str(id['name']), 
                INPUT(_type="checkbox", _name=str(id['name']),
                      value=False, _value='on'))
            for id in cynotedb(cynotedb.notebook.archived == "True") \
                    .select(cynotedb.notebook.name)] + \
            [TR("",INPUT(_type="submit", _value="Unarchive"))]))    
    if form.accepts(request.vars,session):
        for notebook in form.vars.keys():
            cynotedb(cynotedb.notebook.name == notebook).update(archived=False)
        redirect(URL(r=request, f='unarchive_notebook'))
    return dict(form=form)

def my_exporter(): 
    #response.headers['Content-Type'] = 'text/x-csv' 
    #response.headers['Content-Disposition'] = 'attachment'
    return [dict(x)
            for x in (cynotedb(cynotedb.notebook.name == 'Manuscript Reviews') \
               .select(cynotedb.entry.ALL))]
