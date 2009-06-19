#still on testing..

def new_account():
    # creating a new user account
    if userdb(userdb.user.username > 0).count() == 0:
        userdb.user.authorized.default = True
    else:
        userdb.user.authorized.default = False
    form = SQLFORM(userdb.user, fields=['username','password'])
    if form.accepts(request.vars,session):
        redirect(URL(r=request, f='log_in'))
    return dict(form=form)    
    
def log_in():
    # function for user to log in
    # compares the user login and password with userdb.user table
    # if login is successful, the username is stored in session.username
    # for further use. If login is not successful, session.username = None
    form = FORM(TABLE(
                    TR("Username:",INPUT(_name="username",
                                         requires=IS_NOT_EMPTY())),
                    TR("Password:",INPUT(_name="password",_type='password',
                                         requires=[IS_NOT_EMPTY()])),
                    TR("",INPUT(_type="submit", _value="login")))) 
    if FORM.accepts(form,request.vars,session):
        if userdb(userdb.user.username == form.vars.username) \
           (userdb.user.password == form.vars.password) \
           (userdb.user.authorized == True).count():
            session.username = form.vars.username
            redirect(URL(r=request, f='logged'))
        else:
            session.username = None
            response.flash = "invalid username/password" 
    return dict(form=form)

def logged():
    # redirection when login is successful
    return dict(name=session.username)

def log_out():
    # set session.username to None when logged out
    session.username = None
    return dict(name=session.username)
