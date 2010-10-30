#still on testing..
from time import time
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
                               aging=time(),
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
    form = FORM(TABLE(
                TR('Username:', INPUT(_name='username',
                                    requires=IS_NOT_EMPTY())),
                TR('Password:', INPUT(_name='password', _type='password',
                                    requires=[IS_NOT_EMPTY()])),
                TR('', INPUT(_type='submit', _value='login')))) 
    if form.accepts(request.vars, session):
        if userdb(userdb.user.username == form.vars.username) \
             (userdb.user.password == h(form.vars.password).hexdigest()) \
             (userdb.user.authorized == True).count():
            session.username = form.vars.username
            db.user_event.insert(event='Login (hashed password). %s' % \
                                 session.username, 
                                 user='system')
            session.login_count = 1
            redirect(URL(r=request, f='logged'))
        # Legacy management #1 - convert all plain text logins to hash
        elif userdb(userdb.user.username == form.vars.username) \
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
            session.login_count = 1
            redirect(URL(r=request, f='logged'))
        # end of Legacy management # 1
        else:
            db.user_event.insert(event='Login error. Username used = %s. \
            Password used = %s. Login count = %s' % 
            (form.vars.username, form.vars.password, str(session.login_count)), 
            user='system')
            session.username = None
            response.flash = 'invalid username/password'
            session.login_count = session.login_count + 1
            # if session.login_count == 5:
                # db.user_event.insert(event='5 times login error. All users are \
                # deauthorized by system.', user='system')
                # [userdb(userdb.user.username == name).update(authorized=False)
                 # for name in userdb(userdb.user.authorized==True).select(userdb.user.username)]
    return dict(form=form)
    
def change_password():
    """Allows a user to change password"""
    if session.username == None:
        redirect(URL(r=request, f='log_in'))
    if session.pwdaged:
        response.flash = 'Current password is older than 90 days. Please change'
    form = FORM(TABLE(
                TR('Username:', INPUT(_name='username',
                                    requires=IS_NOT_EMPTY())),
                TR('Current Password: ', INPUT(_name='oldpwd', _type='password', 
                                            requires=[IS_NOT_EMPTY()])),
                TR('New Password: ',INPUT(_name='newpwd', _type='password',
                                            requires=[IS_NOT_EMPTY()])),
                TR('Re-enter New Password: ', INPUT(_name='newpwd2',
                                _type='password', requires=[IS_NOT_EMPTY()])),
                TR('',INPUT(_type='submit', _name='submit'))))
    if form.accepts(request.vars, session):
        if userdb(userdb.user.username == form.vars.username) \
             (userdb.user.password == h(form.vars.oldpwd).hexdigest()) \
             (userdb.user.authorized == True).count():
            db.user_event.insert(event='Change password initiated. %s' % \
                                 form.vars.username, 
                                 user='system')
            if form.vars.newpwd == form.vars.newpwd2:            
                 userdb(userdb.user.username == session.username) \
                 .update(password=h(form.vars.newpwd).hexdigest())
                 userdb(userdb.user.username == session.username) \
                 .update(aging=time())
                 db.user_event.insert(event='Change password successful. %s' % \
                                 form.vars.username, 
                                 user='system')
                 response.flash = 'Password change SUCCESSFUL'
            else:
                db.user_event.insert(event='Change password unsuccessful. \
                New passwords do not match. %s' % \
                                 form.vars.username, 
                                 user='system')
                response.flash = 'Password change UNSUCCESSFUL - New passwords \
                do not match'
        else:
            db.user_event.insert(event='Change password unsuccessful. \
            Current password does not match. %s' % \
                                 form.vars.username, 
                                 user='system')
            response.flash = 'Password change UNSUCCESSFUL - Current password \
            does not match'
    return dict(form=form)
 
def logged():
    """redirection when login is successful"""
    session.login_time = time()
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
