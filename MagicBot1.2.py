#!/usr/bin/env python3
from slackbot.bot import Bot
from slackbot.bot import respond_to
import re
import requests
import random


@respond_to('MEB')
def MagicBall(message):
    answers = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.",
               "As I see it, yes.", "Most likely.", "Outlook good.", "Yes", "Signs point to yes.",
               "Reply hazy, try again",
               "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
               "Don't count on it.", "My reply is no.", "My sources say no", "Outlook not so good.", "Very doubtful."]
    answer = answers[random.randint(0, len(answers))-1]
    message.reply(answer)


@respond_to('Give me (.*)', re.IGNORECASE)
def giveme(message, cardname):
    cardname = cardname.replace(" ", '-')
    card_url = "https://api.magicthegathering.io/v1/cards/" + "?name=" + cardname
    data = requests.get(card_url)
    data = data.json()
    data = (data['cards'][1])
    attributes = ['name', 'manaCost', 'type', 'rarity', 'text', 'imageUrl', 'printings']
    card_text = []
    for i in attributes:
        card_text.append(data[i])
        card_join = '\n'.join(str(e) for e in card_text)
    message.reply('{}'.format(card_join))


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
