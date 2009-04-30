# Script for updating CyNote and web2py

import os
import zipfile
import time
from shutil import rmtree, copytree, copy2, ignore_patterns

def cleanup_new_cynote(new_cynote):
    # Step 1.1: remove contents of new_cynote's database directory
    directory = os.sep.join([new_cynote, 'applications', 'init', 'databases'])
    print "Step 1.1: remove contents of %s's database directory" % new_cynote
    for f in [t for t in os.walk(directory)][0][2]:
        os.remove(os.sep.join([directory, f]))
        print '%s in %s removed.' % (f, directory)
    print "Step 1.1 completed"
    print
    # Step 1.2: remove contents of new_cynote's uploads directory
    directory = os.sep.join([new_cynote, 'applications', 'init', 'uploads'])
    print "Step 1.2: remove contents of %s's uploads directory" % new_cynote
    for f in [t for t in os.walk(directory)][0][2]:
        os.remove(os.sep.join([directory, f]))
        print '%s in %s removed.' % (f, directory)
    print "Step 1.2 completed"
    print

def old_to_new(old_cynote, new_cynote):
    # Step 2.1: remove contents of old_cynote's database directory to
    #           new_cynote's database directory
    odirectory = os.sep.join([old_cynote, 'applications', 'init', 'databases'])
    ndirectory = os.sep.join([new_cynote, 'applications', 'init', 'databases'])
    print "Step 2.1: remove contents of %s's database directory to \
%s's database directory" % (odirectory, ndirectory)
    for f in [t for t in os.walk(odirectory)][0][2]:
        copy2(os.sep.join([odirectory, f]), ndirectory)
        print '%s from %s copied to %s' % (f, odirectory, ndirectory)
    print "Step 2.1 completed"
    print
    # Step 2.2: remove contents of old_cynote's uploads directory to
    #           new_cynote's uploads directory
    odirectory = os.sep.join([old_cynote, 'applications', 'init', 'uploads'])
    ndirectory = os.sep.join([new_cynote, 'applications', 'init', 'uploads'])
    print "Step 2.1: remove contents of %s's uploads directory to \
%s's uploads directory" % (odirectory, ndirectory)
    for f in [t for t in os.walk(odirectory)][0][2]:
        copy2(os.sep.join([odirectory, f]), ndirectory)
        print '%s from %s copied to %s' % (f, odirectory, ndirectory)
    print "Step 2.1 completed"
    print

def backup_data(old_cynote, bdirectory):
    # Step 3.1: create backup file
    zfile = bdirectory + os.sep + 'cynote_backup-' + \
            str(int(time.time())) + '.zip'
    z = zipfile.ZipFile(zfile, 'w')
    print "Step 3.1: Backup file (%s) created" % (zfile)
    # Step 3.2: backup database directory 
    directory = os.sep.join([old_cynote, 'applications', 'init', 'databases'])
    print "Step 3.2: Backup database files from %s to %s" % (directory, zfile)
    os.chdir(directory)
    print "Changed working directory to %s" % (directory)
    for f in [t for t in os.walk(directory)][0][2]:
        z.write(os.sep.join([directory, f]))
        print "%s file backup to %s" % (f, zfile)
    # Step 3.3: backup uploads directory 
    directory = os.sep.join([old_cynote, 'applications', 'init', 'uploads'])
    print "Step 3.3: Backup upload files from %s to %s" % (directory, zfile)
    os.chdir(directory)
    print "Changed working directory to %s" % (directory)
    for f in [t for t in os.walk(directory)][0][2]:
        z.write(os.sep.join([directory, f]))
        print "%s file backup to %s" % (f, zfile)
    z.close()
    print "Step 3 completed"
    print

def remove_old(old_cynote, new_cynote):
    # Step 4: remove old cynote
    print "Step 4: remove %s directory" % (old_cynote)
    os.chdir(new_cynote)
    rmtree(old_cynote)
    print "Step 4 completed"
    print

def replace_cynote(old_cynote, new_cynote):
    # Step 5: Copy new cynote to replace deleted old cynote
    print "Step 5: Copy %s to replace deleted %s" % (new_cynote, old_cynote)
    copytree(new_cynote, old_cynote,
             ignore = ignore_patterns('.svn', '*.pyc'))
    print "Step 5 completed"
    print
    

if __name__ == '__main__':
    new_cynote = os.getcwd()
    bdirectory = os.getcwd().split(os.sep)[0]
    print '=================================================================='
    print 'Welcome to CyNote updating utility                                '
    print '=================================================================='
    print 'IMPORTANT: Please close your CyNote before updating'
    print '           or there will be irrecoverable errors.'
    print
    correct = False
    while correct == False:
        old_cynote = raw_input('Please enter your existing CyNote directory: ')
        try:
            app_list = [t for t in
                        os.walk(os.sep.join([old_cynote, 'applications']))][0][1]
##            print app_list
            try: app_list.remove('admin')
            except: pass
            try: app_list.remove('examples')
            except: pass
            try: app_list.remove('welcome')
            except: pass
            try: app_list.remove('init')
            except: pass
            if len(app_list) == 0: correct = True
            else:
		print
                print '%s directory contains the following applications:' % (old_cynote)
		print app_list 
		print 'You cannot use this updating utility without destroying the above mentioned applications'
		print
        except:
            print '%s directory does not contain CyNote. Please try again.' % (old_cynote)    
    correct = False
    while correct == False:
        bdirectory = raw_input('Please enter a directory to keep your backup file: ')
        if os.path.isdir(bdirectory):
            correct = True
        else:
            print '%s directory does not exist. Please try again.' % (bdirectory)        
    cleanup_new_cynote(new_cynote)
    old_to_new(old_cynote, new_cynote)
    backup_data(old_cynote, bdirectory)
    remove_old(old_cynote, new_cynote)
    replace_cynote(old_cynote, new_cynote)
