
Introduction
============

Paletti aims to be usable in multiple ways: as a command-line tool,
as a graphical application and as a module. Let's start off by using
paletti as a module.

Downloading Plugins
___________________

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

   >>> videos = paletti.search('youtube', 'Python compiler')
   >>> videos[0]
   {'type': 'video', 'url': 'https://m.youtube.com/watch?v=pzc4vYqbruk', 'title': 'How to compile your Python code', 'thumbnail': 'https://youtube.com/vi/pzc4vYqbruk/mqdefault.jpg'}
   >>> len(videos)
   20
   >>> videos = paletti.search('youtube', 'Python compiler', results=66)
   >>> len(videos)
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
   >>> videos = paletti.search(playlist_url, results=0)
   >>> len(videos)
   62
   >>>

Note that when searching in playlists, no plugin needs to be specified as this
it determined automatically.

Metadata
______________

If we need additional information about our search results, we use the
`metadata` function. Again, the result is a dictionary, only this time with
more information:

.. code-block:: python

   >>> url = videos[0]['url']
   >>> md = paletti.metadata(url)
   >>> md.keys()
   dict_keys(['duration', 'title', 'likes', 'dislikes', 'desc', 'author', 'view_count',
   'thumbnail_small', 'thumbnail_big', 'avg_rating', 'streams', 'upload_date'])

Downloading
___________

Downloading videos (and audio files) is straightforward.

.. code-block:: python

   >>> dl = paletti.download(url)
   >>> dl
   <Download: {'status': 'idle', 'filesize': 5562776, ... >
   >>> dl.start()
   
The download function returns a `Download` instance wich runs in a Thread.
The current status of the download can be seen by the various attributes:
`filesize` (total filesize in bytes), `progess` (in bytes), `output` 
(where the file will be written) and `status` (either idle, active or cancelled).
The running download can be stopped with `cancel()`.

The function takes various keyword arguments: `audio`, `video`, `quality` and
`container`. So, to get the opus audio stream only:

.. code-block:: python

   >>> dl = paletti.download(url, video=False, container='webm')
   >>> dl.start()
   
