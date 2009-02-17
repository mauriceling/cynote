import Bio.Seq as Seq

def dna_aa():
    if session.username == None: redirect(URL(r=request,f='../account/log_in'))
    form = FORM(TABLE(TR("Sequence:  ", 
                        TEXTAREA(_type="text",_name="sequence",requires=IS_NOT_EMPTY())),
                      TR("Sequence Type: ", 
                        SELECT("Raw Format", "FASTA",_name="seq_type")),
                      TR("Action: ", 
                        SELECT("Complementation", "Transcribe", "Translate", 
                               "Back Transcribe", "Back Translate",_name="action")),
                      TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request.vars,session):
        if form.vars.seq_type=="FASTA": session['sequence'] = fasta_to_raw(form.vars.sequence.upper())
        else: session['sequence'] = form.vars.sequence.upper()
        if form.vars.action=="Complementation":
           session['action'] = "Complementation"
           session['Complement'] = Seq.reverse_complement(session['sequence'])
        if form.vars.action=="Transcribe": 
            session['action'] = 'Transcribe'
            session['Transcribed RNA'] = Seq.transcribe(session['sequence'])
        if form.vars.action=="Back Transcribe": 
            session['action'] = 'Back Transcribe'
            session['DNA'] = Seq.back_transcribe(session['sequence'])
        if form.vars.action=="Translate":
            session['action'] = 'Translate'
            session.update(translate(session['sequence']))
        if form.vars.action=="Back Translate":
            session['action'] = 'Back Translate'
            session.update(back_translate(session['sequence']))
        redirect(URL(r=request,f='dna_aa_output'))
    return dict(form=form)
    
def dna_aa_output():
    result = {}
    result['Input Sequence'] = session.pop('sequence', None)
    result['Action'] = session.pop('action', None)
    if result['Action'] == 'Complementation': result['Complement'] = session.pop('Complement', None)
    if result['Action'] == 'Transcribe': result['Transcribed RNA'] = session.pop('Transcribed RNA', None)
    if result['Action'] == 'Back Transcribe': result['DNA'] = session.pop('DNA', None)
    if result['Action'] == 'Translate':
        result['First Frame'] = session.pop('First Frame', None)
        result['Second Frame'] = session.pop('Second Frame', None)
        result['Third Frame'] = session.pop('Third Frame', None)
        result['Complement First Frame'] = session.pop('Complement First Frame', None)
        result['Complement Second Frame'] = session.pop('Complement Second Frame', None)
        result['Complement Third Frame'] = session.pop('Complement Third Frame', None)
    #if result['Action'] == 'Back Translate':
    #    result['First Frame'] = session.pop('First Frame', None)
    #    result['Second Frame'] = session.pop('Second Frame', None)
    #    result['Third Frame'] = session.pop('Third Frame', None)
    #    result['Complement First Frame'] = session.pop('Complement First Frame', None)
    #    result['Complement Second Frame'] = session.pop('Complement Second Frame', None)
    #    result['Complement Third Frame'] = session.pop('Complement Third Frame', None)
    cynotedb.result.insert(testresult=result)
    cynotedb.commit()
    return dict(result=result)

def translate(seq):
    r = {}
    r['First Frame'] = Seq.translate(seq)
    r['Second Frame'] = Seq.translate(seq[1:])
    r['Third Frame'] = Seq.translate(seq[2:])
    seq = Seq.reverse_complement(seq)
    r['Complement First Frame'] = Seq.translate(seq)
    r['Complement Second Frame'] = Seq.translate(seq[1:])
    r['Complement Third Frame'] = Seq.translate(seq[2:])
    return r

def back_translate(seq):
    r = {}
    return r

def fasta_to_raw(fasta):
    raw = fasta
    return raw
    
def protein_analysis():
    if session.username == None: redirect(URL(r=request,f='../account/log_in'))
    from Bio.SeqUtils.ProtParam import ProteinAnalysis
    form = FORM(TABLE(TR("Amino acid sequence:  ", 
                        TEXTAREA(_type="text",_name="sequence",requires=IS_NOT_EMPTY())),
                      TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request.vars,session):
        session['sequence'] = form.vars.sequence.upper()
        X = ProteinAnalysis(session['sequence'])
        session['aa_count'] = X.count_amino_acids()
        session['percent_aa'] = X.get_amino_acids_percent()
        session['mw'] = X.molecular_weight()
        session['aromaticity'] = X.aromaticity()
        session['instability'] = X.instability_index()
        session['flexibility'] = X.flexibility()
        session['pI'] = X.isoelectric_point()
        session['sec_struct'] = X.secondary_structure_fraction()
        redirect(URL(r=request,f='protein_analysis_output'))
    return dict(form=form)
    
def protein_analysis_output():
    result = {}
    result['Sequence'] = session.pop('sequence', None)
    result['Molecular weight'] = session.pop('mw', None)
    result['Isoelectric point'] = session.pop('pI', None)
    result['Amino acid count'] = session.pop('aa_count', None)
    result['Amino acid proportion'] = session.pop('percent_aa', None)
    result['Aromaticity'] = session.pop('aromaticity', None)
    result['Instability index'] = session.pop('instability', None)
    result['Flexibility'] = session.pop('flexibility', None)
    result['Secondary struction fraction'] = session.pop('sec_struct', None)
    cynotedb.result.insert(testresult=result)
    cynotedb.commit()
    return dict(result=result)

def ncbiblast():
    if session.username == None: redirect(URL(r=request,f='../account/log_in'))
    form = FORM(TABLE(TR("Sequence:  ", 
                        TEXTAREA(_type="text",_name="sequence",requires=IS_NOT_EMPTY())),
                      TR("Program: ", 
                        SELECT("blastn", "blastp", "blastx", "tblastn", "tblastx", 
                        _name="program")),
                      TR("Database: ", 
                        SELECT("nr",
                        _name="database")),
                      TR("Matrix: ", 
                        SELECT("BLOSUM62", "BLOSUM80", "BLOSUM45", 
                        "PAM30", "PAM70",_name="matrix")),
                      TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request.vars,session):
        from Bio.Blast.NCBIWWW import qblast
        from Bio.Blast import NCBIXML
        sequence = fasta_to_raw(form.vars.sequence)
        rec = NCBIXML.parse(qblast(form.vars.program, 
                                   form.vars.database, 
                                   form.vars.sequence,
                                   matrix_name=form.vars.matrix)).next()
        session['sequence'] = sequence
        session['database'] = form.vars.database
        session['program'] = form.vars.program
        session['matrix'] = form.vars.matrix
        session['data'] = [{'Title':row.title, 'Score':str(row.score), 'E-value':str(row.e)} 
                           for row in rec.descriptions]
            
        redirect(URL(r=request,f='ncbiblast_output'))
    return dict(form=form)

def ncbiblast_output():
    #These 2 lines inserts result dictionary into cynote.result table
    result = {'Sequence' : session.pop('sequence', None),
              'Database' : session.pop('database', None),
              'Program' : session.pop('program', None),
              'Matrix' : session.pop('matrix', None),
              'Output' : session.pop('data', None)}
    cynotedb.result.insert(testresult=result)
    cynotedb.commit()
    return dict(Sequence=result['Sequence'],
                Database=result['Database'],
                Program=result['Program'],
                Matrix=result['Matrix'],
                Result=result['Output'])
