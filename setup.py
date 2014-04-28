# coding=utf-8

import os

__author__ = 'paoolo'

pwd = os.path.dirname(os.path.abspath(__file__))

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('%s/requirements.txt' % pwd) as f:
    required = f.read().splitlines()

setup(
    name='air-python',
    packages=['air', 'air.appliance', 'air.machine', 'air.mapping', 'air.property'],
    package_dir={'air': '%s/src/air' % pwd,
                 'air.appliance': '%s/src/air/appliance' % pwd,
                 'air.machine': '%s/src/air/machine' % pwd,
                 'air.mapping': '%s/src/air/mapping' % pwd,
                 'air.property': '%s/src/air/property' % pwd},
    install_requires=required,
    version='1.0',
    description='AIR REST API wrapper in python',
    author=u'Paweł Suder',
    author_email='pawel@suder.info',
    url='https://gitlab.dev.cyfronet.pl/atmosphere/nagios-probe',
    download_url='https://gitlab.dev.cyfronet.pl/paoolo/air-python/repository/archive.zip',
    keywords=['air', 'atmosphere'],
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        ],
    long_description='''\
'''
)