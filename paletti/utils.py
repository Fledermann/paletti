#!/usr/bin/env python

import importlib
import os
import pathlib
import re
import subprocess
import sys

PATH = os.path.dirname(__file__)
sys.path.append(PATH)
PLUGIN_FOLDER = os.path.join(PATH, 'plugins')


def find_modules(type_):
    plugin_list = []
    plugin_folder = pathlib.Path(PLUGIN_FOLDER)
    directories = os.listdir(plugin_folder)
    for d in directories:
        if str(d).startswith('_'):
            continue
        subfolder = plugin_folder / d
        sys.path.append(str(subfolder))
        files = [f for f in os.listdir(subfolder) if not f.startswith('_')]
        for plugin_file in files:
            if type_ == 'plugins':
                if plugin_file.startswith('test_'):
                    continue
                name = plugin_file.split('.')[0]
                mod = importlib.import_module(name)
                plugin_data = {'name': name,
                               'module': mod,
                               'hosts': mod.HOSTS,
                               'type': mod.STREAM_TYPE}
                plugin_list.append(plugin_data)
            if type_ == 'tests':
                if not plugin_file.startswith('test_'):
                    continue
                name = plugin_file.split('.')[0]
                mod = importlib.import_module(name)
                plugin_data = {'name': name,
                               'plugin': subfolder.parts[-1],
                               'type': name.replace('test_', ''),
                               'module': mod}
                plugin_list.append(plugin_data)
    return plugin_list


def make_filename(title):
    """ Create a descriptive and safe filename from the title.

    :param str title: the title of the media object.
    :return: the filename.
    :rtype: str
    """
    return re.sub('[^a-zA-z0-9]+', '_', title)


def merge_files(path):
    """ Merge video and audio files after downloading.

    :param str path: the base path, minus file extensions.
    :return: None
    """
    p = pathlib.Path(path)
    folder = p.parent
    filename = p.parts[-1]
    audio, video = '', ''
    for item in os.listdir(folder):
        properties = item.split('.')
        try:
            if properties[2] in ['audio', 'video'] and properties[0] == filename:
                name, container, type_, codec = properties
            else:
                continue
        except IndexError:
            continue
        out_file = folder / f'{filename}.{container}'
        if type_ == 'audio':
            audio = folder / item
        if type_ == 'video' or type_ == 'audio+video':
            video = folder / item
    if audio and video:
        subprocess.call(f'ffmpeg -i {audio} -i {video} -c:a copy -c:v copy {out_file}',
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(audio)
        os.remove(video)
    elif audio:
        out_file = folder / f'{filename}.{codec}'
        os.rename(audio, out_file)
    elif video:
        out_file = folder / f'{filename}.{codec}'
        os.rename(video, out_file)
    return str(out_file)