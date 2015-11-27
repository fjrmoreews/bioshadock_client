#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(

    # name of the lib
    name='bioshadock_biotools',

    # version
    version='1.0',

    packages=find_packages(),

    author="Francois Moreews",

    description="Import tool for biotools from Dockerfile",

    include_package_data=True,

    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "License :: Apache 2.0",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Topic :: Communications",
    ],

    scripts = [
            'parseDockerFile.py',
            'registryClient.py'
    ],
    install_requires = [
        'lxml',
        'requests>=2.7.0'
    ],


    license="Apache 2.0",

)

