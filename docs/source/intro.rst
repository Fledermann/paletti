
Introduction
============

Paletti aims to be usable in multiple ways: as a command-line tool,
as a graphical application and as a module. Let's start off by using
paletti as a module.

If paletti is freshly installed or downloaded, you will need to download
the plugins (i.e. crawlers for the different websites).

.. code-block:: python

   >>> import paletti
   >>> paletti.get_plugins_from_repo('https://github.com/x/y.git')
   Wrote /home/user/python/paletti/paletti/plugins/xxx.py
   Wrote /home/user/python/paletti/paletti/plugins/yyy.py
   Wrote /home/user/python/paletti/paletti/plugins/zzz.py
   >>>

If you want to update your plugins later on, you need to pass the `force=True`
parameter in order to overwrite the old files (see `main.get_plugins_from_repo()`).

Now we can take paletti for a spin:

.. code-block:: python

   >>> result = paletti.search('Python compiler', 'youtube')
   >>> result[0]
   {'url': 'youtube.com/watch?v=pzc4vYqbruk', 'title': 'How to compile your Python code',
   'thumbnail': 'https://youtube.com/vi/pzc4vYqbruk/mqdefault.jpg'}
   >>> metadata = paletti.fetch('youtube.com/watch?v=pzc4vYqbruk')
   >>> metadata.keys()
   dict_keys(['duration', 'title', 'likes', 'dislikes', 'desc', 'author', 'view_count',
   'thumbnail_small', 'thumbnail_big', 'avg_rating', 'streams', 'upload_date'])

