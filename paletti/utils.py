#!/usr/bin/env python

import os
import pathlib
import re
import subprocess


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
        try:
            name, container, type_ = item.split('.')
        except ValueError:
            continue
        if name == filename:
            out_file = folder / f'{filename}.{container}'
            if type_ == 'audio':
                audio = folder / item
            if type_ == 'video':
                video = folder / item
    if audio and video:
        subprocess.call(f'ffmpeg -i {audio} -i {video} -c:a copy -c:v copy {out_file}',
                        shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        os.remove(audio)
        os.remove(video)
    elif audio:
        os.rename(audio, out_file)
    elif video:
        os.rename(video, out_file)
