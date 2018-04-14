
Introduction
============

To use the api as a module:

.. code-block:: python

   >>> import paletti
   >>> my_api = paletti.SiteAPI('$streaming-site')
   >>> result = my_api.search('Python compiler')
   >>> result[0]
   {'url': '$streaming-site.com/watch?v=pzc4vYqbruk', 'title': 'How to compile your Python code',
   'thumbnail': 'https://$streaming-site.com/vi/pzc4vYqbruk/mqdefault.jpg'}
   >>> video_url = result[0]['url']
   >>> data = my_api.get_information(video_url)
   >>> data.keys()
   dict_keys(['duration', 'title', 'likes', 'dislikes', 'desc', 'author', 'view_count',
   'thumbnail_small', 'thumbnail_big', 'avg_rating', 'streams', 'upload_date'])
   >>> dl = my_api.download(video_url, '/tmp/testfile')
   >>> dl['progress']
   12232340
   >>> dl['progress']
   18898311
   >>> dl['filesize']
   82370900

