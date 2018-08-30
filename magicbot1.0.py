#!/usr/bin/env python3
from slackbot.bot import Bot
from slackbot.bot import respond_to
from slackbot.bot import listen_to
import re
import requests


@respond_to('Give me (.*)', re.IGNORECASE)
def giveme(message, cardname):
    cardname = cardname.replace(" ", '-')
    card_url = "https://api.magicthegathering.io/v1/cards/" + "?name=" + cardname
    data = requests.get(card_url)
    data = data.json()
    data = (data['cards'][1])
    card_text = []
    attributes = ['name', 'cmc', 'type', 'rarity', 'text', 'flavor', 'imageUrl',
                  'printings', 'legalities']
    for i in attributes:
        card_text.append(data[i])
        card_join = '\n'.join(str(e) for e in card_text)
    message.reply('{}'.format(card_join))


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()











