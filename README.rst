experimental.futures
====================

.. image:: https://secure.travis-ci.org/datakurre/experimental.promises.png
   :target: http://travis-ci.org/datakurre/experimental.promises

(This package was renamed from *experimental.promises* to
*experimental.futures*, because the API has been forming to
follow usage of *concurrent.futures*.)

This is an experimental package for providing yet another
way to do asynchronous (non-blocking) processing on Plone.

This time we speak in terms of promises and futures:
promises are asynchronously run functions, which provide
their results as requested futures for add-on your code.

A major differences for any other alternatives is that this
does not require any additional services, but requires only
Plone running on top of a Zope instance.

A major limitation is that the asynchronously executed
code cannot access the database in any way (or you may
face unexpected consequences).


Example
-------

.. code:: python

   from Products.Five.browser import BrowserView

   from experimental import futures


   def my_async_task(*args):
       # a lot of time consuming async processing
       return u'my asynchronously computed value'


   class MyView(BrowserView):

       def __call__(self, *args):
           try:
               return futures.result('my_unique_key')
           except futures.FutureNotSubmittedError:
               futures.submit('my_unique_key', my_async_task, *args)
               return u'just a placeholder value'

or

.. code:: python

   from Products.Five.browser import BrowserView

   from experimental import futures


   def my_async_task(*args):
       # a lot of time consuming async processing
       return u'my asynchronously computed value'


   class MyView(BrowserView):

       def __call__(self, *args):
           return futures.resultOrSubmit(
               'my_unique_key', u'placeholder value', my_async_task, *args)


Explanation
-----------

This package uses approach, which kind of splits a single
request into two separate passes:

Whenever some add-on code
requires a value to be computed asynchronously, it
tries to request for a named future result at first and only then
submits a promise function to compute result for that future.

If any futures are submitted, the initial response is never
published, but instead the current transaction is aborted
and the submitted promise functions are executed in
parallel threads separate from the default Zope threads
(or even in parallel processes) and
their return values are collected
(see also the documentation of ``concurrent.futures`` in Python).

When all promise functions have been resolved, the original request
is cloned, resolved values are set as futures and a new
internal request is dispatched.

After this second pass, the add-on code can use
the now available futures, not submit more futures, and
finally, the response is published all the way to
the browser.

-----

For more background information: http://datakurre.pandala.org/2014/05/asynchronous-stream-iterators-and.html
