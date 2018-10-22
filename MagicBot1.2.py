# - Version 1.6 -
# Changed - to _ in mtglookup to match the APIs url format
# Fixed consistency issues with ifeellucky by redefining the method for obtaining the url
# Changed variable and function names for clarity and simplicity as well as updating help function

# !/usr/bin/env python3
# coding: utf8
import re, random, json
from slackbot.bot import Bot, respond_to
from requests import get
from time import sleep
from bs4 import BeautifulSoup


# Generates a URL to the first Google entry for a search item.
@respond_to('google (.*)')
def google(message, searchterms):
    url = "http://www.google.com/search?hl=en&q=" + searchterms
    htmlresponse = get(url)
    soup = BeautifulSoup(htmlresponse.text, "html.parser")
    linksoup = soup.select('.r a')
    firstlink = (linksoup[0].get('href'))
    message.reply(firstlink.replace('/url?q=', ' '))


# Generates a url image of Griselbrand coupled with a random quote from various 80's action movies.
@respond_to('gbear' or 'gbears', re.IGNORECASE)
def griselbrand(message):
    gbear_urls = ["https://img.scryfall.com/cards/large/en/mm3/72.jpg?1523883086",
                  "https://img.scryfall.com/cards/large/en/pgpx/2015.jpg?1517813031",
                  "https://cdnb.artstation.com/p/assets/images/images/008/979/889/large/tomas-vareika-griselbrand-comp.jpg?1516447685",
                  "https://vignette.wikia.nocookie.net/gamelore/images/d/d6/Griselbrand_avatar.jpg/revision/latest?cb=20140106194506"]
    url = random.choice(gbear_urls)
    gbear_quotes = [" I’ll take my coat back now, asshole.", " Hey, you wanna be a farmer? Here’s a couple of achers!",
                    " Don’t let your mouth get your ass in trouble.", " Donuts don’t wear alligator shoes.",
                    " Imagine the future, Chains, ’cause you’re not in it.", " How do you like ya ribs?",
                    " After fucking your wife, I’ll take two.",
                    " I’m gonna take you to the bank, Senator Trent—to the blood bank!",
                    " I don’t step on toes… I step on necks.", " I never miss.", " They’ve been de-kaffir-nated!",
                    " Go ahead, make my day.", " Always bet on black.", " You’re a disease… And I’m the cure.",
                    " Forgiveness is between them and God. It’s my job to arrange the meeting.",
                    " I have come here to chew bubblegum and kick ass… And I’m all out of bubblegum.",
                    " Do you feel lucky, punk?", " If it bleeds, we can kill it.", " Consider that a divorce!",
                    " Yippee ki yay, motherfucker!"]
    quote = random.choice(gbear_quotes)
    message.reply(url + quote)


# MTG related JoeCoolFacts quote generator
@respond_to('JCF', re.IGNORECASE)
def joecoolfacts(message):
    url = "https://random-spark.000webhostapp.com/joecoolfacts.php"
    quote = get(url).text
    message.reply(quote)


# Jeopardy json file can be found at https://drive.google.com/file/d/0BwT5wj_P7BKXb2hfM3d2RHU1ckE/view
@respond_to('Jeo' or 'Jeopardy', re.IGNORECASE)
def jeo(message):
    with open('j.json') as data_file:
        data = json.loads(data_file.read())
    randomdata = random.choice(data)
    category, value, question, answer = (randomdata["category"]), (randomdata["value"]), \
                                        (randomdata["question"]), (randomdata["answer"])

    message.reply(category + '\n' + value + '\n' + question)
    sleep(15)
    message.reply(answer)


# Magic 8 Ball, answers to be modified for greater comic effect later.
@respond_to('MEB', re.IGNORECASE)
def magicball(message):
    answers = ["It is certain.", "I foresee it", "Without a doubt.", "Yes - definitely.", "You can count on it.",
               "As I see it, yes.", "Most likely.", "Outlook good.", "Yes", "Reply hazy, try again",
               "Ask again later.", "Cannot predict now, but for tree-fiddy, I'll make an exception",
               "¯\_(ツ)_/¯", "Don't count on it.", "No.", "My sources say no",
               "Outlook not so good.", "Very doubtful." "If I told you no, would you believe it?", "Ahahahahahahahah...No.",
               "Truer words have never been spoken", "All signs point to yes", "bruh. totally",
               "I like turtles."]
    answer = random.choice(answers)
    message.reply(answer)

# Generates a randomized Trump quote from a free and public api
@respond_to('TRUMP', re.IGNORECASE)
def trump(message):
    url = "https://api.whatdoestrumpthink.com/api/v1/quotes/random"
    data = get(url)
    data = data.json()
    response = (data["message"])
    message.reply(response)


# Generates and responds with a set of key: value entries for any magic card specified - ! give me {magic card} in chat
@respond_to('Give me (.*)', re.IGNORECASE)
def mtglookup(message, cardname):
    cardname = cardname.replace(" ", '_')  # str.replace(old, new, [, count])
    card_url = "https://api.magicthegathering.io/v1/cards/?name=" + cardname
    data = get(card_url)
    data = data.json()
    data = (data['cards'][1])
    attributes = ['name', 'manaCost', 'type', 'rarity', 'set', 'setName', 'text', 'artist', 'imageUrl', 'multiverseid',
                  'rulings', 'printings', 'originalText', 'legalities']
    card_text = []
    # [(key + " : " + '{}'.format(data[key])) for key in data.keys() if key in attributes] list comp to be implemented
    """We don't want every dictionary key, and not all attributes apply in every case, 
    so we compare lists and output to a desired format"""
    for key in data.keys():
        if key in attributes:
            card_text.append(key + "   *   " + '{}'.format(data[key]))
            card_join = '\n'.join(str(e) for e in card_text)
    message.reply('{}'.format(card_join))


# Slackbot automatically displays valid chat commands when an error is created. This is another way to call that info.
@respond_to('help' or 'helpme', re.IGNORECASE)
def bothelp(message):
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


if __name__ == "__main__":
    main()

