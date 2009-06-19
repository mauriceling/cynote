import os
import datetime
from ftplib import FTP

now = datetime.datetime.utcnow()

def form():
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))    
    form = FORM(TABLE(TR("FTP Server: ", 
                        INPUT(_type="text", _name="ftpserver")),
                      TR("FTP Username: ", 
                        INPUT(_type="text", _name="ftpusername")),
                      TR("FTP Password: ", 
                        INPUT(_type="password", _name="ftppassword")),
                      TR("",
                         INPUT(_type="submit", _value="SUBMIT"))))
    if form.accepts(request.vars,session): 
        table_list = []
        table_backup = []
        backup_path = str(os.sep).join([os.getcwd(), 'applications', 
                        request.application, 'databases', 'cynote_database'])
        backup_uploads_path = str(os.sep).join([os.getcwd(), 'applications', 
                                request.application, 'uploads'])               
        for table in cynotedb.tables:
            rows = cynotedb(cynotedb[table].id).select()
            open(str(os.sep).join([backup_path, table+'.csv']),
                'w').write(str(cynotedb(cynotedb[table].id).select()))    
            table_list.append(table)
            table_backup.append(str(os.sep).join([backup_path, table+'.csv']))
        session["table_list"] = table_list
        session["table_backup"] = table_backup
        backup_list = [x for x in os.listdir(backup_path) 
                        if not os.path.isdir(x)]
        if form.vars.ftpserver: backup_ftp(server=form.vars.ftpserver,
                                            username=form.vars.ftpusername,
                                            password=form.vars.ftppassword,
                                            bpath=backup_path,
                                            blist=backup_list,
                                            buploads=backup_uploads_path)
        redirect(URL(r=request, f="backup_result"))
    return dict(form=form) 
    
def backup_result():
    result = {}
    result["Tables to backup"] = session.pop("table_list")
    result["Backup files"] = session.pop("table_backup")
    result["FTP backup"] = session.pop("ftp", None)
    print result
    return dict(result=result)
    
def backup_ftp(server, username, password, bpath, blist, buploads):
    if session.username == None:
        redirect(URL(r=request, f='../account/log_in'))
    result = []
    try: 
        s = FTP(server)
        result.append(' '.join(['FTP server,', server, ', resolved.']))
    except: result.append('FTP host cannot be resolved')
    try:
        s.login(username, password)
        result.append('Login as ' + username + ' successful')
    except: result.append('Login as ' + username + ' unsuccessful')
    try:
        s.cwd('cynote_database')
        result.append('Changed to cynote_database directory')
    except:
        try:
            s.mkd('cynote_database')
            result.append('cynote_database directory not found.')
            result.append('cynote_database directory created')
            s.cwd('cynote_database')
            result.append('Changed to cynote_database directory')
        except: pass
    for bfile in blist:
        try:
            f = open(bpath + os.sep + bfile, 'rb')
            s.storbinary('STOR ' + bfile, f)
            result.append('Upload file: ' + bfile + ' successful')
        except: result.append('Upload file: ' + bfile + ' unsuccessful')
        try:
            s.rename(bfile, str(now) + ' ' + bfile)
            result.append('Renamed ' + bfile + ' to ' + str(now) + ' ' + \
                          bfile + ' successful')
        except:
            result.append('Renamed ' +  bfile + ' to ' + str(now)+ ' ' + \
                          bfile + ' unsuccessful')
    s.mkd(str(now) + ' uploads')
    result.append(str(now) + ' uploads' + ' directory created')
    s.cwd(str(now) + ' uploads')
    result.append('Changed to ' + str(now) + ' uploads directory')
    for upload_file in [x for x in os.listdir(buploads)]:
        try:
            f = open(buploads + os.sep + upload_file, 'rb')
            s.storbinary('STOR ' + upload_file, f)
            result.append('Upload file: ' + upload_file + ' successful')
        except: result.append('Upload file: ' + upload_file + ' unsuccessful')
    try:
        s.quit()
        result.append('Logout from FTP server')
    except: result.append('FTP terminated withour logging out')
    session['ftp'] = result
    return
