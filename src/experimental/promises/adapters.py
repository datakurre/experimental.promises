# -*- coding: utf-8 -*-
from ZPublisher.BaseRequest import BaseRequest
from zope.annotation import (
    IAttributeAnnotatable,
    IAnnotations
)
from zope.interface import (
    implementer,
    alsoProvides
)
from experimental.promises.interfaces import (
    IPromises,
    IFutures,
    IContainsPromises
)
from venusianconfiguration import configure

PROMISES_KEY = 'experimental.promises'
FUTURES_KEY = 'experimental.promises.futures'


with configure.class_(class_=BaseRequest):
    configure.implements(interface=IAttributeAnnotatable)


@configure.adapter.factory(for_=IAttributeAnnotatable)
@implementer(IPromises)
def get_promises(request):
    alsoProvides(request, IContainsPromises)
    annotations = IAnnotations(request)
    annotations.setdefault(PROMISES_KEY, {})
    return annotations.get(PROMISES_KEY)


@configure.adapter.factory(for_=IAttributeAnnotatable)
@implementer(IFutures)
def get_futures(request):
    annotations = IAnnotations(request)
    annotations.setdefault(FUTURES_KEY, {})
    return annotations.get(FUTURES_KEY)
