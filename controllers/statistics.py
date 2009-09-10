exec("""from applications.%s.modules.copads.SampleStatistics \
import SingleSample""" % (request.application))
exec("""from applications.%s.modules.copads.SampleStatistics \
import MultiSample""" % (request.application))

#######################################################################
# Single Sample (SS)
#######################################################################
def input_SS():
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(
            TABLE(
                TR('Data: ', TEXTAREA(_name='data',
                    value='Enter the data, separated by commas')),   
                INPUT(_type='submit', _value='SUBMIT')))
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

#######################################################################
# Single Sample (SS) - End
#######################################################################

#######################################################################
# Two Samples (TS)
#######################################################################
def input_TS():
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(
            TABLE(
                TR('Name #1: ', INPUT(_name='name1', value='Enter name')),
                TR('Data #1: ', TEXTAREA(_name='data1',
                    value='Enter the data, separated by commas')),
                TR('Name #2: ', INPUT(_name='name2', value='Enter name')),
                TR('Data #2: ', TEXTAREA(_name='data2',
                    value='Enter the data, separated by commas')),
                TR('Type of Analysis: ',
                   SELECT('Paired Z-test',
                          '2-sample Z-test',
                          'Paired t-test',
                          '2-sample t-test',
                          "Pearson's Correlation",
                          "Spearman's Correlation",
                          'Linear regression',
                          'Distance measure',
                          _name='analysis_type'),
                   INPUT(_type='submit', _value='SUBMIT'))))
    if form.accepts(request.vars,session):
        session.analysis_type = form.vars.analysis_type
        session.data1 = [float(x) for x in form.vars.data1.split(',')]
        session.data2 = [float(x) for x in form.vars.data2.split(',')]
        session.name1 = form.vars.name1
        session.name2 = form.vars.name2
        redirect(URL(r=request, f='analyse_TS'))
    return dict(form=form)
    
def analyze_TS():
    result = {}
    result['data'] = session.pop('data', [])
    sample = SingleSample(data=result['data'], name='')
    #print sample
    result['results'] = sample.summary
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(result=result)
    
#######################################################################
# Two Samples (TS) - End
#######################################################################

#######################################################################
# More than Two Samples (MS)
#######################################################################
def parse_data(data, name):
    dataset = MultiSample()
    datalist = [sample for sample in data.split('\r\n')]
    if name == 'NO':
        datalist = [['Sample ' + str(index)] + datalist[index].split(',')
                    for index in range(len(datalist))]
    else: datalist = [datalist[index].split(',') 
                      for index in range(len(datalist))]
    for sample in datalist:
        sample_name = sample.pop(0)
        sample = [float(x) for x in sample]
        dataset.addSample(sample, name=sample_name)
        #print sample_name, sample
        #print dataset.sample
    return dataset
    
def input_MS():
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(
            TABLE(
                TR('Data: ', TEXTAREA(_name='data',
                    value='Enter the data, separated by commas')),
                TR('Data containing sample names? ',
                   SELECT('YES', 'NO', _name='sample_w_name')),
                TR('Type of Analysis: ',
                   SELECT('Distance Matrix',
                          _name='analysis_type'),
                   INPUT(_type='submit', _value='SUBMIT'))))
    if form.accepts(request.vars,session):       
        redirect(URL(r=request, f='analyze_MS'))
    return dict(form=form)
    
def analyze_MS():
    result = {}
    result['data'] = session.pop('data', [])
    sample = SingleSample(data=result['data'], name='')
    #print sample
    result['results'] = sample.summary
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(result=result)
#######################################################################
# More than Two Samples (MS) - End
#######################################################################
