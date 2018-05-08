#!/usr/bin/env python

import os
import sys
import urllib.parse

import urllib3.util

PATH = os.path.dirname(__file__)
sys.path.append(PATH)
PLUGIN_FOLDER = os.path.join(PATH, 'plugins')


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
