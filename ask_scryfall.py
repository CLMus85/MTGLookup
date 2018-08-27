#!/usr/bin/env python3
# encoding: utf-8


import requests

cardname = input()


def giveme(cardname):
    card_url = "https://api.scryfall.com/cards/named?exact=" + cardname
    data = requests.get(card_url)
    data = data.json()
    attributes = ['name', 'mana_cost', 'type_line', 'oracle_text', 'rarity', 'artist', 'usd',
                  'purchase_uris', 'legalities', 'flavor_text']
    try:
        for i in attributes:
            print(data[i])
    except Exception:
        print(Exception)
        pass


giveme(cardname)
