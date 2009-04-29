# Script for updating CyNote and web2py

import os
import zipfile
from shutil import rmtree, copytree, copy2, ignore_patterns

old_cynote = os.sep.join([os.getcwd().split(os.sep)[0], 'cynote'])
new_cynote = os.getcwd()
bdirectory = os.getcwd().split(os.sep)[0]

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
    pass

def remove_old(old_cynote):
    # Step 4: remove old cynote
    print "Step 4: remove %s directory" % (old_cynote)
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
    

cleanup_new_cynote(new_cynote)
old_to_new(old_cynote, new_cynote)
backup_data(old_cynote, bdirectory)
remove_old(old_cynote)
replace_cynote(old_cynote, new_cynote)
