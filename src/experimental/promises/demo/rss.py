# -*- coding: utf-8 -*-
from experimental.promises import getOrSubmit


def _retrieveFeed(self):
    return getOrSubmit(self.url, self._old__retrieveFeed) or False
