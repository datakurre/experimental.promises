# -*- coding: utf-8 -*-
from experimental import futures


def _retrieveFeed(self):
    return futures.resultOrSubmit(self.url, False, self._old__retrieveFeed)
