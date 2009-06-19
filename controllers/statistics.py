from applications.init.modules.copads.SampleStatistics import MultiSample

def input_form():
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(
            TABLE(
                TR("Data: ",
                    TEXTAREA(_name="data",
                    value="""Enter the data, separated by commas, for analysis""")),
                TR("Is the first row represents the Sample name? ",
                   SELECT("YES", "NO", _name="sample_name")),
                TR("Type of Analysis: ",
                   SELECT("Descriptive Statistics",
                          _name="analysis_type")),
                TR("", INPUT(_type="submit", _value="SUBMIT"))))
    if form.accepts(request.vars,session):
        if form.vars.sample_name == 'YES':
            session.sample_name = 'YES'
        else: session.sample_name = 'NO'
        session.analysis_type = form.vars.analysis_type
        session.data = parse_data(form.vars.data, session.sample_name)
        redirect(URL(r=request, f='analysis'))
    return dict(form=form)

def parse_data(data, name):
    dataset = MultiSample()
    data = [x.split(',') for x in data.split('\r\n')]
    if name == 'YES':
        session.sample_name = data.pop(0)
    else: 
        session.sample_name = ['Sample ' + str(x) 
                                for x in range(len(data[0]))]
    for index in range(len(session.sample_name)):
        dataset.addSample([float(row[index]) for row in data],
                          name = session.sample_name[index])
    return dataset

def analysis():
    result = {}
    result['data'] = str(session.pop('data', None))
    result['sample_name'] = session.pop('sample_name', None)
    result['analysis_type'] = session.pop('analysis_type', None)
    result['results'] = a1(vars)
    print result
    print session
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(result=result)

def a1(vars): return 'trying'
