#!/usr/bin/python

""" This module is intended for functional testing, since many of the complex
tasks, like crawling and streaming, cannot be unit-tested reasonably.

"""

import inspect
import pathlib
import random
import sys
import threading

from functional.cases import test_cases

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(root))

import paletti
    

def threaded(func):
    """ A decorator function to call the decorated function with each element
    from args[0] (a list of test arguments) as seperate threads.

    :param callable func: the decorated function.
    :return: callable wrapper.
    """
    threads = []

    def wrapper(*args):
        for arg in args[0]:
            t = threading.Thread(target=func, args=[arg])
            threads.append(t)
            t.start()
        [x.join() for x in threads]
        print(f'Ran {func.__name__} on {len(args[0])} items.')
    return wrapper


def report_error(reason, **kwargs):
    """ Error reporting. Prints out the caller functions' name, the reason
    for the error and an arbitraty number of additional information used
    for debugging.

    :param str reason: the reason for the error.
    :param kwargs: any number of kwargs, which will be printed out.
    :return: None
    """
    func_name = inspect.stack()[1][3]
    print('#' * 40)
    print(f'Error in {func_name}: {reason}.')
    for key, value in kwargs.items():
        print(f'{key}: {value}')
    print('#' * 40)


@threaded
def test_download(url):
    d = paletti.download(url)
    d.start()


@threaded
def test_metadata(url):
    _ = paletti.metadata(url)


@threaded
def test_playlist(url):
    n = random.randint(10, 40)
    r = paletti.search(url, results=n)
    if len(r) != n:
        report_error(f'Wrong number of results. Expected {n}, got {len(r)}',
                     url=url, result=r)


@threaded
def test_search(query):
    _ = paletti.search('youtube', query)


if __name__ == '__main__':
    for test, values in test_cases.items():
        locals()[test](values)
