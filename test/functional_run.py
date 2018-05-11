#!/usr/bin/python

""" This module is intended for functional testing, since many of the complex
tasks, like crawling and streaming, cannot be unit-tested reasonably.

"""

import inspect
import pathlib
import random
import sys
import threading
import time

import functional.cases

root = pathlib.Path(__file__).resolve().parent.parent
sys.path.append(str(root))

import paletti
import paletti.utils
    

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
    d = paletti.download(url, '/tmp')
    d.start()
    while True:
        time.sleep(1)
        if d.status != 'active':
            break
        print(f'\r{d.output:.20s}...: {d.progress/1024:7.0f} of {d.filesize/1024:7.0f} kb.', end='')
    print('')


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
    test_subject = 'all'
    try:
        test_subject = sys.argv[1]
    except IndexError:
        pass

    # Find and add all functional tests to a list.
    test_cases = dict(paletti=functional.cases.test_cases)
    plugin_tests = paletti.utils.find_modules('tests')
    for pt in plugin_tests:
        if pt['type'] == 'functional':
            test_cases[pt['plugin']] = pt['module'].test_cases

    for subject, case in test_cases.items():
        if subject == test_subject or test_subject == 'all':
            for test, values in case.items():
                locals()[test](values)
