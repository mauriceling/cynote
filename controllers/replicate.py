import os 
import zipfile 
import StringIO 
        
def export(): 
    # export the entire database
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    form_user = FORM(
            TR("",
               INPUT(_type="submit", _name="ex_user",
                     _value="Export User List")))
    if form_user.accepts(request.vars):
        redirect(URL(r=request, f='export_user_list')) 
    form_cynote = FORM(
            TR("",
               INPUT(_type="submit", _name="ex_cynote",
                     _value="Export Cynote Database"))) 
    if form_cynote.accepts(request.vars):
        redirect(URL(r=request, f='export_cynote_database')) 
    return dict(form_cynote=form_cynote,
                form_user=form_user) 

def export_cynote_database():
    s = StringIO.StringIO() 
    cynotedb.export_to_csv_file(s) 
    response.headers['Content-Type'] = 'text/csv' 
    return s.getvalue() 

def export_user_list():
    s=StringIO.StringIO() 
    userdb.export_to_csv_file(s) 
    response.headers['Content-Type'] = 'text/csv' 
    return s.getvalue() 
        
def import_sync(): 
    form = FORM(
            INPUT(_type='file', _name='data'),
            INPUT(_type='submit')) 
    if form.accepts(request.vars):      
        cynotedb.import_from_csv_file(form.vars.data.file) 
           # for every table 
        for table in cynotedb.tables: 
                 # for every uuid, delete all but the most 
            items = cynotedb(cynotedb[table].id>0) \
                    .select(cynotedb[table].id,
                            cynotedb[table].uuid,orderby = ~cynotedb[table] \
                            .modified_on,
                            groupby = cynotedb[table].uuid)                  
            for item in items: 
                cynotedb((cynotedb[table].uuid == item.uuid) & \
                         (cynotedb[table].id != item.id)).delete    
    return dict(form=form)
    
def replication():        
    form = FORM(
            TABLE(
                TR("", INPUT(_type="submit", _value="SUBMIT"))))
    if form.accepts(request.vars,session):
        rows = cynotecynotedb((cynotecynotedb.entry.notebook == \
                               cynotecynotedb.entry.id) & \
                              (cynotecynotedb.comment.entry_id == \
                               cynotecynotedb.entry.id)).select()
        for row in rows:
            print row.entry.id, row.notebook.id, row.comment.id 
        #rows=cynotecynotedb().select(
           # cynotecynotedb.entry.ALL,
           # cynotecynotedb.comment.ALL,
            #left=[cynotecynotedb.comment.on(cynotecynotedb.entry.notebook_id==cynotecynotedb.notebook.id),
             # cynotecynotedb.comment.on(cynotecynotedb.comment.entry_id==cynotecynotedb.entry.id)])   
    return dict(form=form,
                rows=rows)


def zip(): 
    form = FORM(TABLE("", INPUT(_type="submit", _value="SUBMIT")))
    if form.accepts(request.vars):
        uploaded_files = os.listdir([os.getcwd(),'applications',
                                     request.application, 'uploads'])    
        zipf = zipfile.Zipfile(os.getcwd(), 'applications',
                               request.application,
                               'uploads','uploads_backup.zip', 'w')                           
        for f in uploaded_files: 
                try: zipf.write(f) 
                except: pass            
        #return encode('rot13')
        f.close()
    return dict(form=form)
    return unicode
    
    
def encrypt(s):
    return s.encode('rot13')
def decrypt(s):
    return s.decode('rot13')
    f = open(filename, 'wb')
    f.write(encrypt(content))
    f.close()
    f = open(filename, 'r')
    content = decrypt(f.read())
    f.close()
