# Version 1.3 - Added a small Jeopardy game, a magic 8 ball, and a random Trump quote generator.
#!/usr/bin/env python3
from slackbot.bot import Bot
from slackbot.bot import respond_to
import re, random, json
from requests import get
from time import sleep


@respond_to('JEO', re.IGNORECASE)
def thegame(message):
    with open('j.json') as data_file:  # https://drive.google.com/file/d/0BwT5wj_P7BKXb2hfM3d2RHU1ckE/view for the json file
        data = json.loads(data_file.read())
    randomint = random.randint(0, 216930)
    category, value, question, answer = (data[randomint]["category"]), (data[randomint]["value"]),\
                                        (data[randomint]["question"]), (data[randomint]["answer"])
    message.reply(category)
    message.reply(value)
    sleep(2)
    message.reply(question)
    sleep(15)
    message.reply(answer)


@respond_to('MEB', re.IGNORECASE)
def MagicBall(message):
    answers = ["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You can count on it.",
               "As I see it, yes.", "Most likely.", "Outlook good.", "Yes", "Signs point to yes.",
               "Reply hazy, try again",
               "Ask again later.", "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
               "Don't count on it.", "No.", "My sources say no", "Outlook not so good.", "Very doubtful."]
    answer = answers[random.randint(0, len(answers))-1]
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
    card_url = "https://api.magicthegathering.io/v1/cards/" + "?name=" + cardname
    data = get(card_url)
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
