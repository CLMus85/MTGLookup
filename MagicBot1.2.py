# Version 1.4 - Added a JoeCoolFacts quote generator, a Griselbrand tribute, and a commands list
#!/usr/bin/env python3
import re, random, json
from slackbot.bot import Bot, respond_to
from requests import get
from time import sleep


@respond_to('gbear' or 'gbears', re.IGNORECASE)
def griselbrand(message):
    gbear_urls = ["https://img.scryfall.com/cards/large/en/mm3/72.jpg?1523883086",
                  "https://img.scryfall.com/cards/large/en/pgpx/2015.jpg?1517813031",
                  "https://cdnb.artstation.com/p/assets/images/images/008/979/889/large/tomas-vareika-griselbrand-comp.jpg?1516447685",
                  "http://www.mtgcanada.com/wp-content/themes/jubini/framework/modules/timthumb/timthumb.php?src=http%3A%2F%2Fwww.mtgcanada.com%2Fwp-content%2Fuploads%2F2015%2F09%2Findex10.jpg&w=930&h=350&zc=1",
                  "https://vignette.wikia.nocookie.net/gamelore/images/d/d6/Griselbrand_avatar.jpg/revision/latest?cb=20140106194506"]
    url = gbear_urls[random.choice(gbear_urls)]
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
    quote = gbear_quotes[random.choice(gbear_quotes)]
    message.reply(url + quote)


@respond_to('JCF', re.IGNORECASE)
def joecoolfacts(message):
    url = "https://random-spark.000webhostapp.com/joecoolfacts.php"
    quote_data = get(url)
    quote = quote_data.text
    message.reply(quote)


@respond_to('JEO', re.IGNORECASE)
def thegame(message):
    with open('j.json') as data_file:
        data = json.loads(data_file.read())
    randomint = random.randint(0, 216929)
    category, value, question, answer = (data[randomint]["category"]), (data[randomint]["value"]),\
                                        (data[randomint]["question"]), (data[randomint]["answer"])
    message.reply(category, value, question)
    sleep(15)
    message.reply(answer)


@respond_to('MEB', re.IGNORECASE)
def magicball(message):
    answers = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You can count on it.",
               "As I see it, yes.", "Most likely.", "Outlook good.", "Yes", "Signs point to yes.",
               "Reply hazy, try again",
               "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
               "Don't count on it.", "No.", "My sources say no", "Outlook not so good.", "Very doubtful."]
    answer = answers[random.choice(answers)]
    message.reply(answer)


@respond_to('TRUMP', re.IGNORECASE)
def trump_quote(message):
    url = "https://api.whatdoestrumpthink.com/api/v1/quotes/random"
    data = get(url)
    data = data.json()
    response = data["message"]
    message.reply(response)


@respond_to('Give me (.*)', re.IGNORECASE)
def giveme(message, cardname):
    cardname = cardname.replace(" ", '-')
    card_url = "https://api.magicthegathering.io/v1/cards/?name=" + cardname
    data = get(card_url)
    data = data.json()
    data = (data['cards'][1])
    attributes = ['name', 'manaCost', 'type', 'rarity', 'set', 'setName', 'text', 'artist', 'imageUrl', 'multiverseid',
                  'rulings', 'printings', 'originalText', 'legalities']
    card_text = []
    try:
        for i in attributes:
            card_text.append(data[i])
            card_join = '\n'.join(str(e) for e in card_text)
        message.reply('{}'.format(card_join))
    except KeyError:
        raise


@respond_to('commands', re.IGNORECASE)
def help(message):
    help_message = ("MagicBot responds to different arguments all following the prefix @magic-bot" '\n' "give me card" '\n\t' 
                    "Prints out data of requested magic card" 
                    '\n' "gbear" '\n\t' "aka gg" '\n' "jeo" '\n\t' "Random Jeopardy question answer delay" 
                    '\n' "meb" '\n\t' "MagicEightBall" '\n' "trump" '\n\t' "Random Trump quote" '\n'
                     "jcf" '\n\t' "Random JoeCoolFacts quote")
    message.reply(help_message)



def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    main()
