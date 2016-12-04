#!/usr/bin/env python
import glob
import sys
sys.path.append('../stage/lib')
sys.path.append('/opt/dashboard/lib') 

from dashboard.distutils.config import setup

"""
Default distutils 'setup' method overwritten.
"""
setup(
    packages=[

  
    ],
    package_dir={'': 'lib'}, 
    data_files=[
        ('deftmon', glob.glob('templates/*html')),
        ('deftmon', glob.glob('templates/*js')), 
        ('deftmon/media/css', glob.glob('templates/media/css/*css')),
        ('deftmon/media/images', glob.glob('templates/media/images/*'))
    ]
)
