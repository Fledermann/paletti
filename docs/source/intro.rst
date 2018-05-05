
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

Now we can take paletti for a spin. Let's start with searching.

Searching
_________

.. code-block:: python

   >>> result = paletti.search('youtube', 'Python compiler')
   >>> result[0]
   {'type': 'video', 'url': 'https://m.youtube.com/watch?v=pzc4vYqbruk', 'title': 'How to compile your Python code', 'thumbnail': 'https://youtube.com/vi/pzc4vYqbruk/mqdefault.jpg'}
   >>> len(result)
   20
   >>> result = paletti.search('youtube', 'Python compiler', results=66)
   >>> len(result)
   66
   >>>

The results come as a list of dictionaries and, in order to be quick, contain
only basic information: type, url, title, and thumbnail. The number of search
results can be specified with the `results` keyword argument.
If `results` is 0, then paletti will not stop searching and gather all results.
This is *not* recommended for normal query searching, as many sites will give
thousands of results and the process may then take a very long time. But it is
useful for playlists, because those usually have a reasonable amount of
videos:

.. code-block:: python

   >>> playlist_url = 'https://m.youtube.com/playlist?list=PLt5AfwLFPxWLNZRKWlcRmTABh_SExiiCj'
   >>> result = paletti.search(playlist_url, results=0)
   >>> len(result)
   62
   >>>

Note that when searching in playlists, no plugin needs to be specified as this
it determined automatically.

Gathering Data
______________

If we need additional information about our search results, we use the
`metadata` function. Again, the result is a dictionary, only this time with
more information:

.. code-block:: python

   >>> url = results[0]['url']
   >>> md = paletti.metadata(url)
   >>> md.keys()
   dict_keys(['duration', 'title', 'likes', 'dislikes', 'desc', 'author', 'view_count',
   'thumbnail_small', 'thumbnail_big', 'avg_rating', 'streams', 'upload_date'])

