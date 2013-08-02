# try something like
import datetime
emaildb=SQLDB('sqlite://emaildb.db')

TOP_MESSAGE="(Email form)"
VALUE="(default message)"

emaildb.define_table('message',
                     SQLField('your_name', requires=IS_NOT_EMPTY()),
                     SQLField('your_email', requires=IS_EMAIL()),
                     SQLField('your_message', 'text', default=VALUE),
                     SQLField('timestamp', default=str(datetime.datetime.now())))

emaildb.define_table('recipient',
                     SQLField('name', requires=IS_NOT_EMPTY()),
                     SQLField('email', requires=IS_EMAIL()))   
   
def email_user(sender,message,subject="group notice"):
    import smtplib
    fromaddr=sender
    toaddrs=[x.email for x in emaildb().select(emaildb.recipient.email)]
    msg="From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s"%(fromaddr,", ".join(toaddrs),subject,message)
    server = smtplib.SMTP('pop.gmail.com:25')
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()
