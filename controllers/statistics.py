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
        session.data = [float(x) for x in form.vars.data.split(',')
                        if x.strip() != '']
        redirect(URL(r=request, f='analyze_SS'))
    return dict(form=form)
    
def analyze_SS():
    exec("""from applications.%s.modules.copads.SampleStatistics \
    import SingleSample""" % (request.application))
    result = {}
    result['data'] = session.pop('data', [])
    sample = SingleSample(result['data'], '')
    #print sample
    sample.fullSummary()
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
                TR('Name #1: ', INPUT(_name='name1', value='Enter name #1'),
                   'Data #1: ', TEXTAREA(_name='data1',
                                value='Enter the data, separated by commas')),
                TR('Name #2: ', INPUT(_name='name2', value='Enter name #2'),
                   'Data #2: ', TEXTAREA(_name='data2',
                                value='Enter the data, separated by commas')),
                TR('Type of Analysis: ',
                   SELECT(#'Paired Z-test',
                          #'2-sample Z-test',
                          #'Paired t-test',
                          #'2-sample t-test',
                          #"Pearson's Correlation",
                          #"Spearman's Correlation",
                          'Linear regression',
                          'Distance measure',
                          _name='analysis_type'), '',
                   INPUT(_type='submit', _value='SUBMIT'))))
    if form.accepts(request.vars,session):
        exec("""from applications.%s.modules.copads.SampleStatistics \
        import TwoSample""" % (request.application))
        if form.vars.name1 == '': form.vars.name1 = 'Sample 1'
        if form.vars.name2 == '': form.vars.name2 = 'Sample 2'
        session.analysis_type = form.vars.analysis_type
        form.vars.data1 = [float(x) for x in form.vars.data1.split(',')
                           if x.strip() != '']
        form.vars.data2 = [float(x) for x in form.vars.data2.split(',')
                           if x.strip() != '']
        session.data = TwoSample(form.vars.data1, form.vars.name1,
                                 form.vars.data2, form.vars.name2)
        session.data_name = (form.vars.name1, form.vars.name2)
        redirect(URL(r=request, f='analyze_TS'))
    return dict(form=form)
    
def analyze_TS():
    result = {}
    data = session.pop('data', [])
    data_name = session.pop('data_name', [])
    result['data'] = {str(data_name[0]): data.getSample(data_name[0]),
                      str(data_name[1]): data.getSample(data_name[1])}
    result['analysis_type'] = session.pop('analysis_type', '')
    analysis_results = {}
    if result['analysis_type'] == 'Paired Z-test': pass
    if result['analysis_type'] == '2-sample Z-test': pass
    if result['analysis_type'] == 'Paired t-test': pass
    if result['analysis_type'] == '2-sample t-test': pass
    if result['analysis_type'] == "Pearson's Correlation": pass
    if result['analysis_type'] == "Spearman's Correlation": pass
    if result['analysis_type'] == 'Linear regression':
        temp = data.linear_regression()
        analysis_results['LM'] = {'gradient': temp[0],
                                          'intercept': temp[1]}
    if result['analysis_type'] == 'Distance measure': pass
    #print sample
    result['results'] = analysis_results
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(result=result, name=data_name)
    
#######################################################################
# Two Samples (TS) - End
#######################################################################

#######################################################################
# More than Two Samples (MS)
#######################################################################
def parse_data(data, name):
    exec("""from applications.%s.modules.copads.SampleStatistics \
    import MultiSample""" % (request.application))
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
                   SELECT("Pearson's Correlation Matrix",
                          _name='analysis_type'),
                   INPUT(_type='submit', _value='SUBMIT'))))
    if form.accepts(request.vars,session):
        session.analysis_type = form.vars.analysis_type
        session.data = parse_data(form.vars.data, form.vars.sample_w_name)       
        redirect(URL(r=request, f='analyze_MS'))
    return dict(form=form)
    
def analyze_MS():
    result = {}
    result['data'] = session.pop('data', [])
    result['analysis_type'] = session.pop('analysis_type', '')
    analysis_results = {}
    if result['analysis_type'] == "Pearson's Correlation Matrix": pass
    #print sample
    result['results'] = analysis_results
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(result=result)
#######################################################################
# More than Two Samples (MS) - End
#######################################################################
