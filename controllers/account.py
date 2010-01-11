#still on testing..

from hashlib import sha512 as h

def new_account():
    """
    Creating a new user account
    """
    if userdb(userdb.user.username > 0).count() == 0: authorized = True
    else: authorized = False
    form = FORM(TABLE(
                TR('Username:', INPUT(_name='username',
                                    requires=IS_NOT_EMPTY())),
                TR('Password:', INPUT(_name='password', _type='password',
                                    requires=[IS_NOT_EMPTY()])),
                TR('Re-enter Password:', INPUT(_name='password2', 
                                    _type='password',
                                    requires=[IS_NOT_EMPTY()])),
                TR('', INPUT(_type='submit', _value='login')))) 
    if form.accepts(request.vars, session):
        if form.vars.password != form.vars.password2:
            response.flash = 'Passwords do not match'
        else:
            userdb.user.insert(username=form.vars.username,
                               password=h(form.vars.password).hexdigest(),
                               authorized=authorized)
            db.user_event.insert(event='New account created. %s' % \
                                 form.vars.username, 
                                 user='system')
            redirect(URL(r=request, f='log_in'))
    return dict(form=form)    
    
def log_in():
    """
    Function for user to log in
    Compares the user login and password with userdb.user table
    If login is successful, the username is stored in session.username
    for further use. If login is not successful, session.username = None
    """
    # i = 0
    # while i < 3:
    form = FORM(TABLE(
                TR('Username:', INPUT(_name='username',
                                    requires=IS_NOT_EMPTY())),
                TR('Password:', INPUT(_name='password', _type='password',
                                    requires=[IS_NOT_EMPTY()])),
                TR('', INPUT(_type='submit', _value='login')))) 
    if form.accepts(request.vars, session):
        if userdb(userdb.user.username == form.vars.username) \
           (userdb.user.password == form.vars.password) \
           (userdb.user.authorized == True).count():
            session.username = form.vars.username
            db.user_event.insert(event='Login (plain text password). %s' % \
                                 session.username, 
                                 user='system')
            # converting plaintext password to hash
            userdb(userdb.user.username == form.vars.username). \
            update(password=h(form.vars.password).hexdigest())
            db.log.insert(event='Convert plain password to hash. \User = ' + \
                          form.vars.username, user='system')
            redirect(URL(r=request, f='logged'))
        elif userdb(userdb.user.username == form.vars.username) \
             (userdb.user.password == h(form.vars.password).hexdigest()) \
             (userdb.user.authorized == True).count():
            session.username = form.vars.username
            db.user_event.insert(event='Login (hashed password). %s' % \
                                 session.username, 
                                 user='system')
            redirect(URL(r=request, f='logged'))
        else:
            #session.username = form.vars.username
            session.username = none
            response.flash = 'invalid username/password'
            # i = i + 1
      #if i > 2
      #    userdb(session.username == user).update(authorized=False)      
             
    return dict(form=form)

def logged():
    """redirection when login is successful"""
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
    if form.accepts(request.vars, session):
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
    if form.accepts(request.vars, session):
        option_checked = [id['name']
                          for id['name'] in form.vars.keys()
                          if form.vars[id['name']]]
        for user in option_checked:
            db.log.insert(event='User de-authorized. User = ' + user, 
                          user=session.username)
            userdb(userdb.user.username == user).update(authorized=False)
    return dict(form=form)
