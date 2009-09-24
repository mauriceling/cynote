#still on testing..

def new_account():
    """
    Creating a new user account
    """
    if userdb(userdb.user.username > 0).count() == 0:
        userdb.user.authorized.default = True
    else:
        userdb.user.authorized.default = False
    form = SQLFORM(userdb.user, fields=['username','password'])
    if form.accepts(request.vars,session):
        redirect(URL(r=request, f='log_in'))
    return dict(form=form)    
    
def log_in():
    """
    Function for user to log in
    Compares the user login and password with userdb.user table
    If login is successful, the username is stored in session.username
    for further use. If login is not successful, session.username = None
    """
    form = FORM(TABLE(
                TR('Username:', INPUT(_name='username',
                                    requires=IS_NOT_EMPTY())),
                TR('Password:', INPUT(_name='password', _type='password',
                                    requires=[IS_NOT_EMPTY()])),
                TR('', INPUT(_type='submit', _value='login')))) 
    if FORM.accepts(form,request.vars,session):
        if userdb(userdb.user.username == form.vars.username) \
           (userdb.user.password == form.vars.password) \
           (userdb.user.authorized == True).count():
            session.username = form.vars.username
            db.user_event.insert(event='Login. %s' % \
                                 session.username, 
                                 user='system')
            redirect(URL(r=request, f='logged'))
        else:
            session.username = None
            response.flash = 'invalid username/password' 
    return dict(form=form)

def logged():
    """edirection when login is successful"""
    return dict(name=session.username)

def log_out():
    """Set session.username to None when logged out"""
    db.user_event.insert(event='Logout. %s' % \
                         session.username, 
                         user='system')
    session.username = None
    return dict(name=session.username)

def auth_new_user():
    """
    Function to authorize newly signed-up users.
    """
    if session.username == None:
        redirect(URL(r=request, f='log_in'))          
    form = FORM(
            TABLE(*[TR('' + str(id['username']), 
                    INPUT(_type='checkbox', _name=str(id['username']),
                          value=False, _value='on'))
            for id in userdb(userdb.user.authorized == 'False') \
                    .select(userdb.user.username)] + \
            [TR('', INPUT(_type='submit', _value='Authorize User'))])) 
    if form.accepts(request.vars,session):
        option_checked = [id['name']
                          for id['name'] in form.vars.keys()
                          if form.vars[id['name']]]
        for user in option_checked:
            db.log.insert(event='User authorized. User = ' + user, 
                          user=session.username)
            userdb(userdb.user.username == user).update(authorized=True)
    return dict(form=form)
    
def deauth_user():
    """
    Function to de-authorize users.
    """
    if session.username == None:
        redirect(URL(r=request, f='log_in'))          
    form = FORM(
            TABLE(*[TR('' + str(id['username']), 
                    INPUT(_type='checkbox', _name=str(id['username']),
                          value=False, _value='on'))
            for id in userdb(userdb.user.authorized == 'True') \
                    .select(userdb.user.username)] + \
            [TR('', INPUT(_type='submit', _value='De-authorize User'))])) 
    if form.accepts(request.vars,session):
        option_checked = [id['name']
                          for id['name'] in form.vars.keys()
                          if form.vars[id['name']]]
        for user in option_checked:
            db.log.insert(event='User de-authorized. User = ' + user, 
                          user=session.username)
            userdb(userdb.user.username == user).update(authorized=False)
    return dict(form=form)
