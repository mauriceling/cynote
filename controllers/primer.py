from math import log10, log

def complement(seq, type='dna'):
    if type=='dna': TorU = 'T'
    if type=='rna': TorU = 'U'
    trans = {TorU:'A','A':TorU,'G':'C','C':'G','N':'N'}
    seq = seq.upper()
    r = []
    for c in seq: r.append(trans[c])
    return ''.join(r)
    
def primer_tm():
    if session.username == None: redirect(URL(r=request,f='../account/log_in'))
    form = FORM(TABLE(TR("Left primer sequence:  ", 
                        INPUT(_type="text",_name="lprimer",requires=IS_NOT_EMPTY())),
                      TR("Right primer sequence: ", 
                        INPUT(_type="text",_name="rprimer")),
                      TR("Monovalent ion concentration (mM): ", 
                        INPUT(_type="text",_name="salt", value=50.0)),
                      TR("Divalent ion concentration (mM): ", 
                        INPUT(_type="text",_name="magnesium", value=2.5)),
                      TR("Primer concentration (uM): ", 
                        INPUT(_type="text",_name="pcon", value=4.0)),
                TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request.vars,session):
        session.lprimer=form.vars.lprimer.upper()
        if form.vars.rprimer: session.rprimer=form.vars.rprimer.upper()
        else: session.rprimer = None
        if form.vars.salt: session.salt=float(form.vars.salt)
        else: session.salt = 50.0
        if form.vars.magnesium: session.magnesium=float(form.vars.magnesium)
        else: session.magnesium = 2.5
        if form.vars.pcon: session.pcon=float(form.vars.pcon)/1000000.0
        else: session.pcon = 4.0/1000000.0
        redirect(URL(r=request,f='primer_output'))
    return dict(form=form)

def primer_output():
    result = {}
    result['Left primer']=session['lprimer']
    result['Right primer']=session['rprimer']
    result['Monovalent ion concentration (mM)']=session['salt']
    result['Divalent ion concentration (mM)']=session['magnesium']
    result['Primer concentration (uM)']=session['pcon']
    session.update(process_degenerate_base(session,pos='l'))
    session.update(process_primer_tm(session,pos='l'))
    result['Left primer length']=session['llen']
    result['Left primer %GC']=str(session['lwGC'])+' to '+str(session['lbGC'])
    result['Left primer Tm (C)']=str(session['lbest'])+' to '+str(session['lworst'])
    result['Left primer Tm, salt corrected (C)']=str(session['lbestNa'])+' to '+str(session['lworstNa'])
    result['Left primer Tm, kinetics (C)']=str(session['lkinTm'])
    if result['Right primer']: 
        session.update(process_degenerate_base(session,pos='r'))
        session.update(process_primer_tm(session,pos='r'))
        result['Right primer length']=session['rlen']
        result['Right primer %GC']=str(session['rwGC'])+' to '+str(session['rbGC'])
        result['Right primer Tm (C)']=str(session['rbest'])+' to '+str(session['rworst'])
        result['Right primer Tm, salt corrected (C)']=str(session['rbestNa'])+' to '+str(session['rworstNa'])
        result['Right primer Tm, kinetics (C)']=str(session['rkinTm'])
    session.pop('salt', None)
    session.pop('magnesium', None)
    session.pop('pcon', None)
    for pos in ['l','r']:
        session.pop(pos+'primer', None)
        session.pop(pos+'len', None)
        session.pop(pos+'bGC', None)
        session.pop(pos+'wGC', None)
        session.pop(pos+'best', None)
        session.pop(pos+'worst', None)
        session.pop(pos+'bestNa', None)
        session.pop(pos+'worstNa', None)
        session.pop(pos+'kinTm', None)
        for base in ['A','T','G','C','U','W','S','N']:
            session.pop(pos+base, None)
    cynotedb.result.insert(testresult=result)
    cynotedb.commit()    
    return dict(result=result)
    
def process_degenerate_base(r, pos='l'):
    for base in ['A','T','G','C','U','W','S']:
        r[pos+base]=r[pos+'primer'].count(base)
    r[pos+'len']=len(r[pos+'primer'])
    r[pos+'N']=r[pos+'len']-r[pos+'A']-r[pos+'T']-r[pos+'G']- \
            r[pos+'C']-r[pos+'U']-r[pos+'W']-r[pos+'S']
    r[pos+'bGC']=100*float(r[pos+'G']+r[pos+'C']+r[pos+'S'])/ \
                            float(r[pos+'len'])
    r[pos+'wGC']=100*float(r[pos+'G']+r[pos+'C']+r[pos+'S']+ \
                            r[pos+'N'])/float(r[pos+'len'])
    return r

def process_primer_tm(result, pos='l'):
    r = {}
    if result[pos+'len'] < 14:
        # Tm (no salt correction) = (wA+xT) * 2 + (yG+zC) * 4
        r[pos+'best'] = ((result[pos+'A']+result[pos+'T']+ \
                result[pos+'U']+result[pos+'W']+ result[pos+'N']) \
                * 2) + ((result[pos+'G']+result[pos+'C']+\
                        result[pos+'S']) * 4)
        r[pos+'worst'] = ((result[pos+'A']+result[pos+'T']+ \
                result[pos+'U']+result[pos+'W']) * 2) + \
                ((result[pos+'G']+result[pos+'C']+result[pos+'S']+ \
                result[pos+'N']) * 4)
        # Tm (salt correction) = (wA+xT)*2 + (yG+zC)*4 - 16.6*log10(0.050) + 16.6*log10([salt])
        r[pos+'bestNa'] = ((result[pos+'A']+result[pos+'T']+ \
                result[pos+'U']+result[pos+'W']+result[pos+'N']) * 2) + \
                ((result[pos+'G']+result[pos+'C']+result[pos+'S']) * \
                4) - 16.6*log10(0.050) + \
                16.6*log10(float(result['salt'])/1000)
        r[pos+'worstNa'] = ((result[pos+'A']+result[pos+'T']+\
                result[pos+'U']+result[pos+'W']) * 2) + \
                ((result[pos+'G']+result[pos+'C']+result[pos+'S']+ \
                result[pos+'N']) * 4) - 16.6*log10(0.050) + \
                16.6*log10(float(result['salt'])/1000)
    else:
        # Tm (no salt correction) = 64.9 +41*(yG+zC-16.4)/(wA+xT+yG+zC)
        r[pos+'best'] = 64.9 + (41*(result[pos+'G']+result[pos+'C']+ \
                result[pos+'S']-16.4)/result[pos+'len'])
        r[pos+'worst'] = 64.9 + (41*(result[pos+'G']+result[pos+'C']+ \
                result[pos+'S']+result[pos+'N']-16.4)/ result[pos+'len'])
        # Tm (salt correction) = 81.5 + 16.6*log10([salt]) - 500/N + 0.41(%GC) 
        r[pos+'bestNa'] = 81.5 + 16.6*log10(float(result['salt'])/1000) - \
                500.0/result[pos+'len'] + 0.41*result[pos+'bGC']
        r[pos+'worstNa'] = 81.5 + 16.6*log10(float(result['salt'])/1000) - \
                500.0/result[pos+'len'] + 0.41*result[pos+'wGC']
    if result[pos+'U'] == 0 and result[pos+'N'] == 0 and result[pos+'W'] == 0 \
        and result[pos+'S'] == 0:
        H = {'AA':-9100, 'AC':-6500, 'AG':-7800, 'AT':-8600,
             'CA':-5800, 'CC':-11000, 'CG':-11900, 'CT':-7800,
             'GA':-5600, 'GC':-11100, 'GG':-11000, 'GT':-6500,
             'TA':-6000, 'TC':-5600, 'TG':-5800, 'TT':-9100,
             'A':0, 'C':0, 'G':0, 'T':0}
        G = {'AA':-1550, 'AC':-1400, 'AG':-1450, 'AT':-1250,
             'CA':-1150, 'CC':-2300, 'CG':-3050, 'CT':-1450,
             'GA':-1150, 'GC':-2700, 'GG':-2300, 'GT':-1400,
             'TA':-850, 'TC':-1150, 'TG':-1150, 'TT':-1550,
             'A':0, 'C':0, 'G':0, 'T':0}
        deltaH = -10000.0
        deltaG = 200.0
        for i in range(len(result[pos+'primer'])):
            try:
                deltaH=deltaH+H[result[pos+'primer'][i]+result[pos+'primer'][i+1]]
                deltaG=deltaG+G[result[pos+'primer'][i]+result[pos+'primer'][i+1]]
            except IndexError: pass
        saltcon = float(result['salt'])/1000 + 4*((float(result['magnesium'])/1000)**0.5)
        r[pos+'kinTm'] = (298.2*deltaH)/(deltaH-deltaG+(1.99*298.2*log(result['pcon']))) + \
                         16.6*log10(saltcon/(1+0.7*saltcon)) - 269.3
    return r

def design_primer():
    if session.username == None: redirect(URL(r=request,f='../account/log_in'))
    form = FORM(TABLE(TR("Sequence:  ", 
                        TEXTAREA(_type="text",_name="sequence",requires=IS_NOT_EMPTY())),
                      TR("Left Primer Range: ", 
                        INPUT(value='1-35',_name="lrange")),
                      TR("Right Primer Range: ", 
                        INPUT(value='1-35',_name="rrange")),
                      TR("Monovalent ion concentration (mM): ", 
                        INPUT(_type="text",_name="salt", value=50.0)),
                      TR("Divalent ion concentration (mM): ", 
                        INPUT(_type="text",_name="magnesium", value=2.5)),
                      TR("Primer concentration (uM): ", 
                        INPUT(_type="text",_name="pcon", value=4.0)),
                      TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request.vars,session):
        lrange = form.vars.lrange.split('-')
        rrange = form.vars.rrange.split('-')
        session['left']=form.vars.sequence.upper()[int(lrange[0]):int(lrange[1])+1]
        session['right']=form.vars.sequence.upper()[-int(rrange[1]):-int(lrange[0])-1]
        session['result']=search_primer_pairs(session['left'], session['right'])
        #redirect(URL(r=request,f='primer_set'))
    return dict(form=form)
    
def primer_set():
    result = {}
    cynotedb.result.insert(testresult=result)
    cynotedb.commit()
    return dict(result=result)
