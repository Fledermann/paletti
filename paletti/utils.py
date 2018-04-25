#!/usr/bin/env python

import threading
import urllib3


class Downloader:
    """ Download a file from the web and start a background thread.

    :param url: the url of the file to download.
    :type url: str
    :param path: the full path where the output file is written.
    :type path: str
    :param dash_params: parameter for downloading sequential DASH streams.
                        if none is provided, download normally (default=False).
    :type dash_params: dict
    :ivar status: holds current information about the download progress for
                  external access. Keys are: "active", "filesize", "path",
                  "url" and "progress".
    :type status: dict
    """
    def __init__(self, url, path, dash_params=False):
        filesize = self._analyze(url)
        self.dash_params = dash_params
        self.filesize = filesize
        self.path = path
        self.progress = 0
        self.status = 'idle'
        self.thread = None
        self.url = url

    @staticmethod
    def _analyze(url):
        """ Get the filesize.

        :param url: the url of the file.
        :type url: str
        :returns: the filesize in bytes.
        :rtype: int
        """
        http = urllib3.PoolManager()
        response = http.request('GET', url, preload_content=False)
        filesize = int(response.headers['Content-Length'])
        return filesize

    def _fetch_file(self, callback=None):
        """ Start downloading the content of the file. While doing so,
        update the `status` dictionary so it can be accessed externally.

        :param callback: the optional callback function which is called after
                         successfully finishing the download. It will be
                         called with `self.status` as the only paramter.
        :type callback: callable
        :returns: None
        """
        self.status = 'active'
        http = urllib3.PoolManager()
        response = http.request('GET', self.url, preload_content=False)
        for chunk in response.stream(1024):
            if self.status != 'active':
                break
            with open(self.path, 'ab') as f:
                f.write(chunk)
            self.progress += 1024
        self.status = 'finished'
        if callback:
            callback(self)
        return

    def _fetch_file_dash(self, callback=None):
        """ Start downloading the content of the DASH file. While doing so,
        update the `status` dictionary so it can be accessed externally.
        This should always be used instead of `_fetch_file` if the resource
        is a DASH stream, because many content providers throttle a regular,
        direct download after a few MiB.

        :param callback: the optional callback function which is called after
                         successfully finishing the download. It will be
                         called with `self.status` as the only paramter.
        :type callback: callable
        :returns: None
        """
        self.status = 'active'
        http = urllib3.PoolManager()
        dash_chunk_size = 10_485_760
        chunk_start = 0
        while self.progress < self.filesize:
            chunk_end = chunk_start + dash_chunk_size - 1
            dash_url = f'{self.url}&{self.dash_params["key"]}={chunk_start}' \
                       f'{self.dash_params["format"]}{chunk_end}'
            response = http.request('GET', dash_url, preload_content=False)
            with open(self.path, 'ab') as f:
                for chunk in response.stream(1024):
                    if not self.status != 'active':
                        return
                    f.write(chunk)
                    self.progress += 1024
            chunk_start = chunk_end + 1
        self.status = 'finished'
        if callback:
            callback(self)
        return

    def cancel(self):
        """ Cancel the download immediately.

        :returns: None
        """
        self.status = 'cancelled'
        self.thread.join()
        return None

    def start(self):
        """ Start the file download as a background thread.

        :returns: None
        """
        if self.dash_params:
            self.thread = threading.Thread(target=self._fetch_file_dash)
            self.thread.start()
        else:
            self.thread = threading.Thread(target=self._fetch_file)
            self.thread.start()
        return None
