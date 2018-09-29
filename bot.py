import os

import telebot
import random
from flask import Flask, request, render_template

bot_token = os.environ['BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

"""typical_phrases = [
    'Гениально',
    'Цвета говно',
    'Сообщение удалено',
    'Вы - звезды',
    'Цифровизация',
    'Фрилансеры в Саранске',
    'Ну что, поехали?',
    'А че, диджея не будет?',
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
"""
typical_phrases = ["Тест"]
old_message = random.choices(typical_phrases)

app = Flask(__name__)

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

@app.route('/')
def hello_world():
    bot.remove_webhook()
    bot.set_webhook(url='https://murmuring-ridge-70204.herokuapp.com/' + bot_token)
    return render_template("index.html")

@app.route('/change_phrases', methods=['POST'])
def change_phrases():
    phrases = request.form['phrases'].split('\n')
    typical_phrases.append(phrases)
    return 'Ксюша, фразы %s успешно добавлены в бота!'%(phrases)
    

# Process webhook calls
@app.route('/' + bot_token, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

# Start flask server
app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
