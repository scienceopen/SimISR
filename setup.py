#!/usr/bin/env python
"""
setup.py
This is the setup file for the RadarDataSim python package

@author: John Swoboda
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'An ISR data simulator',
    'author': 'John Swoboda',
    'url': '',
    'download_url': 'https://github.com/jswoboda/RadarDataSim.git',
    'author_email': 'swoboj@bu.edu',
    'version': '0.2',
    'install_requires': ['numpy', 'scipy', 'tables'],
    'packages': ['RadarDataSim','beamtools','radarsystools'],
    'scripts': [],
    'name': 'RadarDataSim'
}

setup(**config)