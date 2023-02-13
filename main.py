import telebot
from random import choice
from json import load


class Joke:
    def __init__(self, name: str):
        self.name = name
        self.stickers = None
        self.answers = None
        self.triggers = None
        self.triggers2 = None

    def chaser(self, message):
        if self.name == "dormitory":
            for i in self.triggers2:
                if i in str(message.text).lower():
                    break
            else:
                return False
        for i in self.triggers:
            if i in str(message.text).lower():
                return True

    def generate_joke(self):
        sticker = choice(tuple(self.stickers.keys()))
        answer: str = ""
        match sticker:
            case "IQ":
                answer = "Плохие новости..."
            case _:
                answer = choice(self.answers)
        return answer, self.stickers[sticker]


def initialize_Joke(data: dict, instance: Joke):
    setattr(instance, "triggers", data[f"{instance.name}_triggers"])
    setattr(instance, "stickers", data[f"sticker_{instance.name}_data"])
    setattr(instance, "answers", data[f"answer_{instance.name}_data"])


def reply(message, joke: Joke):
    answer, sticker = joke.generate_joke()
    bot.reply_to(message, answer)
    bot.send_sticker(message.chat.id, sticker)


kpi = Joke(name="kpi")
fiot = Joke(name="fiot")
teff = Joke(name="teff")
dormitory = Joke(name="dormitory")

if __name__ == '__main__':
    with open("KpiData.json") as jsondata:
        kdata = load(jsondata)
        token = kdata["token"]

    for i in (kpi, fiot, teff, dormitory):
        initialize_Joke(kdata, i)
    dormitory.triggers2 = kpi.triggers

bot = telebot.TeleBot(token)


@bot.message_handler(commands=["KpiAuthor"])
def author(message):
    bot.send_message(message.chat.id, "@Bhd_shvk04")


@bot.message_handler(func=dormitory.chaser)
def kpi_rep(message):
    reply(message, dormitory)


@bot.message_handler(func=kpi.chaser)
def kpi_rep(message):
    reply(message, kpi)


@bot.message_handler(func=fiot.chaser)
def kpi_rep(message):
    reply(message, fiot)


@bot.message_handler(func=teff.chaser)
def kpi_rep(message):
    reply(message, teff)


if __name__ == '__main__':
    bot.polling()
