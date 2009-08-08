from ez_setup import use_setuptools
use_setuptools()
from setuptools.command.easy_install import main

tabs = [{'module': 'default', 'function': 'bioinformatics', 'name': 'Bioinformatics Tools'},
        {'module': 'default', 'function': 'statistics', 'name': 'Statistical Analyses'},
        #{'module': 'default', 'function': 'assistants', 'name': 'Assistants and Tutors'}, 
        ]

cynote_dependencies = ['biopython==1.50',
                       'pil==1.1.6']

def index():
    for dependency in cynote_dependencies:
        try: main([dependency])
        except KeyError: print dependency + " installation error"
        except: print dependency + " generic error (please inform Maurice Ling)"
    response.flash=T('Welcome to CyNote - A web-enabled notebook compliant with general research record-keeping standard')
    if session.username == None: 
        name = 'Guest'
        redirect(URL(r=request,f='../account/log_in'))
    else: name = session.username
    return dict(tab_list = tabs, name=name, message=T('CyNote Main Menu'))
    
def bioinformatics():
    response.flash=T('Welcome to CyNote - A web-enabled notebook compliant with general research record-keeping standard')
    if session.username == None: 
        name = 'Guest'
        redirect(URL(r=request,f='../account/log_in'))
    else: name = session.username
    return dict(tab_list = tabs, name=name, message=T('CyNote - Bioinformatics Menu'))

def statistics():
    response.flash=T('Welcome to CyNote - A web-enabled notebook compliant with general research record-keeping standard')
    if session.username == None: 
        name = 'Guest'
        redirect(URL(r=request,f='../account/log_in'))
    else: name = session.username
    return dict(tab_list = tabs, name=name, message=T('CyNote - Statistics Menu'))

def assistants():
    response.flash=T('Welcome to CyNote - A web-enabled notebook compliant with general research record-keeping standard')
    if session.username == None: 
        name = 'Guest'
        redirect(URL(r=request,f='../account/log_in'))
    else: name = session.username
    return dict(tab_list = tabs, name=name, message=T('CyNote - Assistants and Tutors'))
