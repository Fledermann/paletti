#!/usr/bin/env python

""" Provide an easy and intuitive way to fetch data from streaming
websites. """

import concurrent.futures
import importlib
import os
import pkgutil
import re
import sys

PATH = os.path.dirname(__file__)
sys.path.append(PATH)
PLUGIN_FOLDER = os.path.join(PATH, 'plugins')
DEFAULT_QUALITY = '720p'
DEFAULT_CONTAINER = 'mp4'


class SiteAPI:
    """ Handle the user-friendly communication between the user and the plugin
    aka crawler.
    """

    def __init__(self, plugin):
        """ Set the plugin.

        :param plugin: the plugin to use.
        :type plugin: str
        """
        self.cache = []
        modules = load_plugins(PLUGIN_FOLDER)
        try:
            self.plugin = modules[plugin]
        except KeyError:
            raise ModuleNotFoundError(f'Plugin {plugin} not found.')

    def _get_from_cache(self, media_url):
        """ Return a cached item, if available. If nothing is found,
        return None.

        :param media_url: the url of the media page.
        :type media_url: str
        :return: dict or None
        """
        for item in self.cache:
            if item['url'] == media_url:
                return item
        return None

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

    def download(self, media_url, folder):
        """ Download files from media_url. Quality, resolution etc is chosen
        automatically according to the configuration. For downloading
        a specific file directly, use `download_file`

        :param media_url: the url of the media page.
        :type media_url: str
        :param folder: the local folder for the downloaded file
        :type folder: str
        :returns: two `Downloader` objects for the audio and the video stream.
        :rtype: tuple(`Downloader`, `Downloader`)
        """
        media_data = self.get_information(media_url)[0]
        audio_file, video_file = choose_stream(media_data)
        filename = re.sub('[^a-zA-z0-9]+', '_', media_data['title'])
        path = os.path.join(folder, filename)
        audio_dl = self.plugin.download(audio_file, f'{path}.aac')
        video_dl = self.plugin.download(video_file, f'{path}.mp4')
        return audio_dl, video_dl

    def download_file(self, url):
        """ Download a file directly.

        :param url: the url of the file.
        :type url: str
        :returns: a `Downloader` object.
        """
        return None

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


def choose_stream(media_data):
    """ Choose the correct file urls according to the settings and available
    streams.

    :param media_data: the metadata of the media.
    :type media_data: dict
    :returns: the audio and video field urls
    :rtype: tuple(str, str)
    """
    for stream in media_data['streams']:
        if stream['type'] == 'video':
            if stream['quality_label'] == DEFAULT_QUALITY and stream['container'] == DEFAULT_CONTAINER:
                video_file = stream['url']
        else:
            if stream['container'] == DEFAULT_CONTAINER:
                audio_file = stream['url']
    return audio_file, video_file


def load_plugins(directory):
    """ Dynamically load all modules from a given folder.

    :param directory: the plugin folder.
    :type directory: str
    :returns: a dict of {name: module} pairs.
    :rtype: dict
    """
    available_plugins = {}
    packages = pkgutil.walk_packages([directory])
    for plugin in packages:
        folder = os.path.normpath(directory).split(os.sep)[-1]
        full_package_name = f'{folder}.{plugin.name}'
        module = importlib.import_module(full_package_name)
        available_plugins[plugin.name] = module
    return available_plugins
