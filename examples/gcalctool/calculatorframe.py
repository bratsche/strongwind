# -*- coding: utf-8 -*-

from strongwind import *
from gcalctool import *

class CalculatorFrame(accessibles.Frame):
    logName = 'Calculator'

    def __init__(self, accessible):
        super(CalculatorFrame, self).__init__(accessible)

        self.menuBar = self.findMenuBar('')
        self.resultRegion = self.findEditbar('')

    def assertResult(self, result):
        'Raise an exception if the result region does not match the given result'

        procedures.expectedResult('The result region displays %s.' % result)

        def resultMatches():
            return self.resultRegion.text == str(result)

        assert retryUntilTrue(resultMatches)

    def changeMode(self, mode):
        '''
        Change the mode

        Mode can be one of: Basic, Advanced, Financial, or Scientific.
        '''

        self.menuBar.select(['View', mode])

        if self.resultRegion.text != '0': # FIXME: if we're already on this mode, the dialog won't pop up
            self.app.findDialog(None, logName='Changing Modes Clears Calculation')._clickPushButton('Change Mode')

        procedurelogger.expectedResult('The mode changes to %s mode.' % mode)

    def quit(self):
        'Quit gcalctool'

        self.menuBar.select(['Calculator', 'Quit'])

        self.assertClosed()

    def assertClosed(self):
        super(CalculatorFrame, self).assertClosed()

        self.app.assertClosed()

