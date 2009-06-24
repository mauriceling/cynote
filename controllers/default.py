tabs = [{'module': 'default', 'function': 'bioinformatics', 'name': 'Bioinformatics Tools'},
        {'module': 'default', 'function': 'statistics', 'name': 'Statistical Analyses'},]

def index():
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
