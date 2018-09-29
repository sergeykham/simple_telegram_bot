import telebot
import os
import time
import random
import flask
from flask import Flask

app = Flask(__name__)

bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

typical_phrases = [
    'Гениально',
    'Цвета говно',
    'Сообщение удалено',
    'Вы - звезды',
    'Цифровизация',
    'Фрилансеры в Саранске',
    'Ну что, поехали?',
    'А че, диджея не буде?',
    'Спасайте! Карту по культуре!',
    'Карточки мечты',
    'Проверь на опечатки',
    'Все самое важное на 11 странице, все остальное можно не читать',
    'Сейчас на экране появится...',
    'Включаем мою лекцию про дофамин',
    'Все в аудио',
    'Я экстраверт',
    'Я интроверт',
    'Благодарен за обратную связь',
    'Отпустите меня в туалет',
    'Сколько по Яндексу ехать?',
    '...взять эту, я извиняюсь, фигню...',
    'я несу людям чудо',
    'Курсы! Курсы! Курсы!',
    'Работаем!',
    'Так, заходим в Sli.do!',
    'Варя видела это?',
    'а какие ваши предложения?',
    'давайте сделаем из этого библиотеку лучших практик',
    'если видите лисичку в зеленых носочках, так и говорите "лисичка в зеленых носочках"!!!',
    'Сейчас расскажу про Бриф. Объясняю на пальцах....',
    'аааа! Хочу!',
    'Кто ведет? ведет кто?',
    'А сейчас я хочу передать слово человеку, который лучше меня знает, зачем мы все здесь собрались',
    'игра закончилась, и вы больше ничего не сможете изменить',
    'Это не на сейчас, это в дальний бэклог!',
    'Крууууууто! Ой, круууууто-то кааааак!',
]
old_message = random.choices(typical_phrases)

WEBHOOK_URL_BASE = "https://murmuring-ridge-70204.herokuapp.com"
WEBHOOK_URL_PATH = "/%s/" % (bot_token)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

@bot.message_handler(commands=['start','help'])
def send_welcome(message):
    user = message.from_user.first_name
    bot.reply_to(message,
     "Привет, %s, я - Цифровой Олег :) Можешь задать мне вопрос!"%(user))

@bot.message_handler(func=lambda message: True)
def send_random_message(message):
    new_message = random.choices(typical_phrases)
    while new_message == old_message:
        new_message = random.choices(typical_phrases)
    bot.reply_to(message, new_message)

bot.remove_webhook()

time.sleep(0.1)

# Set webhook

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)

# Start flask server
if __name__ == '__main__':
    app.run()
