#!/usr/bin/env python

import pathlib
import os
import sys
import urllib.parse

import urllib3.util

PATH = os.path.dirname(__file__)
sys.path.append(PATH)
PLUGIN_FOLDER = os.path.join(PATH, 'plugins')


def get_plugins_from_repo(url, branch='master'):
    """ Find and download all the plugins from the github repository.

    :param url: the .git url.
    :type url: str
    :param branch: the branch, default: "master"
    :type branch: str
    :return: the written files.
    :rtype: list(str)
    """
    local_files_written = []
    url = url.replace('.git', '/')
    host = 'raw.githubusercontent.com'
    parsed_url = urllib3.util.parse_url(url)
    branch_root = urllib.parse.urljoin(parsed_url.path, branch + '/')
    plugin_path = urllib.parse.urljoin(branch_root, 'plugins/')
    plugin_index = urllib.parse.urljoin(plugin_path, 'index.txt')
    http = urllib3.HTTPSConnectionPool(host)
    response = http.request('GET', plugin_index)
    for name in response.data.split():
        name = name.decode('utf-8')
        folder = pathlib.Path(PLUGIN_FOLDER) / name
        module = folder / f'{name}.py'
        test_unit = folder / 'test_unittest.py'
        test_func = folder / 'test_functional.py'
        if not os.path.exists(folder):
            os.mkdir(folder)
        module_url = urllib.parse.urljoin(plugin_path, f'{name}/{name}.py')
        test_unit_url = urllib.parse.urljoin(plugin_path, f'{name}/test_unittest.py')
        test_func_url = urllib.parse.urljoin(plugin_path, f'{name}/test_functional.py')

        files = zip([module, test_unit, test_func],
                    [module_url, test_unit_url, test_func_url])

        for local, remote in files:
            r = http.request('GET', remote)
            with open(local, 'wb') as f:
                f.write(r.data)
            local_files_written.append(local)
    return local_files_written
