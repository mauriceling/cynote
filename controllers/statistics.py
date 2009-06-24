exec("""from applications.%s.modules.copads.SampleStatistics \
import SingleSample""" % (request.application))

#######################################################################
# Single Sample (SS)
#######################################################################
def input_SS():
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(
            TABLE(
                TR("Data: ",
                    TEXTAREA(_name="data",
                    value="""Enter the data, separated by commas, for analysis.""")),   
                TR("", INPUT(_type="submit", _value="SUBMIT"))))
    if form.accepts(request.vars,session):
        session.data = [float(x) for x in form.vars.data.split(',')]
        redirect(URL(r=request, f='analyze_SS'))
    return dict(form=form)
    
def analyze_SS():
    result = {}
    result['data'] = session.pop('data', [])
    sample = SingleSample(data=result['data'], name='')
    #print sample
    result['results'] = sample.summary
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(result=result)

def a1(vars): return 'trying'

#######################################################################
# Single Sample (SS) - End
#######################################################################

#######################################################################
# Two Samples (TS)
#######################################################################
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
    
def two_samples_input():
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(
            TABLE(
                TR("Data: ",
                    TEXTAREA(_name="data",
                    value="""Enter the data, separated by commas, for analysis.""")),
                TR("Type of Analysis: ",
                   SELECT('Paired Z-test',
                          '2-sample Z-test',
                          'Paired t-test',
                          '2-sample t-test',
                          "Pearson's Correlation",
                          "Spearman's Correlation",
                          'Linear regression',
                          _name="analysis_type")),
                TR("", INPUT(_type="submit", _value="SUBMIT"))))
    if form.accepts(request.vars,session):
        session.analysis_type = form.vars.analysis_type
        session.data = [float(x) for x in form.vars.data.split(',')]
        redirect(URL(r=request, f='analysis'))
    return dict(form=form)
    
#######################################################################
# Two Samples (TS) - End
#######################################################################

#######################################################################
# More than Two Samples (MS)
#######################################################################

#######################################################################
# More than Two Samples (MS) - End
#######################################################################
