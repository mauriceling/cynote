from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

setup(name='cynote',
      version='1.4.1',
      description='Cyber Laboratory Notebook',
      long_description="Laboratory notebook using version control system and \
      independent date-time stamping (as notarization), in order to ensure \
      record accountability, auditing, and conforming to US FDA 21 CFR 21's \
      rule on electronic records.",
      author='Maurice HT Ling',
      author_email='mauriceling@acm.org',
      url='http://cynote.sourceforge.net',
      download_url='https://sourceforge.net/projects/cynote/files/cynote1.4.1.zip/download',
      license = 'GNU General Public License version 3',
      platform = 'OS independent',
      package_dir = {},
      packages = [],
      install_requires = ['biopython==1.50',
                          'pil==1.1.6'],
      classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Information Technology',
                   'Intended Audience :: Science/Research',
                   'Intended Audience :: System Administrators',
                   'License :: OSI Approved :: GNU General Public License \
                   (GPL)',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Scientific/Engineering',
                   'Topic :: Utilities'
                    ],
     )
