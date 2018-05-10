#!/usr/bin/env python

""" The Download class.
"""

import sys
import threading
import urllib3


class Download:
    """ A download class specifically for downloading videos.

    :param list(dict) streams: a list of length two, containing the video and
                               audio stream dicts. If one of these is not
                               provided, the stream will be skipped.
    :param str output: the local file path where the fill will be saved.
    """
    def __init__(self, streams, output, postprocessing):
        self.output = output
        self.postprocessing = postprocessing
        self.progress = 0
        self.status = 'idle'
        self.streams = streams
        self.threads = []
        self.filesize = self._analyze()

    def __repr__(self):
        output = self.__dict__.copy()
        del(output['streams'])
        del(output['threads'])
        return f'<Download: {output}>'

    def _analyze(self):
        """ Get the total filesize of all streams.

        :returns: the filesize in bytes.
        :rtype: int
        """
        http = urllib3.PoolManager()
        filesize = 0
        for stream in self.streams:
            if stream:
                response = http.request('GET', stream['url'], preload_content=False)
                filesize += int(response.headers['Content-Length'])
        return filesize

    def cancel(self):
        self.status = 'cancelled'

    def download_file(self, stream):
        if not stream:
            return None
        http = urllib3.PoolManager()
        dash_chunk_size = 10_485_760
        dl_chunk_size = 131_072
        chunk_start = 0
        dash_params = {'key': 'range', 'format': '-'}
        while self.progress < self.filesize:
            chunk_end = chunk_start + dash_chunk_size - 1
            dash_url = f'{stream["url"]}&{dash_params["key"]}={chunk_start}' \
                       f'{dash_params["format"]}{chunk_end}'
            response = http.request('GET', dash_url, preload_content=False)
            filepath = f'{self.output}.{stream["container"]}.{stream["type"]}.{stream["codec"]}'
            with open(filepath, 'ab') as f:
                for chunk in response.stream(dl_chunk_size):
                    if self.status != 'active':
                        return
                    f.write(chunk)
                    # Check whether the chunk was smaller than our chunk size,
                    # to get the correct progress for the last iteration.
                    if sys.getsizeof(chunk_start) == dl_chunk_size:
                        self.progress += dl_chunk_size
                    else:
                        self.progress += sys.getsizeof(chunk)
            chunk_start = chunk_end + 1
        self.status = 'finished'
        self.trigger_pp()
        return

    def start(self):
        self.status = 'active'
        for stream in self.streams:
            t = threading.Thread(target=self.download_file, args=[stream])
            self.threads.append(t)
            t.start()

    def trigger_pp(self):
        if not ([t.isAlive() for t in self.threads].count(True) - 1):
            self.postprocessing(self.output)
