#!/usr/bin/env python
from setuptools import setup
import sys
try:
        import py2exe
except ImportError:
        pass

py2exe_opts = {
        'options': {'py2exe': {
                'bundle_files': 1,
                'compressed': 1,
                'optimize': 2
        }},
        'console': [{
                'script': './catscrape/__main__.py',
                'dest_base': 'catscrape',
        }]
}

if len(sys.argv) >= 2 and sys.argv[1] == 'py2exe':
        opts = py2exe_opts
else:
        opts = {}

setup(name='catscrape',
        version='0.1',
        author='Jai Grimshaw',
        license='MIT',
        install_requires=[
                'beautifulsoup4',
        ],
        packages=['catscrape'],
        scripts=['bin/catscrape'],
        entry_points= {
                'console_scripts': ['catscrape=catscrape.__main__.main'],
        },
        zip_safe=True,
        **opts
)
