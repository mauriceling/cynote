import time
from ez_setup import use_setuptools
use_setuptools()
from setuptools.command.easy_install import main

exec('from applications.%s.controllers.option import *' % (request.application))

tabs = {'bioinformatics': 'Bioinformatics Tools',
        'statistics': 'Statistical Analysis',
        'adhocDB': 'Ad hoc Research Database',
        #'citation': 'Citations',
        #'projects': 'Projects and Resources',
        #'goals': 'Personal Goals',
        #'assistants': 'Assistants and Tutors', 
        }
        
if not session.has_key('login_count'): session.login_count = 0

def password_aging(username, password_age=password_age):
    current_time = int(time.time())
    last_password_change = userdb(userdb.user.username == username) \
                           .select(userdb.user.aging)[0]['aging']
    # print current_time, last_password_change
    if last_password_change == None or \
    last_password_change + (password_age * 24 * 3600) < current_time:
        db.user_event.insert(event='Password aged > 90 days. %s' % \
            session.username, 
            user='system')
        return True
    else: 
        return False

def check_login(session=session):
    if session.login_time == None: 
        session.login_time = 0
    if session.username == None or \
        session.login_time + login_expiry * 3600 < int(time.time()): 
        redirect(URL(r=request, f='../account/log_in'))
    else: 
        return session.username

def index():
    try: session['dependencies']
    except KeyError: session['dependencies'] = 'NOT DONE'
    if session['dependencies'] != 'DONE':
        for dependency in cynote_dependencies:
            try: 
                main([dependency])
            except KeyError: 
                print dependency + ' installation error'
            except: 
                print dependency + ' generic error (please inform Maurice Ling)'
            session['dependencies'] = 'DONE'
    response.flash = cynote_header
    name = check_login()
    if password_aging(session.username) == True:
        session.pwdaged = True
        redirect(URL(r=request, f='../account/change_password'))
    return dict(module='default', tab_list=tabs, name=name, 
                version=version, copyright=copyright,
                message=T('CyNote Main Menu'))
    
def bioinformatics():
    response.flash = cynote_header
    name = check_login()
    return dict(module='default', tab_list=tabs, name=name, 
                copyright=copyright,
                message=T('CyNote - Bioinformatics Menu'))

def statistics():
    response.flash = cynote_header
    name = check_login()
    return dict(module='default', tab_list=tabs, name=name, 
                copyright=copyright,
                message=T('CyNote - Statistics Menu'))
                
def adhocDB():
    response.flash = cynote_header
    name = check_login()
    return dict(module='default', tab_list=tabs, name=name, 
                copyright=copyright,
                message=T('CyNote - Ad hoc Research Database Menu'))

def assistants():
    response.flash = cynote_header
    name = check_login()
    return dict(module='default', tab_list=tabs, name=name, 
                copyright=copyright,
                message=T('CyNote - Assistants and Tutors'))
