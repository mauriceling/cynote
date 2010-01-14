from ez_setup import use_setuptools
use_setuptools()
from setuptools.command.easy_install import main

tabs = [{'module': 'default', 'function': 'bioinformatics', 
            'name': 'Bioinformatics Tools'},
        {'module': 'default', 'function': 'statistics', 
            'name': 'Statistical Analyses'},
        #{'module': 'default', 'function': 'citation', 
        #    'name': 'Citations Manager'},
        #{'module': 'default', 'function': 'projects', 
        #    'name': 'Project Tools'},
        #{'module': 'default', 'function': 'goals', 
        #    'name': 'Personal Goals'},
        #{'module': 'default', 'function': 'assistants', 
        #    'name': 'Assistants and Tutors'}, 
        ]

password_age = 30   # 30 days

cynote_dependencies = ['biopython==1.50',
                       'pil==1.1.6']

if not session.has_key('login_count'): session.login_count = 0

def password_aging(username, password_age=password_age):
    import time
    current_time = int(time.time())
    last_password_change = userdb(userdb.user.username == username) \
                           .select(userdb.user.aging)[0]['aging']
    print current_time, last_password_change
    if last_password_change == None or \
    last_password_change + (password_age * 24 * 3600) < current_time:
        db.user_event.insert(event='Password aged > 30 days. %s' % \
            session.username, 
            user='system')
        return True
    else: 
        return False

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
    response.flash = T('Welcome to CyNote - A web-enabled notebook compliant \
    with general research record-keeping standard (US FDA 21 CFR Part 11)')
    if session.username == None: 
        name = 'Guest'
        session.pwdaged = False
        redirect(URL(r=request, f='../account/log_in'))
    elif password_aging(session.username) == True:
        session.pwdaged = True
        redirect(URL(r=request, f='../account/change_password'))
    else: 
        name = session.username
    return dict(tab_list=tabs, name=name, message=T('CyNote Main Menu'))
    
def bioinformatics():
    response.flash = T('Welcome to CyNote - A web-enabled notebook compliant \
    with general research record-keeping standard (US FDA 21 CFR Part 11)')
    if session.username == None: 
        name = 'Guest'
        redirect(URL(r=request, f='../account/log_in'))
    else: 
        name = session.username
    return dict(tab_list=tabs, name=name, 
                message=T('CyNote - Bioinformatics Menu'))

def statistics():
    response.flash = T('Welcome to CyNote - A web-enabled notebook compliant \
    with general research record-keeping standard (US FDA 21 CFR Part 11)')
    if session.username == None: 
        name = 'Guest'
        redirect(URL(r=request, f='../account/log_in'))
    else: 
        name = session.username
    return dict(tab_list=tabs, name=name, 
                message=T('CyNote - Statistics Menu'))

def assistants():
    response.flash = T('Welcome to CyNote - A web-enabled notebook compliant \
    with general research record-keeping standard (US FDA 21 CFR Part 11)')
    if session.username == None: 
        name = 'Guest'
        redirect(URL(r=request, f='../account/log_in'))
    else: 
        name = session.username
    return dict(tab_list=tabs, name=name, 
                message=T('CyNote - Assistants and Tutors'))
