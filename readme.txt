Это Flask приложение позволяет сохранять данные в CSV файл и загружать фотографии.

Установка
Склонируйте репозиторий на свой компьютер.
Установите зависимости из файла requirements.txt с помощью команды pip install -r requirements.txt.
Запуск
Запустите приложение с помощью команды python app.py.
Использование
Сохранение данных
Для сохранения данных отправьте POST запрос на адрес http://localhost:5000/save_data со следующими параметрами:

user_id (int) - ID пользователя.
object_name (str) - Название объекта.
object_description (str) - Описание объекта.
deadline (str) - Дата окончания.
location (str) - Местоположение.
photo_path (str) - Путь к фотографии.
Получение данных
Для получения данных отправьте GET запрос на адрес http://localhost:5000/get_data со следующими параметрами:

object_name (str) - Название объекта.
Загрузка фотографии
Для загрузки фотографии отправьте POST запрос на адрес http://localhost:5000/upload_photo со следующими параметрами:

photo (file) - Файл фотографии.
photo_path (str) - Путь к фотографии.
Получение фотографии
Для получения фотографии отправьте GET запрос на адрес http://localhost:5000/get_photo со следующими параметрами:

filename (str) - Имя файла фотографии.

Возможно использование бота вместе с приложением при использовании docker-compose файла
Установка
Склонируйте репозиторий на свой компьютер.
Запуск
Запустите приложение и бота с помощью команды compose up.