# Script for updating CyNote and web2py
# backup_cynote function was adapted from
# http://mail.python.org/pipermail/python-list/2004-March/252709.html

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
    print "Step 2.2: remove contents of %s's uploads directory to \
%s's uploads directory" % (odirectory, ndirectory)
    for f in [t for t in os.walk(odirectory)][0][2]:
        copy2(os.sep.join([odirectory, f]), ndirectory)
        print '%s from %s copied to %s' % (f, odirectory, ndirectory)
    print "Step 2.2 completed"
    print
    # Step 2.3: move ad hoc database definitions from old_cynote's models 
    #           directory to new_cynote's models directory
    odirectory = os.sep.join([old_cynote, 'applications', 'init', 'models',
                              'researchdb_adhoc.py'])
    ndirectory = os.sep.join([new_cynote, 'applications', 'init', 'models',
                              'researchdb_adhoc.py'])
    print "Step 2.3: move ad hoc database definitions from %s's models \
directory to %s's models directory" % (odirectory, ndirectory)
    try:
        copy2(odirectory, ndirectory)
        print '%s copied to %s' % (odirectory, ndirectory)
        print "Step 2.3 completed"
    except IOError:
        print 'researchdb_adhoc.py file not found in old CyNote version.'
    print
    
def process_new_cynote(new_cynote):
    # Step 3: Perform release specific tasks for new cynote version
    from new_cynote_processor import *
    print "Step 3: Process new CyNote (%s) " % (new_cynote)
    new_cynote_process_driver(new_cynote)
    print "Step 3 completed"
    print
    
def backup_data(directory, zipFile):
    # Step 4: create backup file
    z = zipfile.ZipFile(zipFile, 'w')
    print "Step 4.1: Backup file (%s) created" % (zfile)
    print "Step 4.2: Backing up.................."
    def walker(zip, directory, files, root=directory):
        for file in files:
            file = os.path.join(directory, file)
            # yes, the +1 is hacky...
            archiveName = file[len(os.path.commonprefix((root, file)))+1:]
            zip.write( file, archiveName, zipfile.ZIP_DEFLATED )
            print "Backing up: %s" % (file)
    os.path.walk(directory, walker, z)
    z.close()
    print "Step 4 completed"
    print

def remove_old(old_cynote, new_cynote):
    # Step 5: remove old cynote
    print "Step 5: remove %s directory" % (old_cynote)
    os.chdir(new_cynote)
    rmtree(old_cynote)
    print "Step 5 completed"
    print
    
def replace_cynote(old_cynote, new_cynote):
    # Step 6: Copy new cynote to replace deleted old cynote
    print "Step 6: Copy %s to replace deleted %s" % (new_cynote, old_cynote)
    copytree(new_cynote, old_cynote,
             ignore = ignore_patterns('.svn', '.hg', '*.pyc'))
    print "Step 6 completed"
    print


    
def print_headers():
    print '=================================================================='
    print 'Welcome to CyNote updating utility                                '
    print '=================================================================='
    print 'IMPORTANT: Please close your CyNote before updating'
    print '           or there will be irrecoverable errors.'
    print

def get_old_cynote():
    correct = False
    while correct == False:
        old_cynote = raw_input('Please enter your existing CyNote directory: ')
        try:
            app_list = [t for t in
                        os.walk(os.sep.join([old_cynote, 
                                            'applications']))][0][1]
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
                print '%s directory contains the following applications:' % \
                (old_cynote)
                print app_list 
                print 'You cannot use this updating utility without destroying \
                the above mentioned applications'
                print
        except:
            print '%s directory does not contain CyNote. Please try again.' % \
            (old_cynote)    
    return old_cynote

def get_bdirectory():
    correct = False
    while correct == False:
        bdirectory = raw_input('Please enter a directory to keep your \
backup file: ')
        if os.path.isdir(bdirectory):
            correct = True
        else:
            print '%s directory does not exist. Please try again.' % \
            (bdirectory)        
    return bdirectory

if __name__ == '__main__':
    new_cynote = os.getcwd()
    bdirectory = os.getcwd().split(os.sep)[0]
    print_headers()
    old_cynote = get_old_cynote()
    bdirectory = get_bdirectory()
    cleanup_new_cynote(new_cynote)
    old_to_new(old_cynote, new_cynote)
    process_new_cynote(new_cynote)
    zfile = bdirectory + os.sep + 'cynote_backup-' + \
            str(int(time.time())) + '.zip'
    backup_data(old_cynote, zfile)
    if os.path.isfile(zfile):
        print "Backup file %s found" % (zfile)
        print
        print "You may now delete " + str(old_cynote) + " folder"
        print "and rename " + str(new_cynote) + " folder as " + str(old_cynote)
        #remove_old(old_cynote, new_cynote)
        #replace_cynote(old_cynote, new_cynote)
        
        
