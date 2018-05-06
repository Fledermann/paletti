#!/usr/bin/env python

""" Provide an easy and intuitive way to fetch data from streaming
websites. """

import functools
import importlib
import os
import pkgutil
import sys
import urllib3
import urllib3.util

import utils
from download import Download

PATH = os.path.dirname(__file__)
sys.path.append(PATH)
PLUGIN_FOLDER = os.path.join(PATH, 'plugins')


def cache(func):
    """ A decorator function which caches the results of requests.

    :param callable func: the decorated function.
    :return: the wrapper.
    :rtype: callable
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
    :return: the wrapper.
    :rtype: callable
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


def _filter_stream(streams, type_, quality, container):
    """ Look up the properties of the video streams and filter by keyword
    arguments. A certain level of interpretation is used, if the exact stream
    is not found. It will only return None if the container format
    is not provided.

    :param tuple(str) args: an arbitrary number of values. Last argument is the
                            dict.
    :return: True if all values were present, False otherwise.
    :rtype: bool
    """
    streams = sorted(streams, key=lambda k: k['quality_int'], reverse=True)
    result = [s for s in streams if s['type'] == type_]
    if not result:
        if type_ == 'audio':
            return None
        result = [s for s in streams if s['type'] == 'audio+video']
    result_ = [s for s in result if s['container'] == container]
    if not result_:
        print(f'Container {container} not available, choosing another one.')
        result_ = result
    best_available = result_[0]['quality']
    if quality == 'best':
        result__ = [s for s in result_ if s['quality'] == best_available]
    else:
        result__ = [s for s in result_ if s['quality'] == quality]
        if not result__:
            result__ = [s for s in result_ if s['quality'] == best_available]
    return result__[0]


@module
def channel(plugin, url):
    raise NotImplementedError


def download(media_url, audio=True, video=True, **kwargs):
    streams_dict = streams(media_url, **kwargs)
    md = metadata(media_url)
    fn = utils.make_filename(md['title'])
    if not video:
        if not streams_dict[0]:
            print('Sorry, audio only is not available for this stream.')
            return None
        streams_dict[1] = None
    if not audio:
        streams_dict[0] = None
    d = Download(streams_dict, f'/tmp/{fn}', utils.merge_files)
    return d


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


def streams(media_url, quality='best', container='webm'):
    """ Given a media url, return the stream dicts.

    :param str media_url: the media url.
    :param str quality: the stream quality (concerns only video files).
                          Default: '1080p'.
    :param str container: the container format. Usually either mp4 or webm.
                            Default: 'webm'.
    :return: the audio and video dicts.
    :rtype: tuple(dict, dict)
    """
    item = metadata(media_url)
    stream_dicts = item['streams']
    video_stream = _filter_stream(stream_dicts, 'video', quality, container)
    audio_stream = _filter_stream(stream_dicts, 'audio', quality, container)
    return [audio_stream, video_stream]


@module
def user(plugin, url):
    raise NotImplementedError
