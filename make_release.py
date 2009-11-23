# Script to make a copy of CyNote for zipping and release

import os
import sys
from shutil import rmtree, copytree, copy2, ignore_patterns

def cleanup_cynote(new_cynote):
    # Step 1.1: remove contents of CyNote's database directory
    directory = os.sep.join([new_cynote, 'applications', 'init', 'databases'])
    print "Step 1.1: remove contents of %s's database directory" % new_cynote
    for f in [t for t in os.walk(directory)][0][2]:
        os.remove(os.sep.join([directory, f]))
        print '%s in %s removed.' % (f, directory)
    print "Step 1.1 completed"
    print
    # Step 1.2: remove contents of CyNote's uploads directory
    directory = os.sep.join([new_cynote, 'applications', 'init', 'uploads'])
    print "Step 1.2: remove contents of %s's uploads directory" % new_cynote
    for f in [t for t in os.walk(directory)][0][2]:
        os.remove(os.sep.join([directory, f]))
        print '%s in %s removed.' % (f, directory)
    print "Step 1.2 completed"
    print
    
def copy_cynote(release, new_cynote):
    # Step 2: Copy CyNote to release directory
    print "Step 2: Copy %s to release directory: %s" % (new_cynote, release)
    copytree(new_cynote, release,
             ignore = ignore_patterns('.svn', '*.pyc'))
    print "Step 2 completed"
    print
    

if __name__=='__main__':
    new_cynote = os.getcwd()
    cleanup_cynote(new_cynote)
    copy_cynote(sys.argv[1], new_cynote)
    