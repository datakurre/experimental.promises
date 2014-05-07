# -*- coding: utf-8 -*-
import cPickle
import time

from Products.Five.browser import BrowserView
from experimental.futures.exceptions import FutureNotSubmittedError

from experimental.futures.interfaces import (
    IFutures,
    IPromises
)

from experimental import futures


def sleep(value):
    time.sleep(2)
    return value


class PromisesAsyncDemoView(BrowserView):

    @property
    def a(self):
        if 'demo_view_a' in IFutures(self.request):
            return IFutures(self.request)['demo_view_a']
        IPromises(self.request)['demo_view_a'] = lambda: sleep('A')
        return u''

    @property
    def b(self):
        return futures.resultOrSubmit('demo_view_b', u'', sleep, 'B')

    @property
    def c(self):
        if 'demo_view_c' in IFutures(self.request):
            return IFutures(self.request)['demo_view_c']
        IPromises(self.request)['demo_view_c'] = cPickle.dumps((sleep, 'C'))
        return u''

    @property
    def d(self):
        try:
            return futures.result('demo_view_d')
        except FutureNotSubmittedError:
            futures.submit('demo_view_d', sleep, 'D')
            return u''

    @property
    def e(self):
        try:
            return futures.result('demo_view_e')
        except FutureNotSubmittedError:
            futures.submitMultiprocess('demo_view_e', sleep, 'E')
            return u''


class PromisesSyncDemoView(PromisesAsyncDemoView):

    @property
    def a(self):
        IFutures(self.request)['demo_view_a'] = sleep('F')
        return super(PromisesSyncDemoView, self).a

    @property
    def b(self):
        IFutures(self.request)['demo_view_b'] = sleep('G')
        return super(PromisesSyncDemoView, self).b

    @property
    def c(self):
        IFutures(self.request)['demo_view_c'] = sleep('H')
        return super(PromisesSyncDemoView, self).c

    @property
    def d(self):
        IFutures(self.request)['demo_view_d'] = sleep('I')
        return super(PromisesSyncDemoView, self).d

    @property
    def e(self):
        IFutures(self.request)['demo_view_e'] = sleep('J')
        return super(PromisesSyncDemoView, self).e
