from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(name='cynote',
      version='1.0',
      description='Cyber Laboratory Notebook',
      long_description='Laboratory notebook using version control system for backups and independent date-time stamping (which may be a form of notarization), in order to ensure record accountability and auditing.',
      author='Maurice HT Ling',
      author_email='mauriceling@acm.org',
      url='http://cynote.sourceforge.net',
      license = 'GNU General Public License version 2',
      platform = 'OS independent',
      package_dir = {},
      packages = [],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: GNU General Public License (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Utilities'
                    ],
     )
