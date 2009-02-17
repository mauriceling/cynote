def form():
    if session.username == None: redirect(URL(r=request,f='../account/log_in'))
    form=SQLFORM(emaildb.message,fields=['your_name','your_email','your_message'])
    if form.accepts(request.vars,session):
       subject='cfgroup message from '+form.vars.your_name
       email_user(sender=form.vars.your_email,\
                  message=form.vars.your_message,\
                  subject=subject)
       response.flash='your message has been submitted'
    elif form.errors:
       response.flash='please check the form and try again'
    return dict(top_message=TOP_MESSAGE,form=form)
