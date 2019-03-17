# !/usr/bin/env python3
# coding: utf8

import json
from re import IGNORECASE
from slackbot.bot import Bot, respond_to
# slackbot requires an api token to work
from requests import get
from random import choice
from time import sleep
from googlesearch import search


# Generates a URL to the first Google entry for a search item.
@respond_to('google (.*)')
def google(message, searchterms):
    list = []
    for i in search(searchterms, tld='com', lang='en', num=1, start=0, stop=1, pause=0.15):
        list.append[i]
    message.send(list)


@respond_to('doug', IGNORECASE)
def doug(message):
    doug_dict = ['i like turtles', 'https://i.imgflip.com/kxncg.jpg',
                 'https://pics.me.me/thumb_snowman-im-cold-im-not-very-attractive-and-i-cant-40582604.png',
                 'https://pics.me.me/snowman-if-you-ever-need-anything-anything-at-all-and-37772162.png',
                 'The NOOP command always succeeds.  It does nothing.']
    message.send(choice(doug_dict))


# Generates a url image of Griselbrand coupled with a random quote from various 80's action movies.
@respond_to('gbear' or 'gbears', IGNORECASE)
def griselbrand(message):
    gbear_urls, gbear_quotes = (["https://img.scryfall.com/cards/large/en/mm3/72.jpg?1523883086",
                                 "https://img.scryfall.com/cards/large/en/pgpx/2015.jpg?1517813031",
                                 "https://cdnb.artstation.com/p/assets/images/images/008/979/889/large/tomas-vareika-griselbrand-comp.jpg?1516447685",
                                 "https://vignette.wikia.nocookie.net/gamelore/images/d/d6/Griselbrand_avatar.jpg/revision/latest?cb=20140106194506"],
                                [" I’ll take my coat back now, asshole.",
                                 " Hey, you wanna be a farmer? Here’s a couple of achers!",
                                 " Don’t let your mouth get your ass in trouble.",
                                 " Donuts don’t wear alligator shoes.",
                                 " Imagine the future, Chains, ’cause you’re not in it.", " How do you like ya ribs?",
                                 " After fucking your wife, I’ll take two.",
                                 " I’m gonna take you to the bank, Senator Trent—to the blood bank!",
                                 " I don’t step on toes… I step on necks.", " I never miss.",
                                 " They’ve been de-kaffir-nated!",
                                 " Go ahead, make my day.", " Always bet on black.",
                                 " You’re a disease… And I’m the cure.",
                                 " Forgiveness is between them and God. It’s my job to arrange the meeting.",
                                 " I have come here to chew bubblegum and kick ass… And I’m all out of bubblegum.",
                                 " Do you feel lucky, punk?", " If it bleeds, we can kill it.",
                                 " Consider that a divorce!",
                                 " Yippee ki yay, motherfucker!"])
    message.send(choice(gbear_urls) + choice(gbear_quotes))


# MTG related JoeCoolFacts quote generator
@respond_to('JCF', IGNORECASE)
def joecoolfacts(message):
    url = "https://random-spark.000webhostapp.com/joecoolfacts.php"
    quote = get(url).text
    message.send(quote)
# dict_json = {"code": "bad", "meal": "hot"}


# Jeopardy json file can be found at https://drive.google.com/file/d/0BwT5wj_P7BKXb2hfM3d2RHU1ckE/view
@respond_to('Jeo' or 'Jeopardy', IGNORECASE)
def jeo(message):
    with open('j.json') as data_file:
        data = json.loads(data_file.read())
    randomdata = choice(data)
    category, value, question, answer = (randomdata["category"]), (randomdata["value"]), \
                                        (randomdata["question"]), (randomdata["answer"])
    message.send(category + '\n' + value + '\n' + question)
    sleep(15)
    message.send(answer)


# Magic 8 Ball, answers to be modified for greater comic effect later.
@respond_to('8ball', IGNORECASE)
def magicball(message):
    answers = ["It is certain.", "I foresee it", "Without a doubt.", "Yes - definitely.", "You can count on it.",
               "As I see it, yes.", "Outlook good.", "Yes", "How Can Mirrors Be Real If Our Eyes Aren't Real",
               "Ask again later.", "I'm gonna need about tree-fiddy to answer that",
               "No. ( ͡° ͜ʖ ͡°) Yes. ( ͡☉ ͜ʖ ͡☉) Maybe. (ง ° ͜ ʖ °)ง", "Don't count on it.",
               "My sources say no","Outlook not so good.", "Very doubtful." "If I told you no, would you believe it?",
               "Ahahahahahahahah...No.", "Does Doug Durdle?", "All signs point to yes", "Bruh.", "I like turtles."]
    message.send(choice(answers))


# Generates a randomized Trump quote from a free and public api
@respond_to('TRUMP', IGNORECASE)
def trump(message):
    """
    ¯\_(ツ)_/¯ alternative quotes, for fact checking alternative facts, source: fake news ¯\_(ツ)_/¯
    """
    message.send((get("https://api.whatdoestrumpthink.com/api/v1/quotes/random").json())["message"])


@respond_to('Give me (.*)' or '! (.*)', IGNORECASE)
def mtglookup(message, cardname):
    """
    Generates and responds with a set of key: value entries for any magic card specified
    @bot_name give me {magic card}
    """
    # str.replace(old, new, [, count])
    attributes = ['name', 'mana_cost', 'type_line', 'oracle_text', 'rarity', 'set_name', 'setName', 'artist',
                  'multiverse_ids', 'rulings', 'printings', 'originalText', 'legalities', 'released_at',
                  'scryfall_uri', 'flavor_text', 'artist', 'prices', 'border_crop', 'mtgtop8', 'related_uris',
                  'purchase_uris']
    try:
        data = ((get("https://api.scryfall.com/cards/named?exact=" + cardname.replace(" ", '_'))).json())
        if 'status' in data:
            message.send('{} {} {}'.format(data['status'], data['object'], data['details']))
    finally:
        if 'status' not in data:
            message.send('{}'.format(transform_dict(flatten_nested_dict(data), attributes)))


# Slackbot automatically displays valid chat commands when an error is created. This is another way to call that info.
@respond_to('help' or 'helpme', IGNORECASE)
def bothelp(message):
    """
    Slackbot automatically displays valid chat commands when an error is created.
    This is another way to call that info.
    """

    help_message = ("MagicBot responds to different arguments all following the prefix @magic-bot or simply !"
                    '\n' "give me {card}" '\n\t*'
                    "Prints out data of the requested magic card"
                    '\n' "gbear" '\n\t*' "aka gg" '\n' "jeo" '\n\t*' "Random Jeopardy question with answer delay"
                    '\n' "meb {question}" '\n\t*' "MagicEightBall" '\n' "trump" '\n\t*' "Random Trump quote" '\n'
                    "jcf" '\n\t*' "Random JoeCoolFacts quote" '\n' "google {search terms}" '\n\t*' "Returns the "
                    "first entry of a google search")

    message.reply(help_message)


def main():
    bot = Bot()
    bot.run()


def flatten_nested_dict(data):
    """
    Flatten nested dicts
    """
    for item in list(data):
        if type(item) is dict:
            for key in item:
                data[key] = item[key]
    return data


# pass your dict/json object as data and your desired keys to extract as a list of attributes outputs key / value format
def transform_dict(data, attributes):
    """
    Transform dict structure to a specific format
    """
    item_text = []
    try:
        for key in data:
            if key in attributes:
                item_text.append(key + ":" + (" " * (16-len(key))) + '{}'.format(data[key]))
                item_join = ('\n'.join(str(e) for e in item_text))
    except NameError:
        print(NameError, "whoops")
    finally:
        return item_join


if __name__ == "__main__":
    main()

