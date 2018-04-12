
Introduction
============

To use the api as a module:

.. code-block:: python

   >>> import paletti
   >>> my_api = paletti.SiteAPI('$streaming-site')
   >>> result = my_api.search('Python compiler')
   >>> result
   {'url': '$streaming-site.com/watch?v=pzc4vYqbruk', 'title': 'How to compile your Python code',
   'thumbnail': 'https://$streaming-site.com/vi/pzc4vYqbruk/mqdefault.jpg'}
   >>> dl = my_api.download(result['url'], '/tmp/testfile')
   >>> dl['progress']
   12232340
   >>> dl['progress']
   18898311
   >>> dl['filesize']
   82370900

