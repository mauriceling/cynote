def input_form():
    if session.username == None: redirect(URL(r=request,f='../account/log_in'))
    form = FORM(TABLE(TR("Sequence: ",TEXTAREA(_name="seq",
               value="Enter your sequence in plain text here. If your sequence is in FASTA format, just remove the comment line.")),
           TR("Option",INPUT(_type="checkbox",_name="option")),
           TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request.vars,session):
        print form.vars.option
        if form.vars.option: session.option = 'checked'
        else: session.option ='unchecked'
        session.seq=form.vars.seq.upper()
        redirect(URL(r=request,f='analysis'))
    return dict(form=form)

def analysis():
    result = {}
    result['seq']=session.pop('seq', None)
    result['option'] = session.option
    result['analysis'] = a1(vars)
    print result
    print session
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(seq=result['seq'],result=result)

def a1(vars): return 'trying'

options = range(5)
          
def multi_input():
    if session.username == None: redirect(URL(r=request,f='../account/log_in'))
    form = FORM(
            TABLE(*[TR('T',INPUT(_type="checkbox",_name='T'))]+\
             [TR("Option "+str(opt), INPUT(_type="checkbox",_name=str(opt),value=False,_value='on')) 
                 for opt in options]+\
             [TR("",INPUT(_type="submit",_value="SUBMIT"))]))             
    opt_list = []
    if form.accepts(request.vars,session):
        session['form_vars'] = form.vars
        option_checked = [opt for opt in form.vars.keys() if form.vars[opt]]
        print option_checked
        redirect(URL(r=request,f='multi_out'))
    return dict(form=form)
    
def multi_out(): 
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(result=session['form_vars'])
