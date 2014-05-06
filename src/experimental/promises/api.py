# -*- coding: utf-8 -*-
import cPickle
from zope.globalrequest import getRequest
from experimental.promises.interfaces import (
    IFutures,
    IPromises
)

_marker = object()


def get(key, default=_marker):
    """Get the required future. When the future is not available, return
    the given default or raise KeyError. If the future is an exception,
    it will be raised instead of returned. If the future is a KeyError,
    it will be raised as a value of an Exception instead.
    """
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
    """Submit promise (name, function, arguments.., keyword arguments...)
    for the default (thread) executor

    """
    request = getRequest()
    IPromises(request)[key] = {
        'fn': fn,
        'args': args,
        'kwargs': kwargs
    }
    return True  # to enable submit(...) and ...


def getOrSubmit(key, placeholder, fn, *args, **kwargs):
    """Get the required future. When the future is not available,
    submit the given promise and return the given placeholder instead.

    """
    try:
        return get(key)
    except KeyError:
        submit(key, fn, *args, **kwargs)
    return placeholder


def submitMultiprocess(key, fn, *args, **kwargs):
    """Submit promise (name, function, arguments.., keyword arguments...)
    for the process pool executor.

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


def getOrSubmitMultiprocess(key, placeholder, fn, *args, **kwargs):
    """Get the required future. When the future is not available,
    submit the given promise and return the given placeholder instead
    (for the process pool executor).

    """
    try:
        return get(key)
    except KeyError:
        submitMultiprocess(key, fn, *args, **kwargs)
    return placeholder
