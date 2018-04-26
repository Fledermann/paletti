#!/usr/bin/env python

""" Provide an easy and intuitive way to fetch data from streaming
websites. """

import importlib
import os
import pkgutil
import re
import sys
import urllib3
import urllib3.util

from paletti import utils

urllib3.disable_warnings()

PATH = os.path.dirname(__file__)
sys.path.append(PATH)
PLUGIN_FOLDER = os.path.join(PATH, 'plugins')
DEFAULT_QUALITY = '720p'
DEFAULT_CONTAINER = 'mp4'


class SiteAPI:
    """ Handle the user-friendly communication between the user and the plugin
    aka crawler.
    """

    def __init__(self, plugin_name):
        """ Set the plugin.

        :param plugin_name: the plugin to use.
        :type plugin_name: str
        """
        self.cache = []
        self.name = plugin_name
        plugins_all = find_modules(PLUGIN_FOLDER)
        try:
            package_name = plugins_all[plugin_name]
        except KeyError:
            raise ModuleNotFoundError(f'Plugin {plugin_name} not found.')
        self.plugin = importlib.import_module(package_name)

    def _get_from_cache(self, media_url):
        """ Return a cached item, if available. If nothing is found,
        return None.

        :param media_url: the url of the media page.
        :type media_url: str
        :return: dict or None
        """
        for item in self.cache:
            print(item)
            if item['url'] == media_url:
                return item
        return None

    def _make_filename(self, title):
        """ Create a descriptive and safe filename from the title.

        :param title: the title of the media object.
        :type title: str
        :return: the filename.
        :rtype: str
        """
        return re.sub('[^a-zA-z0-9]+', '_', title)

    def get_information(self, media_url):
        """ Fetch information for the specified media url and return a
        dict.

        :param media_url: the url of the media page.
        :type media_url: str
        :returns: all the information / metadata found.
        :rtype: dict
        """

        media_item = self._get_from_cache(media_url)
        if not media_item:
            media_item = self.plugin.get_metadata(media_url)
            self.cache.append(media_item)
        return media_item

    def get_thumbnail(self, media_url, folder, size='small'):
        """

        :param media_url: the url of the media page.
        :type media_url: str
        :param folder: the local folder for the downloaded file
        :type folder: str
        :param size: the size / resolution of the thumbnail
                        (default: 'small'). Either 'small' or 'big'.
        :type size: str
        :return: the local path of the downloaded thumbnail.
        :rtype: str
        """
        media_data = self.get_information(media_url)
        thumb_url = media_data[f'thumbnail_{size}']
        dl = self.download_file(thumb_url, folder)
        dl.start()
        while not dl.status['finished']:
            pass
        return dl.status['path']

    def download(self, media_url, folder, **kwargs):
        """ Download files from media_url. Quality, resolution etc is chosen
        automatically according to the configuration. For downloading
        a specific file directly, use `download_file`

        :param media_url: the url of the media page.
        :type media_url: str
        :param folder: the local folder for the downloaded file
        :type folder: str
        :keyword callback: a callback function which is called when the process
                           finished.
        :type callback: callable
        :returns: One or two `Downloader` objects, depending on the site and
                  the media type.
        :rtype: list
        """
        media_data = self.get_information(media_url)
        stream_type = self.plugin.STREAM_TYPE
        downloads = []
        if 'video' in stream_type:
            video_file = choose_stream(media_data, 'video')
            downloads.append(video_file)
        if 'seperate' in stream_type or 'audio' in stream_type:
            audio_file = choose_stream(media_data, 'audio')
            downloads.append(audio_file)
        filename = self._make_filename(media_data['title'])
        path = os.path.join(folder, filename)
        output = []
        for i, d in enumerate(downloads):
            dl = self.plugin.download(d, f'{path}.{i}', **kwargs)
            output.append(dl)
        return output

    def download_file(self, url, folder, **kwargs):
        """ Download a file directly.

        :param url: the url of the file.
        :type url: str
        :param folder: the folder where the file will be downloaded.
        :type folder: str
        :param callback: the optional callback funtion which is called after
                         successfully finishing the download. It will be
                         called with `self.status` as the only paramter.
        :type callback: callable
        :returns: a `Downloader` object.
        """
        parsed_url = urllib3.util.parse_url(url)
        filename = parsed_url.path.split('/')[-1]
        path = os.path.join(folder, filename)
        dl = utils.Downloader(url, path, **kwargs)
        return dl

    def search(self, query):
        """ Perform a search and return the result. The result will be a list
        of dicts, each dict containing some basic data for the stream like
        title, duration etc.

        :param query: the search query.
        :type query: str
        :returns: the search result.
        :rtype: list
        """
        return self.plugin.search(query)


def choose_stream(media_data, type_):
    """ Choose the correct file url according to the settings and available
    streams.

    :param media_data: the metadata of the media.
    :type media_data: dict
    :param type_: the type of stream to choose (video or audio).
    :type type_: str
    :returns: the stream url.
    :rtype: str
    """
    streams = [s for s in media_data['streams'] if
               s['type'] == type_ and s['container'] == DEFAULT_CONTAINER]
    if type_ == 'audio':
        return streams[0]['url']
    for s in streams:
        if s['quality'] == DEFAULT_QUALITY:
            return s['url']


def find_modules(directory):
    """ Find all modules from a given folder and return their names
    and full paths. Ignore files starting with an underscore.

    :param directory: the plugin folder.
    :type directory: str
    :returns: a dict of {name: package path} pairs.
    :rtype: dict
    """
    available_plugins = {}
    packages = pkgutil.walk_packages([directory])
    for plugin in packages:
        folder = os.path.normpath(directory).split(os.sep)[-1]
        full_package_name = f'{folder}.{plugin.name}'
        if not plugin.name.startswith('_'):
            available_plugins[plugin.name] = full_package_name
    return available_plugins


def get_plugin_for_host(host):
    """ Find the plugin which handles 'host' and return it.

    :param host: the host
    :type host: str
    :return: the module
    """
    # FIXME: this loads all modules only to discard them.
    all_plugins = find_modules(PLUGIN_FOLDER)
    for name, package in all_plugins.items():
        module = importlib.import_module(package)
        if host in module.HOSTS:
            return name


def show_plugins():
    """ Return all available plugins.

    :returns: the plugins.
    :rtype: list
    """
    plugins = find_modules(PLUGIN_FOLDER)
    return list(plugins.keys())
