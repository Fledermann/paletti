#!/usr/bin/python

import pathlib
import sys

root = pathlib.Path(__file__).resolve().parent.parent

sys.path.append(str(root))

import paletti

query_list = ['Numberphile', 'Numperphile', '######', '123', '  ',
              'Süßigkeiten', '猫视频', 'Māo shìpín', 'видео кота', '098()/(")KNMN']

url_list = ['https://m.youtube.com/watch?v=_pP_C7HEy3g',
            'https://m.youtube.com/watch?v=wZ1E_CM7MqA',
            'https://m.youtube.com/watch?v=bPZFQ6i759g',
            'https://m.youtube.com/watch?v=aKPkQCys86c',
            'https://m.youtube.com/watch?v=3Bv-QMaYlmo',
            'https://m.youtube.com/watch?v=Us-__MukH9I',
            'https://m.youtube.com/watch?v=BDEo5XpZcXo',
            'https://m.youtube.com/watch?v=BDEo5XpZcXo',
            'https://m.youtube.com/watch?v=BDEo5XpZcXo',
            'https://m.youtube.com/watch?v=BDEo5XpZcXo']

other_list = ['https://m.youtube.com/playlist?list=PLAzDjZDAksx3R2p12EJv5tEcnBbJ5RtVQ',
              'https://m.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj',
              'https://www.youtube.com/playlist?list=PLK9Sc5q_4K6aNajVLKtkaAB1JGmKyccf2']
    

def metadatatest(urls):
    for url in urls:
        _ = paletti.metadata(url)
    print(f'metadatatest: ran {len(urls)} tests.')


def playlisttest(urls):
    for url in urls:
        _ = paletti.search(url)
    print(f'playlisttest: ran {len(urls)} tests.')


def searchtest(queries):
    for query in queries:
        _ = paletti.search('youtube', query)
    print(f'searchtest: ran {len(queries)} tests.')


if __name__ == '__main__':
    playlisttest(other_list)
    searchtest(query_list)
    metadatatest(url_list)
