# -*- coding: utf-8 -*-
import cPickle
from zope.globalrequest import getRequest
from experimental.promises.interfaces import (
    IFutures,
    IPromises
)

_marker = object()


def get(key, default=_marker):
    """Get the required future, or default, or raise KeyError"""
    request = getRequest()

    try:
        value = IFutures(request)[key]
    except KeyError:
        if default is _marker:
            raise
        value = default

    if isinstance(value, KeyError):
        # KeyError is reserved to be raised when future not yet resolved
        raise Exception(value)
    elif isinstance(value, Exception):
        raise value

    return value


def submit(key, fn, *args, **kwargs):
    """Submit promise for the default executor"""
    request = getRequest()
    IPromises(request)[key] = {
        'fn': fn,
        'args': args,
        'kwargs': kwargs
    }
    return True  # to enable submit(...) and ...


def getOrSubmit(key, fn, *args, **kwargs):
    try:
        return get(key)
    except KeyError:
        submit(key, fn, *args, **kwargs)
    return None  # to enable getOrSubmit(...) or ...


def submitMultiprocess(key, fn, *args, **kwargs):
    """Submit promise for process pool executor

    Args are pickled, because only pickleable promises can be resolved with
    MultiProcessExecutor and unpickleable args raises an exception, which
    cannot be caught.

    """
    request = getRequest()
    IPromises(request)[key] = cPickle.dumps({
        'fn': fn,
        'args': args,
        'kwargs': kwargs
    })
    return True  # to enable submit(...) and ...


def getOrSubmitMultiprocess(key, fn, *args, **kwargs):
    try:
        return get(key)
    except KeyError:
        submitMultiprocess(key, fn, *args, **kwargs)
    return None  # to enable getOrSubmitMultiprocess(...) or ...
