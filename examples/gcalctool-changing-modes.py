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
sleep(config.SHORT_DELAY)
app.calculatorFrame.changeMode('Advanced')

app.calculatorFrame.findPushButton('Numeric 2').click()
sleep(config.SHORT_DELAY)
app.calculatorFrame.changeMode('Financial')

app.calculatorFrame.findPushButton('Numeric 3').click()
sleep(config.SHORT_DELAY)
app.calculatorFrame.changeMode('Scientific')

app.calculatorFrame.findPushButton('Numeric 4').click()
sleep(config.SHORT_DELAY)
app.calculatorFrame.changeMode('Basic')

app.calculatorFrame.quit()

