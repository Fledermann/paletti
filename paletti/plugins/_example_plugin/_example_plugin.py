#!/usr/bin/env python

from urllib3.util import parse_url


def parse_userinput(url_or_query):
    """ Parse the userinput to determine what kind of method to use.
    The user may have used a video url, a playlist url, a search query etc.

    :param str url_or_query: the url.
    :return: the kind of request to be used. It is either "channel",
             "playlist", "search_query" or "user".
    :rtype: str
    """
    parsed = parse_url(url_or_query)
    if not parsed.scheme:
        return 'search_query'
    if parsed.path == '/playlist':
        return 'playlist'
    if parsed.path.startswith('/channel/'):
        return 'channel'
    if parsed.path.startswith('/user/'):
        return 'user'
