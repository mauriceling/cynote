def entries(): 
    """
    Return the notebook itself - Table of contents
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
            (cynotedb.notebook.archived == False) \
            .select(cynotedb.entry.ALL, orderby = ~cynotedb.entry.id) 
        form = SQLFORM(cynotedb.entry, fields=['notebook'])
    return dict(form=form,
                records=records)
        
def show():
    """
    Called to show one entry and its linked comments based on the entry.id
    Called by TOC (entries or archived_entries) in order to provide an entry.id
    """
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
    """
    Create a new entry, if successful, it will redirect to the TOC page 
    (entries function).
    Only allow new entry creation in unarchived notebooks.
    Possible to have duplicate titles
    The author is set to username
    Event is logged in db.log table as "New entry created."
    """
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    # get unarchived notebooks
    notebook = [notebook['name'] 
                for notebook in cynotedb(cynotedb.notebook.archived == False).\
                    select(cynotedb.notebook.name)]
    notebook.sort()
    form = FORM(TABLE(
            TR('Title: ', INPUT(_type='text', _name='title', _size=80)),
            TR('File: ', INPUT(_type='file', _name='uploadfile')),
            TR('Keywords: ', INPUT(_type='text', _name='keywords', _size=80)),
            TR('Notebook: ', SELECT(notebook, _name='notebook')),
            TR('Description: ', TEXTAREA(_type='text', _name='description'),
            TR('',INPUT(_type='submit', _name='SUBMIT')))))
    if form.accepts(request.vars,session):
        # get notebook.id from notebook.name
        notebook_id=cynotedb(cynotedb.notebook.name == form.vars.notebook).\
                select(cynotedb.notebook.id).as_list()[0]['id']
        if form.vars.uploadfile != '':
            # if there is file to upload
            import os, random, shutil
            upload_dir = os.sep.join([os.getcwd(), 'applications', 
                                    request.application, 'uploads'])
            sourcefile = form.vars.uploadfile.filename
            newfile = upload_dir + os.sep + 'entry.file.' + \
                    str(int(random.random()*10000000000000)) + \
                    os.path.splitext(sourcefile)[-1]
            shutil.copy2(sourcefile, newfile)
            cynotedb.entry.insert(title=form.vars.title,
                              author=session.username,
                              notebook=notebook_id,
                              file=newfile.split(os.sep)[-1],
                              filename=newfile.split(os.sep)[-1],
                              description=form.vars.description)
        else:
            # no file to upload 
            cynotedb.entry.insert(title=form.vars.title,
                              author=session.username,
                              notebook=notebook_id,
                              file='',
                              filename='',
                              description=form.vars.description)
        db.log.insert(event='New entry created. %s. Title = %s'% \
                            (cynotedb(
                            cynotedb.notebook.id==notebook_id)\
                            .select(cynotedb.notebook.name),
                            form.vars.title), 
                      user=session.username)
        redirect(URL(r=request, f='entries'))
    return dict(form=form)
    
def new_notebook():
    """
    Create a new notebook, if successful, it will redirect to the TOC page 
    (entries function).
    Event is logged in db.log table as "New notebook created."
    """
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    form = SQLFORM(cynotedb.notebook, fields=['name','description'])
    if form.accepts(request.vars,session):
        db.log.insert(event='New notebook created. Notebook = ' + 
                    request.vars.name, 
                    user=session.username)
        redirect(URL(r=request,f='entries'))
    return dict(form=form)
    
def download():
    """
    Called by cynote.show() function
    Used to stream a file from uploads directory 
    request.args[0] given by an entry (entry.filename) or a comment 
    (comment.filename)
    """
    import os
    import gluon.contenttype
    filename = request.args[0]
    response.headers['Content-Type'] = gluon.contenttype.contenttype(filename)
    file = os.path.join(request.folder, 'uploads/',  filename)
    return response.stream(file)
      
def notarize_bysystem():
    """
    Function to bulk notarize all entries by inserting a notarization comment
    for each entry.
    """
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
    """
    User to notarize one entry
    User identified during login
    Redirected to TOC page (entries function)
    """
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
    """
    Show the contents of cynotedb.result table 
    cynotedb.result table stores results from analysis functions
    Generates a form to allow user to show a specific result for saving into a 
    new entry
    """
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
    # get unarchived notebooks
    notebook = [notebook['name'] 
                for notebook in cynotedb(cynotedb.notebook.archived == False).\
                    select(cynotedb.notebook.name)]
    notebook.sort()
    form = FORM(TABLE(
            TR('Title: ', INPUT(_type='text', _name='title', _size=80)),
            TR('File: ', INPUT(_type='file', _name='uploadfile')),
            TR('Keywords: ', INPUT(_type='text', _name='keywords', _size=80)),
            TR('Notebook: ', SELECT(notebook, _name='notebook')),
            TR('Description: ', TEXTAREA(_type='text', _name='description'),
            TR('',INPUT(_type='submit', _name='SUBMIT')))))
    if form.accepts(request.vars,session):
        # get notebook.id from notebook.name
        notebook_id=cynotedb(cynotedb.notebook.name == form.vars.notebook).\
                select(cynotedb.notebook.id).as_list()[0]['id']
        if form.vars.uploadfile != '':
            # if there is file to upload
            import os, random, shutil
            upload_dir = os.sep.join([os.getcwd(), 'applications', 
                                    request.application, 'uploads'])
            sourcefile = form.vars.uploadfile.filename
            newfile = upload_dir + os.sep + 'entry.file.' + \
                    str(int(random.random()*10000000000000)) + \
                    os.path.splitext(sourcefile)[-1]
            shutil.copy2(sourcefile, newfile)
            cynotedb.entry.insert(title=form.vars.title,
                              author=session.username,
                              notebook=notebook_id,
                              file=newfile.split(os.sep)[-1],
                              filename=newfile.split(os.sep)[-1],
                              description=form.vars.description)
        else:
            # no file to upload 
            cynotedb.entry.insert(title=form.vars.title,
                              author=session.username,
                              notebook=notebook_id,
                              file='',
                              filename='',
                              description=form.vars.description)
        db.log.insert(event='New entry created. %s. Title = %s'% \
                            (cynotedb(
                            cynotedb.notebook.id==notebook_id)\
                            .select(cynotedb.notebook.name),
                            form.vars.title), 
                      user=session.username)
        cynotedb(cynotedb.result.id == id).delete()
        redirect(URL(r=request, f='entries'))
    return dict(result=session['form_vars'],
                test=test,
                form=form)

def archive_notebook(): 
    """
    Function to archive one or more notebooks.
    Event is logged in db.log table as "Notebook archived."
    """  
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
        option_checked = [id['name']
                          for id['name'] in form.vars.keys()
                          if form.vars[id['name']]]
        for notebook in option_checked:
            db.log.insert(event='Notebook archived. Notebook = ' + notebook, 
                          user=session.username)
            cynotedb(cynotedb.notebook.name == notebook).update(archived=True)
        redirect(URL(r=request, f='archive_notebook'))
    return dict(form=form)

def unarchive_notebook():  
    """
    Function to unarchive one or more previously notebooks.
    Event is logged in db.log table as "Notebook unarchived."
    """ 
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
        option_checked = [id['name']
                          for id['name'] in form.vars.keys()
                          if form.vars[id['name']]]
        for notebook in option_checked:
            db.log.insert(event='Notebook unarchived. Notebook = ' + notebook, 
                          user=session.username)
            cynotedb(cynotedb.notebook.name == notebook).update(archived=False)
        redirect(URL(r=request, f='unarchive_notebook'))
    return dict(form=form)

