
Introduction
============

To use the api as a module:

.. code-block:: python

   >>> import paletti
   >>> paletti.fetch_plugins_from_repo('https://github.com/x/y.git')
   >>> result = paletti.search('Python compiler', 'youtube')
   >>> result[0]
   {'url': 'youtube.com/watch?v=pzc4vYqbruk', 'title': 'How to compile your Python code',
   'thumbnail': 'https://youtube.com/vi/pzc4vYqbruk/mqdefault.jpg'}
   >>> metadata = paletti.fetch('youtube.com/watch?v=pzc4vYqbruk')
   >>> metadata.keys()
   dict_keys(['duration', 'title', 'likes', 'dislikes', 'desc', 'author', 'view_count',
   'thumbnail_small', 'thumbnail_big', 'avg_rating', 'streams', 'upload_date'])

