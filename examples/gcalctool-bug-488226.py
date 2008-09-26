#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test for bugzilla bug #488226
"""

from strongwind import *
from gcalctool import *

app = launchGcalctool()

app.calculatorFrame.changeMode('Basic')

app.calculatorFrame.findPushButton('Numeric 8').click()
sleep(config.SHORT_DELAY)
app.calculatorFrame.changeMode('Advanced', assertModeChanged=False)

# handle the Change Mode dialog ourselves...
dialog = app.findDialog(None, logName='Changing Modes Clears Calculation')

dialog.keyCombo('Esc')

dialog.assertClosed()

del dialog

procedurelogger.expectedResult('The mode does not change and the result region still displays 8.')

def modeUnchanged():
    return app.calculatorFrame.menuBar.findMenu('View').findCheckMenuItem('Basic').checked and app.calculatorFrame.resultRegion.text == '8'

assert retryUntilTrue(modeUnchanged)

procedurelogger.expectedResult('NOTE: In bugzilla bug #488226, Advanced mode is selected in the View menu, although gcalctool remains in Basic mode.')

# check that we can still change to other modes
app.calculatorFrame.changeMode('Financial', expectChangeModeDialog=True)

procedurelogger.expectedResult('NOTE: In bugzilla bug #488226, gcalctool remains in Basic mode.')

app.calculatorFrame.quit()

