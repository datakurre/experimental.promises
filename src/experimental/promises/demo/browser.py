# -*- coding: utf-8 -*-
import time

from Products.Five.browser import BrowserView

from experimental.promises.interfaces import (
    IFutures,
    IPromises
)


def sleep(value):
    time.sleep(1)
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
        if 'demo_view_b' in IFutures(self.request):
            return IFutures(self.request)['demo_view_b']
        IPromises(self.request)['demo_view_b'] = lambda: sleep('B')
        return u''

    @property
    def c(self):
        if 'demo_view_c' in IFutures(self.request):
            return IFutures(self.request)['demo_view_c']
        IPromises(self.request)['demo_view_c'] = lambda: sleep('C')
        return u''

    @property
    def d(self):
        if 'demo_view_d' in IFutures(self.request):
            return IFutures(self.request)['demo_view_d']
        IPromises(self.request)['demo_view_d'] = lambda: sleep('D')
        return u''


class PromisesSyncDemoView(PromisesAsyncDemoView):

    @property
    def a(self):
        IFutures(self.request)['demo_view_a'] = sleep('E')
        return super(PromisesSyncDemoView, self).a

    @property
    def b(self):
        IFutures(self.request)['demo_view_b'] = sleep('F')
        return super(PromisesSyncDemoView, self).b

    @property
    def c(self):
        IFutures(self.request)['demo_view_c'] = sleep('G')
        return super(PromisesSyncDemoView, self).c

    @property
    def d(self):
        IFutures(self.request)['demo_view_d'] = sleep('H')
        return super(PromisesSyncDemoView, self).d
