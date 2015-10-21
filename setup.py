# Setup file for feedstail
from setuptools import setup


setup( name             = "jsontail"
     , description      = "A tail-f-like utility for JSON feeds"
     , long_description = open('README.rst').read()
     , license          = "GNU General Public License v3"
     , url              = "https://github.com/jamestwebber/jsontail"

     , author           = "James Webber"
     , author_email     = "jamestwebber at gmail dot com"

     , version          = '0.1'
     , scripts          = ['bin/jsontail']
     , packages         = ['jsontail']
     , data_files       = [('', ['README.rst', 'LICENSE.txt'])]
     , install_requires = ['argparse', 'requests']

     , classifiers      =
         [ "Development Status :: 3 - Alpha"
         , "License :: OSI Approved :: GNU General Public License (GPL)"
         , "Operating System :: OS Independent"
         , "Programming Language :: Python :: 2.7"
         , "Topic :: Utilities"
         ]
      )

