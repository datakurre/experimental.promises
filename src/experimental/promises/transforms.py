# -*- coding: utf-8 -*-
import StringIO
import threading
import collections
from App.config import getConfiguration
import cPickle
from concurrent import futures

from zope.interface import Interface
from zope.component import adapts
from plone.transformchain.interfaces import ITransform
from zope.interface import implements
from ZPublisher.Iterators import IStreamIterator
from ZServer.PubCore.ZEvent import Wakeup
from ZServer.Producers import iterator_producer
from ZServer.HTTPResponse import ChannelPipe

from experimental.promises.interfaces import (
    IContainsPromises,
    IPromises,
    IFutures
)


class zhttp_channel_wrapper(object):

    def __init__(self, channel):
        self._channel = channel

        self._mutex = threading.Lock()
        self._deferred = None
        self._released = False

    def _push(self, producer, send=1):
        self._channel.push(producer, send)

    def push(self, producer, send=1):
        if not isinstance(producer, iterator_producer):
            return  # trash all but promise iterator
        if not isinstance(producer.iterator, PromiseWorkerStreamIterator):
            return  # trash all but promise iterator

        with self._mutex:
            if not self._released:
                self._deferred = (producer, send)
            else:
                self._push(producer, send)

    def release(self):
        with self._mutex:
            if self._deferred is not None:
                self._push(*self._deferred)
            self._released = True
        Wakeup()

    def __getattr__(self, key):
        return getattr(self._channel, key)


def safe_promise(value):
    """Parse promise value into its fn, args and kwargs"""

    if isinstance(value, dict):
        fn = value.get('fn')
        args = value.get('args', [])
        kwargs = value.get('kwargs', {})

    elif isinstance(value, collections.Iterable) and len(value):
        fn = value[0]
        args = value[1:]
        kwargs = {}

    else:
        fn = value
        args = []
        kwargs = {}

    return fn, args, kwargs


def safe_submit(executor, value):
    """Parse promise value into its fn, args and kwargs and submit
    it for the given executor"""
    fn, args, kwargs = safe_promise(value)
    return executor.submit(fn, *args, **kwargs)


class PromiseWorkerStreamIterator(StringIO.StringIO):

    implements(IStreamIterator)

    def __init__(self, promises, request, response):
        # Mimic 'file' because someone may expect IStreamIterator to be one
        StringIO.StringIO.__init__(self)

        # Reset response
        self._zrequest = request.retry()
        self._zrequest.retry_count -= 1
        self._zrequest.response.stdout = ChannelPipe(response.stdout._request)
        response._retried_response = None

        # Wrap channel
        self._channel = response.stdout._channel
        self._wrapped_channel = zhttp_channel_wrapper(self._channel)
        response.stdout._channel = self._wrapped_channel

        # Enable stream iterator support
        response.setHeader('content-length', '0')  # required by ZPublisher

        # Init promises and futures
        self._promises = promises
        self._futures = IFutures(request)

        # Init Lock
        self._mutex = threading.Lock()

        # Read the product config
        product_config = getConfiguration().product_config
        configuration = product_config.get('experimental.promises', dict())
        try:
            max_workers = int(configuration.get('max_workers', 5))
        except ValueError:
            max_workers = 5

        # Resolve promises into futures
        thread_executor = futures.ThreadPoolExecutor(max_workers=max_workers)
        process_executor = futures.ProcessPoolExecutor(max_workers=max_workers)

        futures_to_promises = dict([
            (safe_submit(process_executor, cPickle.loads(value)), name)
            for name, value in self._promises.items()
            if isinstance(value, str)
        ])
        futures_to_promises.update(dict([
            (safe_submit(thread_executor, value), name)
            for name, value in self._promises.items()
            if not isinstance(value, str)
        ]))

        for future in futures.as_completed(futures_to_promises):
            promise = futures_to_promises[future]
            try:
                value = future.result()
            except Exception as e:
                value = e
            self.record(promise, value)

        process_executor.shutdown(wait=True)
        thread_executor.shutdown(wait=True)

    def record(self, name, value):
        with self._mutex:
            self._futures[name] = value
            if set(self._promises).issubset(set(self._futures)):
                self._wrapped_channel.release()

    def next(self):
        if self._futures:
            IFutures(self._zrequest).update(self._futures)
            self._futures = {}  # mark consumed to raise StopIteration

            from ZServer.PubCore import handle
            handle('Zope2', self._zrequest, self._zrequest.response)
        else:
            raise StopIteration

    def __len__(self):
        return 0  # promise worker cannot return any sane value


class PromisesTransform(object):
    implements(ITransform)
    adapts(Interface, IContainsPromises)

    order = 7000  # before p.a.theming and p.a.blocks

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def transformString(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformUnicode(self, result, encoding):
        return self.transformIterable([result], encoding)

    def transformIterable(self, result, encoding):
        if IPromises(self.request):
            return PromiseWorkerStreamIterator(
                IPromises(self.request), self.request, self.request.response)
        else:
            return None
