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

cynote_dependencies = ['biopython==1.50',
                       'pil==1.1.6']

if not session.has_key('login_count'): session.login_count = 0

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
        redirect(URL(r=request, f='../account/log_in'))
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
