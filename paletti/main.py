#!/usr/bin/env python

import os
import urllib.parse
import urllib3.util
import sys

import paletti.web_api

PATH = os.path.dirname(__file__)
sys.path.append(PATH)
PLUGIN_FOLDER = os.path.join(PATH, 'plugins')

plugins = {}


def _get_api(name):
    """ Find the right `SiteAPI` instance based on the name.

    :param name: the name of the plugin.
    :type name: str
    :return: the api instance.
    :rtype: `SiteAPI`
    """
    global plugins
    if name in plugins:
        return plugins[name]
    try:
        plugin = paletti.web_api.SiteAPI(name)
        plugins[name] = plugin
        return plugin
    except ModuleNotFoundError:
        print('Error: host not recognized (there is no plugin for that).')
        return None


def fetch(url):
    """ Retrieve all metadata for the stream.

    :param url: the url.
    :type url: str
    :return:
    """
    parsed_url = urllib3.util.parse_url(url)
    host = parsed_url.host
    plugin = paletti.web_api.get_plugin_for_host(host)
    api = _get_api(plugin)
    if api:
        return api.get_information(url)


def get_plugins_from_repo(url, branch='master', force=False):
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


def search(query, plugin):
    """ Perform a search and return the results.

    :param query: the search query.
    :type query: str
    :param plugin: the name of the plugin to use for the search.
    :type plugin: str
    :return: the search result.
    :rtype: list(dict)
    """
    api = _get_api(plugin)
    if api:
        return api.search(query)
