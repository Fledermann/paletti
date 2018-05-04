#!/usr/bin/env python

""" Provide an easy and intuitive way to fetch data from streaming
websites. """

import functools
import importlib
import os
import pkgutil
import re
import sys
import urllib3
import urllib3.util

PATH = os.path.dirname(__file__)
sys.path.append(PATH)
PLUGIN_FOLDER = os.path.join(PATH, 'plugins')


def cache(func):
    """ A decorator function which caches the results of requests.

    :param callable func: the decorated function.
    :return: dict of media data.
    :rtype: dict
    """
    cache_list = []

    @functools.wraps(func)
    def wrapper(*args):
        for item in cache_list:
            if item['url'] == args[1]:
                return item
        media_item = func(*args)
        cache_list.append(media_item)
        return media_item
    return wrapper


def module(func):
    """ A decorator function which provides the necessary plugin modules.

    :param callable func: the decorated function.
    :return: the module
    """
    plugin_list = []
    packages = pkgutil.walk_packages([PLUGIN_FOLDER])
    for plugin in packages:
        folder = os.path.normpath(PLUGIN_FOLDER).split(os.sep)[-1]
        full_package_name = f'{folder}.{plugin.name}'
        mod = importlib.import_module(full_package_name)
        if not plugin.name.startswith('_'):
            plugin_data = {'name': plugin.name,
                           'module': mod,
                           'hosts': mod.HOSTS,
                           'type': mod.STREAM_TYPE}
            plugin_list.append(plugin_data)

    @functools.wraps(func)
    def wrapper(plugin_name_or_url, *args, **kwargs):
        host = urllib3.util.parse_url(plugin_name_or_url).host
        for item in plugin_list:
            if host == item['name'] or host in item['hosts']:
                mod = item['module']
                break
        else:
                raise ModuleNotFoundError
        if not args:
            args = (plugin_name_or_url, )
        return func(mod, *args, **kwargs)
    return wrapper


def _filter_stream(*args):
    """ Look up values in a dict. Return true if all values were found.

    :param tuple(str) args: an arbitrary number of values. Last argument is the
                            dict.
    :return: True if all values were present, False otherwise.
    :rtype: bool
    """
    stream = args[-1]
    for param in args[:-1]:
        if param not in stream.values():
            return False
    return True


def _make_filename(title):
    """ Create a descriptive and safe filename from the title.

    :param str title: the title of the media object.
    :return: the filename.
    :rtype: str
    """
    return re.sub('[^a-zA-z0-9]+', '_', title)


@module
def channel(plugin, url):
    raise NotImplementedError


@module
@cache
def metadata(plugin, media_url):
    """ Fetch information for the specified media url and return a
    dict.

    :param str media_url: the url of the media page.
    :returns: all the information / metadata found.
    :rtype: dict
    """
    return plugin.get_metadata(media_url)


@module
def playlist(plugin, media_url, **kwargs):
    return plugin.playlist(media_url, **kwargs)


@module
def search(plugin, query_or_url, **kwargs):
    """ Perform a search and return the result. The result will be a list
    of dicts, each dict containing some basic data for the video like
    title, duration etc. The `query_or_url` parameter can either be a
    regular search time, in which case the plugin must be specified, or
    ot may be the url of a channel or playlist (where the plugin in
    determined automatically).

    :param str plugin: the plugin.
    :param str query_or_url: the search query.
    :keyword int results: the number of search results (default value depends on
                          the plugin).
    :returns: the search result.
    :rtype: list
    """
    methods = {'search_query': plugin.search,
               'playlist': playlist,
               'channel': channel,
               'user': user}
    request = plugin.parse_userinput(query_or_url)
    return methods[request](query_or_url, **kwargs)


def stream_urls(media_url, quality='1080p', container='webm'):
    """ Given a media url, return the absolute stream files.

    :param str media_url: the media url.
    :param str quality: the stream quality (concerns only video files).
                          Default: '1080p'.
    :param str container: the container format. Usually either mp4 or webm.
                            Default: 'webm'.
    :return: the video url and the audio url.
    :rtype: tuple(str, str)
    """
    item = metadata(media_url)
    streams = item['streams']
    video_url, audio_url = '', ''
    video_streams = list(filter(functools.partial(_filter_stream, 'video', quality, container), streams))
    if video_streams:
        video_url = video_streams[0]['url']
    audio_streams = list(filter(functools.partial(_filter_stream, 'audio', container), streams))
    if audio_streams:
        best = audio_streams[0]
        for stream in audio_streams:
            if int(stream['quality']) > int(best['quality']):
                best = stream
        audio_url = best['url']
    return audio_url, video_url


@module
def user(plugin, url):
    raise NotImplementedError
