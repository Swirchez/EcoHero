import telebot
from telebot import types
import random

bot = telebot.TeleBot('TOKEN')
user_data = {}
numbers = '0123456789'
letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

quizzes = {
    "Новичок 🌱": [
        {
            "question": "Сколько лет разлагается пластиковая бутылка?",
            "options": ["50 лет", "200 лет", "450 лет", "500 лет"],
            "answer": 2
        },
        {
            "question": "Какой способ передвижения самый экологичный?",
            "options": ["Автомобиль", "Велосипед", "Самолет", "Автобус"],
            "answer": 1
        },
        {
            "question": "Какая из этих вещей является биодеградируемой?",
            "options": ["Пластиковая упаковка", "Стеклянная бутылка", "Металлическая банка", "Банановая кожура"],
            "answer": 3
        },
        {
            "question": "Что из этого нельзя переработать?",
            "options": ["Газета", "Стекло", "Композитный материал", "Пластик"],
            "answer": 2
        },
        {
            "question": "Какой вид отходов можно переработать на 100%?",
            "options": ["Пластик", "Стекло", "Металл", "Бумага"],
            "answer": 1
        }
    ],
    "Любитель 🌿": [
        {
            "question": "Сколько воды тратится на производство 1 кг говядины?",
            "options": ["15 000 литров", "5 000 литров", "1000 литров", "500 литров"],
            "answer": 0
        },
        {
            "question": "Что из этого нельзя переработать?",
            "options": ["Стеклянная бутылка", "Пластиковая упаковка", "Одноразовый стаканчик с покрытием", "Консервная банка"],
            "answer": 2
        },
        {
            "question": "Какую энергию производит ветряная установка?",
            "options": ["Тепловая энергия", "Электрическая энергия", "Механическая энергия", "Химическая энергия"],
            "answer": 1
        },
        {
            "question": "Какой из этих видов транспорта наименее экологичен?",
            "options": ["Электрический автобус", "Гибридный автомобиль", "Трамвай", "Самолет"],
            "answer": 3
        },
        {
            "question": "Какой ресурс является возобновляемым?",
            "options": ["Газ", "Уголь", "Солнечная энергия", "Нефть"],
            "answer": 2
        }
    ],
    "Эксперт 🌳": [
        {
            "question": "Какой процент пластика перерабатывается в мире?",
            "options": ["9%", "15%", "25%", "50%"],
            "answer": 0
        },
        {
            "question": "Сколько CO2 выделяет один поисковый запрос в интернете?",
            "options": ["0.2 грамма", "2 грамма", "5 граммов", "20 грамм"],
            "answer": 1
        },
        {
            "question": "Какая страна производит больше всего углекислого газа на душу населения?",
            "options": ["США", "Китай", "Россия", "Катар"],
            "answer": 3
        },
        {
            "question": "Какой материал используется для создания солнечных панелей?",
            "options": ["Медь", "Золото", "Кремний", "Сталь"],
            "answer": 2
        },
        {
            "question": "Какой из этих методов получения энергии является самым чистым?",
            "options": ["Угледобыча", "Гидроэнергетика", "Ветроэнергетика", "Ядерная энергетика"],
            "answer": 2
        }
    ]
}

def show_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🎯 Викторина")
    markup.row("📊 Статистика", "🏬 Магазин")
    bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Новичок 🌱")
    button2 = types.KeyboardButton("Любитель 🌿")
    button3 = types.KeyboardButton("Эксперт 🌳")
    markup.add(button1, button2, button3)
    
    bot.send_message(
        message.chat.id, 
        "Привет, Я EcoHero, твой помощник для вклада в экологию. Выбери свой ранг для получения викторин соответствующей сложности:", 
        reply_markup=markup
    )
    
    if message.from_user.id not in user_data:
        user_data[message.from_user.id] = {
            'points': 0,
            'rank': None,
            'completed_quizzes': 0,
            'promocodes': [],
            'vip': "Неактивный"
        }

@bot.message_handler(func=lambda message: message.text in ["Новичок 🌱", "Любитель 🌿", "Эксперт 🌳"])
def set_rank(message):
    user_id = message.from_user.id
    rank = message.text
    user_data[user_id]['rank'] = rank

    show_main_menu(message.chat.id)
    
    bot.send_message(
        message.chat.id,
        "Твой ранг: " + rank + ". Нажми '🎯 Викторина' для получения вопроса за который дадут ЭкоБаллы."
    )

@bot.message_handler(func=lambda message: message.text == "🎯 Викторина")
def send_quiz(message):
    user_id = message.from_user.id
    
    if user_id not in user_data or user_data[user_id]['rank'] is None:
        start(message)
        return
    
    rank = user_data[user_id]['rank']
    if rank in quizzes and quizzes[rank]:
        quiz = random.choice(quizzes[rank])
        
        markup = types.InlineKeyboardMarkup()
        for i, option in enumerate(quiz["options"]):
            button = types.InlineKeyboardButton(option, callback_data="quiz_" + str(i))
            markup.add(button)
        
        bot.send_message(
            message.chat.id,
            "📚 Викторина (" + rank + "): " + quiz['question'],
            reply_markup=markup
        )
    else:
        bot.send_message(message.chat.id, "Пока нет новых викторин для твоего ранга")

@bot.message_handler(func=lambda message: message.text == "📊 Статистика")
def show_stats(message):
    user_id = message.from_user.id
    if user_id in user_data:
        stats = user_data[user_id]
        message_text = (
            "📊 Твоя статистика:\n"
            "• Ранг: " + (stats['rank'] if stats['rank'] else 'Не выбран') + "\n"
            "• ЭкоБаллы: " + str(stats['points']) + "\n"
            "• Пройдено викторин: " + str(stats['completed_quizzes']) + "\n"
            "• Промокоды: " + (', '.join(stats['promocodes']) if stats['promocodes'] else 'Нет') + "\n"
            "• VIP-статус: " + stats['vip']
        )
        bot.send_message(message.chat.id, message_text)
    else:
        start(message)

@bot.callback_query_handler(func=lambda call: call.data.startswith('quiz_'))
def handle_quiz_answer(call):
    user_id = call.from_user.id
    if user_id not in user_data:
        return
    
    selected_option = int(call.data.split('_')[1])
    rank = user_data[user_id]['rank']
    
    if rank not in quizzes:
        return
    
    for quiz in quizzes[rank]:
        if quiz['question'] in call.message.text:
            correct_answer = quiz['answer']
            break
    else:
        return
    
    if selected_option == correct_answer:
        points_earned = 15
        user_data[user_id]['points'] += points_earned
        user_data[user_id]['completed_quizzes'] += 1
        
        message_text = (
            "✅ Правильно! +" + str(points_earned) + " ЭкоБаллов.\n"
            "Твой баланс: " + str(user_data[user_id]['points'])
        )
    else:
        correct_option = quiz['options'][correct_answer]
        message_text = "❌ Неверно. Правильный ответ: " + correct_option
    
    bot.answer_callback_query(call.id, message_text, show_alert=True)
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=None
    )

@bot.message_handler(func=lambda message: message.text == "🏬 Магазин")
def shop(message):
    user_id = message.from_user.id
    
    if user_id not in user_data:
        start(message)
        return
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Купить промокод (45 баллов)")
    markup.row("Купить VIP-статус (150 баллов)")
    markup.row("Назад")
    
    balance = user_data[user_id]['points']
    shop_message = (
        "🏬 Магазин\n"
        "Здесь ты можешь:\n"
        "- Купить промокод за 45 ЭкоБаллов\n"
        "- Купить VIP-статус за 150 ЭкоБаллов\n\n"
        "Твой баланс: " + str(balance) + " ЭкоБаллов"
    )
    
    bot.send_message(message.chat.id, shop_message, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Купить промокод (45 баллов)")
def buy_promo(message):
    user_id = message.from_user.id
    
    if user_id not in user_data:
        start(message)
        return
    
    if user_data[user_id]['points'] < 45:
        bot.send_message(
            message.chat.id,
            "❌ Недостаточно ЭкоБаллов! Нужно 45, а у тебя только " + str(user_data[user_id]['points']) + ".\n"
            "Выполняй больше заданий!",
            reply_markup=types.ReplyKeyboardRemove()
        )
        show_main_menu(message.chat.id)
        return
    
    promocode = (
        ''.join(random.choices(letters, k=3)) +
        random.choice(numbers) +
        ''.join(random.choices(letters, k=3)) +
        random.choice(numbers)
    )
    
    user_data[user_id]['points'] -= 45
    user_data[user_id]['promocodes'].append(promocode)
    
    bot.send_message(
        message.chat.id,
        "🎉 Поздравляем! Твой промокод: " + promocode + ".\n"
        "Новый баланс: " + str(user_data[user_id]['points']) + " ЭкоБаллов",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "Купить VIP-статус (150 баллов)")
def buy_vip(message):
    user_id = message.from_user.id
    
    if user_id not in user_data:
        start(message)
        return
    
    if user_data[user_id]['points'] < 150:
        bot.send_message(
            message.chat.id,
            "❌ Недостаточно ЭкоБаллов! Нужно 150, а у тебя только " + str(user_data[user_id]['points']) + ".\n"
            "Выполняй больше заданий!",
            reply_markup=types.ReplyKeyboardRemove()
        )
        show_main_menu(message.chat.id)
        return
    
    user_data[user_id]['points'] -= 150
    user_data[user_id]['vip'] = "Активный👑"

    bot.send_message(
        message.chat.id,
        "🎉 Поздравляем! Вы активировали VIP-статус.\n"
        "Новый баланс: " + str(user_data[user_id]['points']) + " ЭкоБаллов",
        reply_markup=types.ReplyKeyboardRemove()
    )
    
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: message.text == "Назад")
def back_to_menu(message):
    show_main_menu(message.chat.id)

if __name__ == '__main__':
    print("EcoHero запущен!")
    bot.polling(none_stop=True)
