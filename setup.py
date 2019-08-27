#!/usr/bin/env python
"""
xontrib-per-directory-history
-----
Per-directory history for xonsh, like zsh's
https://github.com/jimhester/per-directory-history

Restricts history to those that were executed in the current
directory, with keybindings to switch between that and global history.
"""

from setuptools import setup


setup(
    name='xontrib-per-directory-history',
    version='0.1',
    description="Per-directory history for xonsh, like zsh's https://github.com/jimhester/per-directory-history",
    long_description=__doc__,
    license='MIT',
    url='https://github.com/eppeters/xontrib-per-directory-history',
    author='Eddie Peters',
    author_email='edward.paul.peters@gmail.com',
    packages=['xontrib'],
    package_dir={'xontrib': 'xontrib'},
    package_data={'xontrib': ['*.xsh']},
    platforms='any',
    install_requires=[
        'xonsh>=0.9.3',
    ],
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: System :: Shells',
        'Topic :: System :: System Shells',
    ]
)
