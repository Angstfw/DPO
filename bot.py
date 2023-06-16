import telebot
import pandas as pd
import os
import requests
import json

bot = telebot.TeleBot('6185851405:AAG3x9J0XN33o9zMps88-EkWxjY7n525lg0')
API_URL = os.getenv('API_URL')


df = pd.read_csv('data.csv')

@bot.message_handler(commands=['start'])
# def start_message(message):
#     bot.send_message(message.chat.id, 'Введи Название объекта, брат')
#     bot.register_next_step_handler(message, get_user_id)

def get_user_id(message):
    # user_id = message.text
    bot.send_message(message.chat.id, 'Введите название объекта')
    bot.register_next_step_handler(message, get_object_name)

def get_object_name(message):
    global object_name
    object_name = message.text
    print(object_name)
    bot.send_message(message.chat.id, 'Введите описание объекта')
    bot.register_next_step_handler(message, get_object_description)

def get_object_description(message):
    global object_description
    object_description = message.text
    print(object_description)
    bot.send_message(message.chat.id, 'Введите срок реализации проекта в формате "YYYY-MM-DD"')
    bot.register_next_step_handler(message, get_deadline)

def get_deadline(message):
    global deadline
    deadline  = message.text
    bot.send_message(message.chat.id, 'Введите локацию проекта')
    bot.register_next_step_handler(message, get_location)

def get_location(message):
    global location
    location = message.text
    bot.send_message(message.chat.id, 'Введите кодовое слово на латинице')
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, 'Загрузите фото объекта')
    bot.register_next_step_handler(message, get_photo_path)

def get_photo_path(message):
    try:
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = requests.get(f'https://api.telegram.org/file/bot6185851405:AAG3x9J0XN33o9zMps88-EkWxjY7n525lg0/{file_info.file_path}')
        # отправка post запроса
        response = requests.post('http://{API_URL}/upload_photo', files={'photo': file.content}, data = {"photo_path": f"{name}.jpg"})

        data = {
            'user_id': message.chat.id,
            'object_name': object_name,
            'object_description': object_description,
            'deadline': deadline,
            'location': location,
            'photo_path': f"{name}.jpg"
        }
        response = requests.post('http://{API_URL}:5000/save_data', data=data)

        # отправляем словарь пользователю
        bot.send_message(chat_id=message.chat.id, text=str('Все готово, брат, проверяй'))
    except TypeError:
        bot.send_message(chat_id=message.chat.id, text=str('Что-то ты не то скинул, брат'))
    
# Обработчик всех текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    object_name = message.text
    response = requests.get(f'http://{API_URL}:5000/get_data?object_name={object_name}')
    jsona = json.loads(response.text.replace("\n", ""))

    try:
        object_name = jsona["object_name"]
        object_name = object_name[list(object_name.keys())[0]]

        object_description = jsona["object_description"]
        object_description_data = []
        for key in object_description:
            object_description_data.append(object_description[key])

        location = jsona["location"]
        location_data = []
        for key in location:
            location_data.append(location[key])

        deadline = jsona["deadline"]
        deadline_data = []
        for key in deadline:
            deadline_data.append(deadline[key])

        answer = f"Название объекта: {object_name}\n"
        answer += f"Описание объекта: {object_description_data}\n"
        answer += f"Сроки реализации/запуска объекта: {location_data}\n"
        answer += f"Местоположение объекта: {deadline_data}\n"

        bot.send_message(message.chat.id, answer)

        photo_path = jsona["photo_path"]
        photo_path_data = []

        for key in photo_path:
            photo_path_data.append(photo_path[key])
        
        for photo in photo_path_data:
            url = 'http://{API_URL}:5000/get_photo'
            params = {'filename': photo}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                with open('photo.jpg', 'wb') as file:
                    file.write(response.content)
                    print('Photo saved successfully!')
            else:
                print('Failed to download photo!')
            with open("photo.jpg", 'rb') as photo_to_send:
                        bot.send_photo(message.chat.id, photo_to_send)
    except IndexError:
        bot.send_message(message.chat.id, 'Такого объекта нет, брат')
    

bot.polling()