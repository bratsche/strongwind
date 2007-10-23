# -*- coding: utf-8 -*-

'Application wrapper for gcalctool'

from strongwind import *

import os

def launchGcalctool(exe=None):
    'Launch gcalctool with accessibility enabled and return a Gcalctool object'

    if exe is None:
        exe = '/usr/bin/gcalctool'

    args = [exe]

    (app, subproc) = cache.launchApplication(args=args)

    gcalctool = Gcalctool(app, subproc)
    cache.addApplication(gcalctool)

    # calculatorFrame's assertClosed() calls self.app.assertClosed(), but if the
    # app has closed already, self.app will return None.  Normally, we would
    # cache self.app in the constructor of the calculatorFrame class, but at the
    # time the calculatorFrame's constructor is run, cache.getApplication(self._app_id) 
    # resolves to an accessible.Application().  We promote the application to
    # a Gcalctool object here, so we must set calculatorFrame.app immediately
    # afterward.
    gcalctool.calculatorFrame.app = gcalctool

    return gcalctool

class Gcalctool(accessibles.Application):
    def __init__(self, accessible, subproc=None):
        'Get a reference to the calculator window'
        super(Gcalctool, self).__init__(accessible, subproc)

        self.findFrame(re.compile('^Calculator'), logName='Calculator')

