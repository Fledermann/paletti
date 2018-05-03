#!/usr/bin/python

import paletti

query_list = ['Numberphile', 'Numperphile', '######', '123', '  ',
              'Süßigkeiten', '猫视频', 'Māo shìpín', 'видео кота']


def searchtest(queries):
    for query in queries:
        result = paletti.search('youtube', query)
    print(f'searchtest: ran {len(queries)} tests.')


if __name__ == '__main__':
    searchtest(query_list)