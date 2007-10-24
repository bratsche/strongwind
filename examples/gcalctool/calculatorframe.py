# -*- coding: utf-8 -*-

from strongwind import *
from gcalctool import *

class CalculatorFrame(accessibles.Frame):
    logName = 'Calculator'

    def __init__(self, accessible):
        super(CalculatorFrame, self).__init__(accessible)

        # get a reference to commonly-used child widgets
        self.menuBar = self.findMenuBar('')
        self.resultRegion = self.findEditbar('')

    def assertResult(self, result):
        'Raise an exception if the result region does not match the given result'

        procedurelogger.expectedResult('The result region displays %s.' % result)

        def resultMatches():
            return self.resultRegion.text == str(result)

        assert retryUntilTrue(resultMatches)

    def changeMode(self, mode, expectChangeModeDialog=False, assertModeChanged=True):
        '''
        Change the mode

        Mode can be one of: Basic, Advanced, Financial, or Scientific.
        '''

        if expectChangeModeDialog:
            sleep(config.SHORT_DELAY)

        self.menuBar.select(['View', mode])

        if expectChangeModeDialog:
            self.app.findDialog(None, logName='Changing Modes Clears Calculation')._clickPushButton('Change Mode')

        if assertModeChanged:
            procedurelogger.expectedResult('The mode changes to %s mode and the result region displays 0.' % mode)

            def modeChanged():
                return self.menuBar.findMenu('View').findCheckMenuItem(mode).checked and self.resultRegion.text == '0'

            assert retryUntilTrue(modeChanged)

    def quit(self):
        'Quit gcalctool'

        self.menuBar.select(['Calculator', 'Quit'])

        self.assertClosed()

    def assertClosed(self):
        super(CalculatorFrame, self).assertClosed()

        # if the calculator window closes, the entire app should close.  assert that this is true 
        self.app.assertClosed()

