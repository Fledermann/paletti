#!/usr/bin/python

test_cases = {
    'test_search': [
        'Numberphile',
        'Numperphile',
        '######',
        '123',
        '  ',
        'Süßigkeiten',
        '猫视频',
        'Māo shìpín',
        'видео кота',
        '098()/(")KNMN'],

    'test_metadata': [
        'https://m.youtube.com/watch?v=_pP_C7HEy3g',
        'https://m.youtube.com/watch?v=wZ1E_CM7MqA',
        'https://youtube.com/watch?v=bPZFQ6i759g',
        'https://www.youtube.com/watch?v=aKPkQCys86c',
        'https://www.youtube.com/watch?v=3Bv-QMaYlmo',
        'http://youtube.com/watch?v=Us-__MukH9I',
        'http://m.youtube.com/watch?v=BDEo5XpZcXo',
        'http://m.youtube.com/watch?v=BDEo5XpZcXo',
        'https://m.youtube.com/watch?v=BDEo5XpZcXo',
        'https://m.youtube.com/watch?v=BDEo5XpZcXo',
        'https://www.youtube.com/watch?v=5jJTunjNucc',
        'https://www.youtube.com/watch?v=UtMfQzcCmaI'],

    'test_playlist': [
        'http://youtube.com/playlist?list=PLAzDjZDAksx3R2p12EJv5tEcnBbJ5RtVQ',
        'https://m.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj',
        'https://www.youtube.com/playlist?list=PLK9Sc5q_4K6aNajVLKtkaAB1JGmKyccf2'],

    'test_download': [
        #'https://www.youtube.com/watch?v=XlKy3nYIKwE',
        #'https://www.youtube.com/watch?v=eLYhnBaWOzc',
        'https://www.youtube.com/watch?v=DN9DW4rrEjY']
}