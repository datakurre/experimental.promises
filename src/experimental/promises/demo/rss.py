# -*- coding: utf-8 -*-
from zope.globalrequest import getRequest
from experimental.promises.interfaces import IFutures, IPromises


def _retrieveFeed(self):
    request = getRequest()
    if self.url in IFutures(request):
        return IFutures(request)[self.url]
    else:
        IPromises(request)[self.url] = self._old__retrieveFeed
        return False
