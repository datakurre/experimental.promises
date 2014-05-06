experimental.promises
=====================

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

   from experimental.promises import (
       get,
       submit
   )

  
   def my_async_task():
       # a lot of async processing
       return u'my asynchronously computed value'


   class MyView(BrowserView):

       def __call__(self):
           try:
               return get('my_unique_key')
           except KeyError:
               return submit('my_unique_key', my_async_task) and u''

or

.. code:: python

   from Products.Five.browser import BrowserView

   from experimental.promises import getOrSubmit


   def my_async_task():
       # a lot of async processing
       return u'my asynchronously computed value'


   class MyView(BrowserView):

       def __call__(self):
           return getOrSubmit('my_unique_key, my_async_task) or u''


Explanation
-----------

This package uses approach, which kind of splits a single
request into two separate passes:

Whenever some add-on code
requires a value to be computed asynchronously, it
tries to look it from the futures at first and only then
defines a promise to compute that value.

If any promises are defined, the initial response is never
published, but instead the promise functions are executed in
parallel threads separate from the default Zope threads and
their return values are collected
(see also the documentation of ``concurrent.futures`` in Python).

When all promises have been resolved, the original request
is cloned, resolved values are set as futures and a new
internal request is dispatched.

After this second pass, the add-on code can use
the now available futures, not set any more promises, and
finally, the response is published all the way to
the browser.

-----

For more background information: http://datakurre.pandala.org/2014/05/asynchronous-stream-iterators-and.html
