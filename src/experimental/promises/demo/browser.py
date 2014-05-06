# -*- coding: utf-8 -*-
import cPickle
import time

from Products.Five.browser import BrowserView

from experimental.promises.interfaces import (
    IFutures,
    IPromises
)

from experimental.promises import (
    get,
    submit,
    multiprocess
)


def sleep(value):
    # import threading
    # print threading.currentThread(), value
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
        IPromises(self.request)['demo_view_b'] = sleep, 'B'
        return u''

    @property
    def c(self):
        if 'demo_view_c' in IFutures(self.request):
            return IFutures(self.request)['demo_view_c']
        IPromises(self.request)['demo_view_c'] = cPickle.dumps((sleep, 'C'))
        return u''

    @property
    def d(self):
        try:
            return get('demo_view_d')
        except KeyError:
            submit('demo_view_d', sleep, 'D')
            return u''

    @property
    def e(self):
        try:
            return get('demo_view_e')
        except KeyError:
            multiprocess('demo_view_e', sleep, 'E')
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
