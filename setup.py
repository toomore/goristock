#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import grs

long_description = open('./README.rest', 'r').read()

setup(name='grs',
      version=grs.__version__,
      description='台灣股市股票股價擷取（Fetch TWSE stock data）',
      long_description=long_description,
      author='Toomore Chiang',
      author_email='toomore0929@gmail.com',
      url='https://github.com/toomore/goristock/tree/grs_rewrite',
      packages=['grs'],
      include_package_data=True,
      license='MIT',
      install_requires=[],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Financial and Insurance Industry',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Chinese (Traditional)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Office/Business :: Financial :: Investment',
          ],
     )
