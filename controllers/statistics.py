exec("""from applications.%s.modules.copads.StatisticsDistribution \
    import ChiSquareDistribution""" % (request.application))
exec("""from applications.%s.modules.copads.StatisticsDistribution \
    import NormalDistribution""" % (request.application))

#######################################################################
# Categorical Data
#######################################################################
def categorical():
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(
            TABLE(
                TR('Idenifier: ', 
                    TEXTAREA(_name='identifier',
                        value='Enter the data identifiers, separated by commas')),
                TR('Observed values: ', 
                    TEXTAREA(_name='observed',
                             value='Enter the data, separated by commas')),
                TR('Expected Values: ', 
                    TEXTAREA(_name='expected',
                             value='Enter the data, separated by commas')),
                TR('Expected value type: ', 
                    SELECT('Counts', 'Percentage', _name='etype')),
                TR('Type of Analysis: ',
                   SELECT('Chi-square test',
                          _name='analysis')),
                TR(INPUT(_type='submit', _value='SUBMIT'))))
    if form.accepts(request.vars, session):
        session.identifier = [x for x in form.vars.identifier.split(',')
                                if x != '']
        session.observed = [float(x) for x in form.vars.observed.split(',')
                                        if x != '']
        session.analysis = form.vars.analysis
        if form.vars.etype == 'Percentage':
            total = sum(session.observed)
            session.expected = [(float(x) * total) / 100
                                for x in form.vars.expected.split(',')
                                    if x != '']
        else:
            session.expected = [float(x) for x in form.vars.expected.split(',')
                                            if x != '']
        if len(session.expected) > len(session.observed):
            session.expected = session.expected[:len(session.observed)]
            session.warning = 'Expected counts more than observed counts. \
            Expected counts is truncated to observed counts.'
        elif len(session.expected) < len(session.observed):
            session.observed = session.observed[:len(session.expected)]
            session.warning = 'Observed counts more than expected counts. \
            Observed counts is truncated to expected counts.'
        else: session.warning = 'None'
        if len(session.identifier) > len(session.observed):
            session.identifier = session.identifier[:len(session.observed)]
        if len(session.identifier) < len(session.observed):
            session.identifier = session.identifier + \
                [''] * (len(session.observed) - len(session.identifier))
        redirect(URL(r=request, f='analyze_categorical'))
    return dict(form=form)
    
def analyze_categorical():
    result = {}
    result['observed'] = session.pop('observed', [])
    result['expected'] = session.pop('expected', [])
    result['identifier'] = session.pop('identifier', [])
    result['analysis'] = session.pop('analysis', '')
    if result['analysis'] == 'Chi-square test':
        stat = sum([(result['observed'][index] - result['expected'][index]) ** 2 / \
                        result['expected'][index]
                    for index in range(len(result['observed']))])
        result['value'] = 1.0 - ChiSquareDistribution(len(result['observed'])).CDF(stat)
        print stat, result['value']
    return dict(result=result)
#######################################################################
# Categorical Data - End
#######################################################################
    
#######################################################################
# 2x2 Contingency Table
#######################################################################
def ttcontingency():
    if session.username == None: 
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(
            TABLE(
                TR('', 
                    INPUT(_name='outcome1', value='Outcome 1'), 
                    INPUT(_name='outcome2', value='Outcome 2')),
                TR(INPUT(_name='group1', value='Group 1'), 
                    INPUT(_name='o1g1'), 
                    INPUT(_name='o2g1')),
                TR(INPUT(_name='group2', value='Group 2'), 
                    INPUT(_name='o1g2'), 
                    INPUT(_name='o2g2')),
                TR('Type of Analysis: ',
                   SELECT('Z test - Correlated Proportions',
                          "Chi-square test with Yate's correction",
                          "Chi-square test without Yate's correction",
                          "McNemar's test with Yate's correction",
                          "McNemar's test without Yate's correction",
                          'P1 - P2',
                          'Relative Risk',
                          'Odds Ratio',
                          _name='analysis')),
                INPUT(_type='submit', _value='SUBMIT')))
    if form.accepts(request.vars,session):
        session.outcome1 = str(form.vars.outcome1)
        session.outcome2 = str(form.vars.outcome2)
        session.group1 = str(form.vars.group1)
        session.group2 = str(form.vars.group2)
        if form.vars.o1g1 == '': session.o1g1 = 0.0
        else: session.o1g1 = float(form.vars.o1g1)
        if form.vars.o1g2 == '': session.o1g2 = 0.0
        else: session.o1g2 = float(form.vars.o1g2)
        if form.vars.o2g1 == '': session.o2g1 = 0.0
        else: session.o2g1 = float(form.vars.o2g1)
        if form.vars.o2g2 == '': session.o2g2 = 0.0
        else: session.o2g2 = float(form.vars.o2g2)
        session.analysis = form.vars.analysis
        redirect(URL(r=request, f='analyze_ttcontingency'))
    return dict(form=form)
    
def analyze_ttcontingency():
    result = {}
    result['outcome1'] = session.pop('outcome1', 'outcome1')
    result['outcome2'] = session.pop('outcome2', 'outcome2')
    result['group1'] = session.pop('group1', 'group1')
    result['group2'] = session.pop('group2', 'group2')
    result['o1g1'] = session.pop('o1g1', 0)
    result['o1g2'] = session.pop('o1g2', 0)
    result['o2g1'] = session.pop('o2g1', 0)
    result['o2g2'] = session.pop('o2g2', 0)
    result['analysis'] = session.pop('analysis', '')
    N = result['o1g1'] + result['o2g1'] + result['o1g2'] + result['o2g2']
    result['phi'] = ((result['o1g1'] * result['o2g2']) - \
                      (result['o1g2'] * result['o2g1'])) / \
                    (((result['o1g1'] + result['o2g1']) * \
                      (result['o1g2'] + result['o2g2']) * \
                      (result['o1g1'] + result['o1g2']) * \
                      (result['o2g1'] + result['o2g2'])) ** 0.5)
    Po = (result['o1g1'] + result['o2g2']) / \
         (result['o1g1'] + result['o2g1'] + result['o1g2'] + result['o2g2'])
    Pe = ((((result['o1g1'] + result['o2g1']) * \
            (result['o1g1'] + result['o1g2'])) / N) + \
          (((result['o1g2'] + result['o2g2']) * \
            (result['o2g1'] + result['o2g2'])) / N)) / N
    result['kappa'] = (Po - Pe) / (1 - Pe)
    if result['analysis'] == 'Z test - Correlated Proportions':
        exec("""from applications.%s.modules.copads.HypothesisTest \
        import ZCorrProportion""" % (request.application))
        stat = ZCorrProportion(ssize=N, ny=result['o2g1'], yn=result['o1g2'], 
                               confidence=0.975)
        p = NormalDistribution().CDF(stat[2])
        if p < 0.5: result['value'] = p
        else: result['value'] = 1.0 - p
    if result['analysis'] == "Chi-square test with Yate's correction":
        stat = (N * (abs((result['o1g1'] * result['o2g2']) - \
                         (result['o1g2'] * result['o2g1'])) - \
                     (0.5 * N)) ** 2) / \
               ((result['o1g1'] + result['o2g1']) * \
                (result['o1g2'] + result['o2g2']) * \
                (result['o1g1'] + result['o1g2']) * \
                (result['o2g1'] + result['o2g2']))
        result['value'] = 1.0 - ChiSquareDistribution(2).CDF(stat)
    if result['analysis'] == "Chi-square test without Yate's correction":
        stat = (N * (((result['o1g1'] * result['o2g2']) - \
                      (result['o1g2'] * result['o2g1'])) ** 2)) / \
               ((result['o1g1'] + result['o2g1']) * \
                (result['o1g2'] + result['o2g2']) * \
                (result['o1g1'] + result['o1g2']) * \
                (result['o2g1'] + result['o2g2']))
        result['value'] = 1.0 - ChiSquareDistribution(2).CDF(stat)
    if result['analysis'] == "McNemar's test with Yate's correction":
        stat = ((abs(result['o1g1'] - result['o2g2']) - 1) ** 2) / \
               (result['o1g1'] + result['o2g2'])
        result['value'] = 1.0 - ChiSquareDistribution(2).CDF(stat)
    if result['analysis'] == "McNemar's test without Yate's correction":
        stat = ((result['o1g1'] - result['o2g2']) ** 2) / \
               (result['o1g1'] + result['o2g2'])
        result['value'] = 1.0 - ChiSquareDistribution(2).CDF(stat)
    if result['analysis'] == 'P1 - P2':
        result['value'] = (result['o1g1'] / \
                            float(result['o1g1'] + result['o2g1'])) - \
                          (result['o1g2'] / \
                            float(result['o1g2'] + result['o2g2']))
    if result['analysis'] == 'Relative Risk':
        result['value'] = (result['o1g1'] / \
                            float(result['o1g1'] + result['o2g1'])) / \
                          (result['o1g2'] / \
                            float(result['o1g2'] + result['o2g2']))
    if result['analysis'] == 'Odds Ratio':
        result['value'] = (result['o1g1'] / float(result['o2g1'])) / \
                          (result['o1g2'] / float(result['o2g2']))
    return dict(result=result)
#######################################################################
# 2x2 Contingency Table - End
#######################################################################

#######################################################################
# 2xC Contingency Table
#######################################################################
def tccontingency():
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
                INPUT(_type='submit', _value='SUBMIT')))
    if form.accepts(request.vars, session):
        if form.vars.name1 == '': form.vars.name1 = 'Sample 1'
        if form.vars.name2 == '': form.vars.name2 = 'Sample 2'
        session.analysis_type = form.vars.analysis_type
        form.vars.data1 = [float(x) for x in form.vars.data1.split(',')
                           if x.strip() != '']
        form.vars.data2 = [float(x) for x in form.vars.data2.split(',')
                           if x.strip() != '']
        session.data_name = (form.vars.name1, form.vars.name2)
        session.data = (form.vars.data1, form.vars.data2)
        redirect(URL(r=request, f='analyze_tccontingency'))
    return dict(form=form)
    
def con_discordance(a, b):
    p = [a[i] * sum(b[i+1:]) for i in range(len(a) - 1)]
    q = [a[i] * sum(b[:i]) for i in range(len(a)-1, 0, -1)]
    return (sum(p), sum(q))
    
def analyze_tccontingency():
    result = {}
    data = session.pop('data', ([], []))
    name = session.pop('data_name')
    pq = con_discordance(data[0], data[1])
    N = sum(data[0]) + sum(data[1])
    result['gamma'] = float(pq[0] - pq[1]) / float(pq[0] + pq[1])
    result['tau_a'] = float(pq[0] - pq[1]) / \
                      ((N * (N - 1)) / 2)
    result['tau_c'] = float(pq[0] - pq[1]) * \
                      (4 / (N * N))
    return dict(result=result, data=data, name=name)
#######################################################################
# 2xC Contingency Table - End
#######################################################################

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
# Regression Analysis
#######################################################################
def regression():
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
                TR('Correlation to be statistically', 
                ' tested the correlation from data', ' : ',
                    INPUT(_name='pcorr', value=0.0)),
                TR('Type of Analysis: ',
                   SELECT(#'Paired Z-test',
                          #'2-sample Z-test',
                          #'Paired t-test',
                          #'2-sample t-test',
                          #"Spearman's Correlation",
                          'Linear regression',
                          #'Distance measure',
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
        session.pcorr = float(form.vars.pcorr)
        redirect(URL(r=request, f='analyze_regression'))
    return dict(form=form)
    
def analyze_regression():
    result = {}
    data = session.pop('data', [])
    data_name = session.pop('data_name', [])
    result['data'] = {str(data_name[0]): data.getSample(data_name[0]),
                      str(data_name[1]): data.getSample(data_name[1])}
    result['analysis_type'] = session.pop('analysis_type', '')
    analysis_results = {}
    if result['analysis_type'] == 'Linear regression':
        exec("""from applications.%s.modules.copads.HypothesisTest \
        import ZPearsonCorrelation""" % (request.application))
        analysis_results['pcorr'] = session.pop('pcorr', 0.0)
        temp = data.linear_regression()
        analysis_results['LM'] = {'gradient': temp[0],
                                  'intercept': temp[1]}
        analysis_results['pearson'] = data.pearson()
        test = ZPearsonCorrelation(sr=analysis_results['pearson'], 
                                   pr=analysis_results['pcorr'],
                                   ssize=len(result['data'][str(data_name[0])]),
                                   confidence=0.975)
        analysis_results['pvalue'] = 1.0 - NormalDistribution().CDF(test[2])
    #print sample
    result['results'] = analysis_results
    #These 2 lines inserts result dictionary into cynote.result table
    #cynotedb.result.insert(testresult=result)
    #cynotedb.commit()
    return dict(result=result, name=data_name)
    
#######################################################################
# Regression - End
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
