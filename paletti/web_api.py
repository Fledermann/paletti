#!/usr/bin/env python

""" Provide an easy and intuitive way to fetch data from streaming
websites. """

import importlib
import os
import pkgutil
import re
import sys
import urllib.parse
import urllib3

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

    def get_thumbnail(self, media_url, size='small'):
        """

        :param media_url: the url of the media page.
        :type media_url: str
        :param size: the size / resolution of the thumbnail
                        (default: 'small'). Either 'small' or 'big'.
        :type size: str
        :return: the local path of the downloaded thumbnail.
        :rtype: str
        """
        media_data = self.get_information(media_url)
        thumb_url = media_data[f'thumbnail_{size}']
        local_path = self.download_file(thumb_url)
        return local_path


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
        media_data = self.get_information(media_url)
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


def fetch_plugins_from_repo(url, branch='master', force=False):
    """ Find and download all the plugins from the github repository.

    :param url: the .git url.
    :type url: str
    :param branch: the branch, default: "master"
    :type branch: str
    :param force: if true, overwrite local files.
    :type force: bool
    :return: None
    """
    url = url.replace('.git', '/')
    host = 'raw.githubusercontent.com'
    parsed_url = urllib3.util.parse_url(url)
    branch_root = urllib.parse.urljoin(parsed_url.path, branch + '/')
    plugin_path = urllib.parse.urljoin(branch_root, 'plugins/')
    plugin_index = urllib.parse.urljoin(plugin_path, '_index.txt')
    http = urllib3.HTTPSConnectionPool(host)
    response = http.request('GET', plugin_index)
    for name in response.data.split():
        filename = name.decode('utf-8') + '.py'
        file_url = urllib.parse.urljoin(plugin_path, filename)
        file_local = os.path.join(PLUGIN_FOLDER, filename)
        file_exists = os.path.isfile(file_local)
        if not file_exists or force:
            r = http.request('GET', file_url)
            with open(file_local, 'wb') as f:
                f.write(r.data)
            print(f'Wrote {file_local}')
        else:
            print(f'File {file_local} already exists, not overwriting.')


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


def show_plugins():
    """ Return all available plugins.

    :returns: the plugins.
    :rtype: list
    """
    plugins = find_modules(PLUGIN_FOLDER)
    return list(plugins.keys())
