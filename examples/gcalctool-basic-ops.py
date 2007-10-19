#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Exercise basic operations
"""

from strongwind import *
from gcalctool import *

app = launchGcalctool()

app.calculatorFrame.assertResult(0)
app.calculatorFrame.changeMode('Basic')

app.calculatorFrame.findPushButton('Numeric 2').click()
app.calculatorFrame.findPushButton('Add').click()
app.calculatorFrame.findPushButton(re.compile('^Numeric 4')).click()
app.calculatorFrame.assertResult('2+4')

app.calculatorFrame.findPushButton('Calculate result').click()
app.calculatorFrame.assertResult(6)

app.calculatorFrame.findPushButton('Divide').click()
app.calculatorFrame.findPushButton('Numeric 3').click()
app.calculatorFrame.assertResult('6/3')

app.calculatorFrame.findPushButton('Calculate result').click()
app.calculatorFrame.assertResult(2)

app.calculatorFrame.findPushButton('Change sign [c]').click()
app.calculatorFrame.assertResult('-(2)')

app.calculatorFrame.findPushButton('Multiply').click()
app.calculatorFrame.findPushButton('Numeric 3').click()
app.calculatorFrame.assertResult('-(2)*3')

app.calculatorFrame.findPushButton('Backspace').click()
app.calculatorFrame.findPushButton('Numeric 7').click()
app.calculatorFrame.assertResult('-(2)*7')

app.calculatorFrame.findPushButton('Calculate result').click()
app.calculatorFrame.assertResult(-14)

app.calculatorFrame.findPushButton('Subtract').click()
app.calculatorFrame.findPushButton('Numeric 6').click()
app.calculatorFrame.assertResult('-14-6')

app.calculatorFrame.findPushButton('Calculate result').click()
app.calculatorFrame.assertResult(-20)

app.calculatorFrame.findPushButton('Clear').click()
app.calculatorFrame.assertResult(0)

app.calculatorFrame.quit()

