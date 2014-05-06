# -*- coding: utf-8 -*-
from experimental.promises import (
    get,
    submit
)


def _retrieveFeed(self):
    try:
        return get(self.url)
    except KeyError:
        submit(self.url, self._old__retrieveFeed)
        return False
