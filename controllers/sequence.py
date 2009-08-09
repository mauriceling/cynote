import Bio.Seq as Seq

def seqClean(s):
    import re
    return re.sub('\s', '', s)
    
def dna_aa():
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(TABLE(TR("Sequence:  ", 
                        TEXTAREA(_type="text",
                                 _name="sequence",
                                 requires=IS_NOT_EMPTY())),
                      TR("Sequence Type: ", 
                        SELECT("Raw Format", "FASTA",
                               _name="seq_type")),
                      TR("Action: ", 
                        SELECT("Complementation", "Transcribe", "Translate", 
                               "Back Transcribe", "Back Translate",
                               _name="action")),
                      TR("", INPUT(_type="submit", _value="SUBMIT"))))
    if form.accepts(request.vars,session):
        if form.vars.seq_type == "FASTA": 
            session['sequence'] = \
                seqClean(fasta_to_raw(form.vars.sequence.upper()))
        else: session['sequence'] = seqClean(form.vars.sequence.upper())
        if form.vars.action == "Complementation":
           session['action'] = "Complementation"
           session['Complement'] = Seq.reverse_complement(session['sequence'])
        if form.vars.action == "Transcribe": 
            session['action'] = 'Transcribe'
            session['Transcribed RNA'] = Seq.transcribe(session['sequence'])
        if form.vars.action == "Back Transcribe": 
            session['action'] = 'Back Transcribe'
            session['DNA'] = Seq.back_transcribe(session['sequence'])
        if form.vars.action == "Translate":
            session['action'] = 'Translate'
            session.update(translate(session['sequence']))
        if form.vars.action == "Back Translate":
            session['action'] = 'Back Translate'
            session.update(back_translate(session['sequence']))
        redirect(URL(r=request, f='dna_aa_output'))
    return dict(form=form)
    
def dna_aa_output():
    result = {}
    result['Input Sequence'] = session.pop('sequence', None)
    result['Action'] = session.pop('action', None)
    if result['Action'] == 'Complementation':
        result['Complement'] = session.pop('Complement', None)
    if result['Action'] == 'Transcribe':
        result['Transcribed RNA'] = session.pop('Transcribed RNA', None)
    if result['Action'] == 'Back Transcribe':
        result['DNA'] = session.pop('DNA', None)
    if result['Action'] == 'Translate':
        result['First Frame'] = session.pop('First Frame', None)
        result['Second Frame'] = session.pop('Second Frame', None)
        result['Third Frame'] = session.pop('Third Frame', None)
        result['Complement First Frame'] = \
                           session.pop('Complement First Frame', None)
        result['Complement Second Frame'] = \
                           session.pop('Complement Second Frame', None)
        result['Complement Third Frame'] = \
                           session.pop('Complement Third Frame', None)
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
    form = FORM(
        TABLE(
            TR("Amino acid sequence:  ",
               TEXTAREA(_type="text", _name="sequence",
                        requires=IS_NOT_EMPTY())),
            TR("", INPUT(_type="submit", _value="SUBMIT"))))
    if form.accepts(request.vars,session):
        session['sequence'] = seqClean(form.vars.sequence.upper())
        X = ProteinAnalysis(session['sequence'])
        session['aa_count'] = X.count_amino_acids()
        session['percent_aa'] = X.get_amino_acids_percent()
        session['mw'] = X.molecular_weight()
        session['aromaticity'] = X.aromaticity()
        session['instability'] = X.instability_index()
        session['flexibility'] = X.flexibility()
        session['pI'] = X.isoelectric_point()
        session['sec_struct'] = X.secondary_structure_fraction()
        redirect(URL(r=request, f='protein_analysis_output'))
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
    result['Secondary structure fraction'] = session.pop('sec_struct', None)
    cynotedb.result.insert(testresult=result)
    cynotedb.commit()
    return dict(result=result)

ncbi_db = {"Non-redundant GenBank (nr)" : "nr",
           "NCBI Reference Sequence (refseq)" : "refseq",
           "SWISS-PROT protein sequence (last update) (swissprot)" : \
                "swissprot",
           "Patent division of GenPept (pat)" : "pat",
           "Protein Data Bank (pdb)" : "pdb",
           "Protein - environmental samples (env_nr)" : "env_nr",
           "RNA - NCBI Reference Sequence (refseq_rna)" : "refseq_rna",
           "Genomic - NCBI Reference Sequence (refseq_genomic)" : \
                "refseq_genomic",
           "ESTs - GenBank + EMBL + DDBJ (est)" : "est",
           "Mouse subset of ESTs (est_mouse)" : "est_mouse",
           "Human subset of ESTs (est_human)" : "est_human",
           "Non-mouse non-human subset of ESTs (est_others)" : "est_others",
           "Genome Survey Sequences (gss)" : "gss",
           "Complete chromosomes (chromosome)" : "chromosome",
           "Whole Genome Shotgun sequences (wgs)" : "wgs",
           "Nucleotide - environmental samples (env_nr)" : "env_nt"}

genetic_code = {"Standard (1)" : 1,
                "Vertebrate Mitochondria (2)" : 2,
                "Yeast Mitochondria (3)" : 3,
                "Mold, Protozoan, and Coelenterate Mitochondria (4)" : 4,
                "Mycoplasma/Spiroplasma (4)" : 4,
                "Invertebrate Mitochondria (5)" : 5,
                "Ciliate, Dasycladacean and Hexamita Nuclear (6)" : 6,
                "Echinoderm and Flatworm Mitochondria (9)" : 9,
                "Euplotid Nuclear (10" : 10,
                "Bacterial, Archaeal and Plant Plastid (11)" : 11,
                "Alternative Yeast Nuclear (12)" : 12,
                "Ascidian Mitochondria (13)" : 13,
                "Alternative Flatworm Mitochondria (14)" : 14,
                "Blepharisma Nuclear (15)" : 15,
                "Chlorophycean Mitochondria (16)" : 16,
                "Trematode Mitochondria (21)" : 21,
                "Scenedesmus obliquus Mitochondria (22)" : 22,
                "Thraustochytrium Mitochondria (23)" : 23}

def ncbiblast():
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(TABLE(TR("Job Title: ", 
                        INPUT(_type="text", _name="title")),
                      TR("Sequence:  ", 
                        TEXTAREA(_type="text", _name="sequence",
                                 requires=IS_NOT_EMPTY())),
                      TR("Program: ", 
                        SELECT("blastn", "blastp", "blastx", "tblastn",
                               "tblastx",
                               _name="program")),
                      TR("Database: ", 
                        SELECT("Non-redundant GenBank (nr)", 
                        "NCBI Reference Sequence (refseq)",
                        "SWISS-PROT protein sequence (last update) (swissprot)",
                        "Patent division of GenPept (pat)", 
                        "Protein Data Bank (pdb)",
                        "Protein - environmental samples (env_nr)",
                        "RNA - NCBI Reference Sequence (refseq_rna)",
                        "Genomic - NCBI Reference Sequence (refseq_genomic)",
                        "ESTs from GenBank + EMBL + DDBJ (est)",
                        "Mouse subset of ESTs (est_mouse)", 
                        "Human subset of ESTs (est_human)",
                        "Non-mouse non-human subset of ESTs (est_others)",
                        "Genome Survey Sequences (gss)", 
                        "Complete chromosomes (chromosome)",
                        "Whole Genome Shotgun sequences (wgs)",
                        "Nucleotide - environmental samples (env_nr)",
                        _name="database")),
                      TR("Translation Table: ", 
                        SELECT("Standard (1)",
                        "Vertebrate Mitochondria (2)",
                        "Yeast Mitochondria (3)",
                        "Mold, Protozoan, and Coelenterate Mitochondria (4)",
                        "Mycoplasma/Spiroplasma (4)",
                        "Invertebrate Mitochondria (5)",
                        "Ciliate, Dasycladacean and Hexamita Nuclear (6)",
                        "Echinoderm and Flatworm Mitochondria (9)",
                        "Euplotid Nuclear (10)",
                        "Bacterial, Archaeal and Plant Plastid (11)",
                        "Alternative Yeast Nuclear (12)",
                        "Ascidian Mitochondria (13)",
                        "Alternative Flatworm Mitochondria (14)",
                        "Blepharisma Nuclear (15)",
                        "Chlorophycean Mitochondria (16)",
                        "Trematode Mitochondria (21)",
                        "Scenedesmus obliquus Mitochondria (22)",
                        "Thraustochytrium Mitochondria (23)",
                            _name="gcode")),
                      TR("Matrix: ", 
                        SELECT("BLOSUM62", "BLOSUM80", "BLOSUM45", 
                        "PAM30", "PAM70",_name="matrix")),
                      TR("Maximum number of hits to return: ", 
                        SELECT("50", "100", "200", "500", "1000", "2000",
                               "5000", "10000", "20000", "50000",
                               _name="hitlist_size")),
                      TR("Number of random hits expected: ", 
                        INPUT(_type="text", _name="expect", value=10)),
                      TR("Word size: ", 
                        INPUT(_type="text", _name="word_size", value=3)),
                      TR("",INPUT(_type="submit", _value="SUBMIT"))))
    if form.accepts(request.vars,session):
        from Bio.Blast.NCBIWWW import qblast
        from Bio.Blast import NCBIXML
        sequence = seqClean(fasta_to_raw(form.vars.sequence.upper()))
        rec = NCBIXML.parse(qblast(form.vars.program, 
                                   ncbi_db[form.vars.database], 
                                   sequence,
                                   matrix_name=form.vars.matrix,
                                   hitlist_size=int(form.vars.hitlist_size),
                                   expect=float(form.vars.expect),
                                   word_size=int(form.vars.word_size),
                                   db_genetic_code=genetic_code[form.vars.gcode])).next()
        session['title'] = form.vars.title
        session['sequence'] = sequence
        session['database'] = form.vars.database
        session['program'] = form.vars.program
        session['matrix'] = form.vars.matrix
        session['gcode'] = form.vars.gcode
        session['hitsize'] = form.vars.hitlist_size
        session['expect'] = form.vars.expect
        session['word_size'] = form.vars.word_size
        session['data'] = [{'Title':row.title, 'Score':str(row.score), 
                            'E-value':str(row.e)} 
                           for row in rec.descriptions]
        redirect(URL(r=request, f='ncbiblast_output'))
    return dict(form=form)

def ncbiblast_output():
    #These 2 lines inserts result dictionary into cynote.result table
    result = {'Job Title' : session.pop('title', 'Untitled'),
              'Sequence' : session.pop('sequence', None),
              'Database' : session.pop('database', None),
              'Program' : session.pop('program', None),
              'Matrix' : session.pop('matrix', None),
              'Genetic Code' : session.pop('gcode', None),
              'Word Size' : session.pop('word_size', None),
              'Maximum hits' : session.pop('hitsize', None),
              'Expect' : session.pop('expect', None),
              'Output' : session.pop('data', "No result")}
    cynotedb.result.insert(testresult=result)
    cynotedb.commit()
    return dict(Title=result['Job Title'],
                Sequence=result['Sequence'],
                Database=result['Database'],
                Program=result['Program'],
                Matrix=result['Matrix'],
                Genetic_code=result['Genetic Code'],
                Word_size=result['Word Size'],
                Hitlist_size=result['Maximum hits'],
                Expect=result['Expect'],
                Result=result['Output'])

def restriction_digest():
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    form = FORM(TABLE(TR("Sequence:  ", 
                        TEXTAREA(_type="text",
                                 _value="Enter your DNA sequence in plain form",
                                 _name="sequence",
                                 requires=IS_NOT_EMPTY())),
                      TR("DNA Type: ", 
                        SELECT("Linear", "Circular",
                               _name="dna_type")),
                      TR("Show Fragments: ", 
                        SELECT("No", "Yes",
                               _name="show_frag")),
                      TR("", INPUT(_type="submit", _value="Digest DNA"))))
    if form.accepts(request.vars,session):
        from Bio import Restriction as R
        from Bio.Seq import Seq
        from Bio.Alphabet import IUPAC
        if request.vars.dna_type == 'Linear':
            dna_type = 'True'
        else:
            dna_type = 'False'
        seq = Seq(request.vars.sequence, IUPAC.unambiguous_dna)
        results = {}
        nocut = []
        results['sequence'] = seq
        for enzyme in R.RestrictionBatch([], suppliers = ['F', 'N', 'R']):
            digest = enzyme.search(seq, linear=dna_type)
            digest.sort()
            #fragment = [digest[x+1] - digest[x]
            #            for x in range(len(digest) - 1)]
            #fragment.sort()
            d = {}
            if len(digest) == 0:
                nocut.append(str(enzyme))
            else:
                d['Restriction site'] = enzyme.site
                if dna_type == 'True':
                    d['Number of fragments'] = str(len(digest) + 1)
                else:
                    d['Number of fragments'] = str(len(digest))
                if request.vars.show_frag == 'Yes':
                    d['Cut positions'] = str(digest)
                results[str(enzyme)] = d
        results['Enzymes that do not cut'] = nocut
        session['result'] = results
        redirect(URL(r=request, f='restriction_digest_output'))
    return dict(form=form)
    
def restriction_digest_output():
    result = session.pop('result', None)
    cynotedb.result.insert(testresult=result)
    cynotedb.commit()
    sequence = result.pop('sequence', None)
    uncut = result.pop('Enzymes that do not cut', None)
    uncut.sort()
    return dict(sequence=sequence, result=result, uncut=uncut)
