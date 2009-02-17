def index():
    response.flash=T('Welcome to CyNote - A web-enabled notebook compliant with general research record-keeping standard')
    if session.username == None: 
        name = 'Guest'
        redirect(URL(r=request,f='../account/log_in'))
    else: name = session.username
    return dict(name=name, message=T('CyNote Menu'))
