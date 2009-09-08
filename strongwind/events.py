# -*- coding: utf-8 -*-
#
# Strongwind
# Copyright (C) 2009 Novell, Inc.
# 
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
# 
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# 
# Authors:
#      Brad Taylor <brad@getcoded.net>
#

import threading
import pyatspi
import utils
import accessibles

class EventListener(threading.Thread):
    '''
    Listens for events using pyatspi.Registry and provides an easy mechanism
    to test that an event was fired.

    Example:

    >>> from strongwind import *
    Error importing yaml module; tags will not be parsed
    events: 
    >>> import pyatspi
    >>> desktop = pyatspi.Registry.getDesktop(0)
    >>> nautilus = Application(pyatspi.findDescendant(desktop, lambda x: x.name == 'nautilus', breadth_first=True))
    >>> icon_view = nautilus.findLayeredPane('Icon View')
    >>> icon_view.clearSelection()
    >>> listener = EventListener()
    >>> with listener.listenTo(icon_view):
    ...     icon_view.selectChild(0)
    >>> listener.containsEvent(type='object:selection-changed')
    True
    >>> icon_view.clearSelection()
    >>> with listener.listenTo(icon_view):
    ...     icon_view.selectChild(1)
    ...     listener.waitForEvent(type='object:selection-changed')
    True
    '''
    def __init__(self, condition=threading.Condition()):
        threading.Thread.__init__(self)

        self.cond = condition
        self.daemon = True
        self.events = {}
        self.targets = []

        self.all_event_types = pyatspi.EVENT_TREE.keys()
        for sub_events in pyatspi.EVENT_TREE.itervalues():
            self.all_event_types.extend(sub_events)

        self.all_event_types = list(set([
            event.strip(':') for event in self.all_event_types
        ]))
        self.all_event_types.sort()

        self.thread_listening = False
        self.thread_listening_cond = threading.Condition()

    def listenTo(self, targets):
        '''
        Returns an object that can be used with the with keyword.
        
        @param targets: the accessibles to listen to
        '''
        class __listenClass:
            def __init__(self, listener, targets):
                self.listener = listener
                self.targets = targets

            def __enter__(self):
                self.listener.clearQueuedEvents()
                self.listener.start(targets)

            def __exit__(self, type, value, traceback):
                self.listener.stop()

        return __listenClass(self, targets)


    def start(self, targets, *args, **kwargs):
        '''
        Start pyatspi.Registry's main loop, causing it to start listening for
        events.

        @param targets: the accessibles to listen to
        '''
        if not isinstance(targets, list):
            targets = (targets,)

        with self.cond:
            self.targets = [self._unwrapAccessible(t) for t in targets]

        pyatspi.Registry.registerEventListener(self._eventFired, \
                                               *self.all_event_types)

        with self.thread_listening_cond:
            self.thread_listening = True
            self.thread_listening_cond.notifyAll()

        if not self.is_alive():
            threading.Thread.start(self, *args[1:], **kwargs)

    def run(self):
        '''
        Runs pyatspi.Registry's main loop in a thread.  This should not be used
        externally.  Instead, use .start().
        '''
        self.thread_listening_cond.acquire()

        while True:
            if self.thread_listening:
                # Make sure we release the lock before we block
                self.thread_listening_cond.release()
                pyatspi.Registry.start()
                self.thread_listening_cond.acquire()
            self.thread_listening_cond.wait()

        self.thread_listening_cond.release()

    def stop(self):
        '''
        Stops pyatspi.Registry's main loop, causing it to stop listening to
        events.
        '''
        pyatspi.Registry.stop()

        with self.thread_listening_cond:
            self.thread_listening = False
            self.thread_listening_cond.notifyAll()
    
        pyatspi.Registry.deregisterEventListener(self._eventFired, \
                                                 *self.all_event_types)

    def containsEvent(self, target=None, type=None, qty=None):
        '''
        Returns if the EventListener has seen a event of the given type on the
        given target.

        @param target: the requested event target
        @param type: the type of event to listen for
        @param qty: how many events should be fired
        @return: returns True if we've seen the event, False otherwise
        @rtype: boolean
        '''
        num = self._getNumEvents(self._unwrapAccessible(target), type)
        if qty is None:
            return num > 0
        return qty == num

    def waitForEvent(self, target=None, type=None, qty=None):
        '''
        Waits until the event occurs and returns True.  If the event does not
        occur within config.RETRY_TIMES * config.RETRY_INTERVAL seconds,
        returns False.

        @param target: the requested event target, or None
        @param type: the type of event to listen to, or None
        @param qty: how many events should be fired
        @return: returns True if the event occured, False otherwise
        @rtype: boolean
        '''
        return utils.retryUntilTrue(self.containsEvent, \
                                    args=(self._unwrapAccessible(target),
                                          type, qty))

    def clearQueuedEvents(self):
        '''
        Clears the internal list of events used for querying.
        '''
        with self.cond:
            self.events.clear()

    def _getNumEvents(self, target=None, type=None):
        '''
        Returns the number of events matching the provided criteria.

        @param target: the requested event target, or None
        @param type: the type of event to listen to, or None
        @return: the number of events that match
        @rtype: int
        '''
        with self.cond:
            if target:
                if target not in self.events:
                    return 0

                if type:
                    return len(filter(lambda x: x.type == type, self.events[target]))
                else:
                    return len(self.events[target])
            else:
                if type:
                    return len(filter(lambda x: x.type == type, sum(self.events.values(), [])))
                else:
                    return len(self.events.values())
        return 0

    def _eventFired(self, evt):
        with self.cond:
            if evt.source in self.targets:
                if not self.events.has_key(evt.source):
                    self.events[evt.source] = []
                self.events[evt.source].append(evt)
                self.cond.notifyAll()
        return False

    def _unwrapAccessible(self, acc):
        if isinstance(acc, accessibles.Accessible):
            return acc._accessible
        return acc
