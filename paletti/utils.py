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
        self.status = {'active': True, 'filesize': filesize, 'path': path,
                       'url': url}
        self.thread = None

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

    def _fetch_file(self):
        """ Start downloading the content of the file. While doing so,
        update the `status` dictionary so it can be accessed externally.

        :returns: None
        """
        self.status['progress'] = 0
        path = self.status['path']
        http = urllib3.PoolManager()
        response = http.request('GET', self.status['url'], preload_content=False)
        for chunk in response.stream(1024):
            if not self.status['active']:
                break
            with open(path, 'ab') as f:
                f.write(chunk)
            self.status['progress'] += 1024
        return

    def _fetch_file_dash(self):
        """ Start downloading the content of the DASH file. While doing so,
        update the `status` dictionary so it can be accessed externally.
        This should always be used instead of `_fetch_file` if the resource
        is a DASH stream, because many content providers throttle a regular,
        direct download after a few MiB.

        :returns: None
        """
        self.status['progress'] = 0
        url = self.status['url']
        path = self.status['path']
        dp = self.dash_params
        http = urllib3.PoolManager()
        dash_chunk_size = 1024 * 1024 * 10
        chunk_start = 0
        while self.status['progress'] < self.status['filesize']:
            chunk_end = chunk_start + dash_chunk_size - 1
            dash_url = f'{url}&{dp["key"]}={chunk_start}{dp["format"]}{chunk_end}'
            response = http.request('GET', dash_url, preload_content=False)
            with open(path, 'ab') as f:
                for chunk in response.stream(1024):
                    if not self.status['active']:
                        return
                    f.write(chunk)
                    self.status['progress'] += 1024
            chunk_start = chunk_end + 1
        return

    def cancel(self):
        """ Cancel the download immediately.

        :returns: None
        """
        self.status['active'] = False
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
