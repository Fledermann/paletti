Code Examples
=============

Download all videos in best quality from playlist:

.. code-block:: python

   import paletti
   
   videos = paletti.search(playlist_url)
   for i, vid in enumerate(videos):
       print(f'Downloading {i+1} of {len(videos)}.')
       dl = paletti.download(vid['url'])
       dl.start()
       while dl.status != 'finished':
           pass

