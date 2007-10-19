#!/usr/bin/env python

"""
Strongwind is a GUI test automation framework inspired by dogtail.

Strongwind is object-oriented and extensible. You can use Strongwind to build
object-oriented representations of your applications ("application wrappers"),
then reuse the application wrappers to quickly develop many test scripts.
Strongwind scripts generate a human-readable log that contains the action,
expected result and a screen shot of each step.  Most simple actions are logged
automatically.
"""

from distutils.core import setup

setup(name='Strongwind',
      version='0.9',
      description='GUI Test Automation Framework',
      author='Jonathan Tai',
      author_email='jon@tgpsolutions.com',
      url='http://www.medsphere.org/projects/strongwind/',
      packages=['strongwind'],
     )
