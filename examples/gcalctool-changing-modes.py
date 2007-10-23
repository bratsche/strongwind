#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test changing modes (Basic, Advanced, Financial, Scientific)
"""

from strongwind import *
from gcalctool import *

app = launchGcalctool()

app.calculatorFrame.changeMode('Basic')

app.calculatorFrame.changeMode('Advanced')
app.calculatorFrame.changeMode('Financial')
app.calculatorFrame.changeMode('Scientific')
app.calculatorFrame.changeMode('Basic')

app.calculatorFrame.findPushButton('Numeric 1').click()
app.calculatorFrame.changeMode('Advanced', expectChangeModeDialog=True)

app.calculatorFrame.findPushButton('Numeric 2').click()
app.calculatorFrame.changeMode('Financial', expectChangeModeDialog=True)

app.calculatorFrame.findPushButton('Numeric 3').click()
app.calculatorFrame.changeMode('Scientific', expectChangeModeDialog=True)

app.calculatorFrame.findPushButton('Numeric 4').click()
app.calculatorFrame.changeMode('Basic', expectChangeModeDialog=True)

app.calculatorFrame.quit()

