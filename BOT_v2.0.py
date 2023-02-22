import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
import time
import openai
import logging
from PIL import Image, PngImagePlugin
import secrets
import sqlite3
import datetime
import csv
from send_photo import send_photo
from generate_response import generate_response
from generet import generet
from set_user_gen_limit import set_user_gen_limit
from dalle_ai import dalle_ai
from send_dalle import send_dalle
from repost_vk_group import repost_vk_group
from gen_promt import gen_promt
from generet_img_group import generet_img_group
from repost_vk_name import repost_vk_name



openai_api_key = "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"
openai.api_key = openai_api_key
vk_token = ("vk1.a.mxEpwbhYSgGnpFgHcckzsynpF7KCCaYOzVSnVcbrfV_XohaDteWezoCS8hgGCZOPW_JMi1w2uoDdW25SYnGygtRXQeJfNDXLszRY1wLacY63CQ_h3Y2jdbriUp4a-AWd42jAw2IgxFH-y_sn36PLb5HyCYlOSVj8NcSg_uGBWqK7DB0q3h-KxCrCMc3K0dWNminmPhInw5d1igJAsB8lXA")
vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
print("connect to vk")


# Устанавливаем уровень логирования и имя файла для логов
logging.basicConfig(filename='bot.csv', level=logging.DEBUG)


conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                (id integer PRIMARY KEY, "name" integer, "limit" integer, "excluded" integer, ignore_time real, gen_limit integer,"admin" integer, gen_ignore_time real)''')




# Основной цикл обработки сообщений
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    user_id = event.user_id
                    message = event.text
                    # получаем информацию о пользователе
                    user_info = vk.users.get(user_ids=user_id, name_case='nom')[0]
                    user_name = user_info['first_name'] + ' ' + user_info['last_name']
                    user_limits = (5, 0, 0, 5, 0) # устанавливаем лимит по умолчанию
                    # Логируем сообщение
                    logging.info(f"{user_name} ({user_id}) написал: {message}")
                    
                    # Проверка, является ли пользователь администратором
                    user_admin = cursor.execute('SELECT admin FROM users WHERE id=?', (user_id,)).fetchone()
                    if user_admin is not None and user_admin[0] == 1:
                        # пользователь является администратором, устанавливаем бесконечный лимит на генерацию
                        gen_limit = 5000
                    else:
                        # пользователь не является администратором, используем обычный лимит
                        # проверяем, есть ли автор в базе
                        user_limits = cursor.execute('SELECT "limit", "excluded", ignore_time, gen_limit, gen_ignore_time FROM users WHERE id=?', (user_id,)).fetchone()
                        if user_limits is None:
                            # если автора нет в базе, добавляем его с лимитом 5 и без исключения
                            cursor.execute('INSERT INTO users (id, name, "limit", "excluded", ignore_time, gen_limit, gen_ignore_time, admin) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (user_id, user_name, 5, 0, 0, 10, 0, 0))
                            conn.commit()
                            
                        gen_limit = user_limits[3]

                        
                    
                    # остальной код обработки сообщений
                    # ...
                    # Обрабатываем команду "steps"
                    if "steps" in message.lower():
                        # Проверка, является ли пользователь администратором
                        user_admin = cursor.execute('SELECT admin FROM users WHERE id=?', (user_id,)).fetchone()
                        if user_admin is not None and user_admin[0] == 1:
                            steps = ''.join(filter(str.isdigit, message))
                            vk.messages.send(user_id=user_id, message=f"Value of steps: {steps}", random_id=0)
                            print (steps)
                            continue
                        else:
                            vk.messages.send(user_id=user_id, message="К сожалению, в данный момент только администратор имеет возможность изменить данную функцию. \
                            Однако, если вам необходима эта функция, вы можете рассмотреть возможность перехода на платный тариф. Мы всегда готовы помочь в выборе оптимального решения для вас.", random_id=0)

                    if message == 'инфо_бот':
                        # Проверка, является ли пользователь администратором
                        user_admin = cursor.execute('SELECT admin FROM users WHERE id=?', (user_id,)).fetchone()
                        if user_admin is not None and user_admin[0] == 1:
                            # получаем информацию о всех пользователях
                            all_users = cursor.execute('SELECT name, "limit", gen_limit FROM users').fetchall()
                            # формируем строку с информацией о пользователях
                            users_info = '\n'.join([f"{name}: лимит: {limit}, лимит на генерацию: {gen_limit}" for name, limit, gen_limit in all_users])
                            # получаем количество пользователей
                            users_count = cursor.execute('SELECT COUNT(*) FROM users').fetchone()[0]
                            # формируем сообщение
                            message_text = f"В базе данных {users_count} пользователей:\n{users_info}"
                            # отправляем сообщение
                            vk.messages.send(user_id=event.user_id, message=message_text, random_id=0)



                    if message == 'лог_инфо':
                        # Проверка, является ли пользователь администратором
                        user_admin = cursor.execute('SELECT admin FROM users WHERE id=?', (user_id,)).fetchone()
                        if user_admin is not None and user_admin[0] == 1:
                            with open('bot.csv', 'r') as f:
                                # Собираем строки начинающиеся с "INFO" в одну строку
                                info_lines = ''.join(line for line in f if line.startswith('INFO'))
                            # Отправляем пользователю
                            
                            vk.messages.send(user_id=event.user_id, message=info_lines, random_id=0)

                    if message == 'удалить_логи':
                        # Проверка, является ли пользователь администратором
                        user_admin = cursor.execute('SELECT admin FROM users WHERE id=?', (user_id,)).fetchone()
                        if user_admin is not None and user_admin[0] == 1:
                            with open('bot.csv', 'w') as f:
                                f.truncate(0)
                            vk.messages.send(user_id=event.user_id, message="Все логи были удалены!", random_id=0)

                    if message.startswith('set_limit '):
                        # изменяем лимит у пользователя по имени
                        command = message.split()
                        if len(command) != 4:
                            # выводим сообщение об ошибке, если команда некорректна
                            vk.messages.send(user_id=user_id, message="Некорректный формат команды.",random_id=0)
                        else:
                            user_name = f"{command[1]} {command[2]}"
                            new_limit = int(command[3])
                            message_text = set_user_gen_limit(user_name, new_limit)
                            vk.messages.send(user_id=user_id, message=message_text,random_id=0)
                            
                    if message == 'admin_help':
                        # Проверка, является ли пользователь администратором
                        user_admin = cursor.execute('SELECT admin FROM users WHERE id=?', (user_id,)).fetchone()
                        if user_admin is not None and user_admin[0] == 1:
                            vk.messages.send(user_id=user_id, message="(set_limit) - это функция, которая позволяет изменить лимит для конкретного пользователя. \
                        Например, чтобы установить лимит для Герман Келлер на 50, можно использовать следующий синтаксис: (set_limit Герман Келлер 50). \
                        Эта функция может быть полезна, если вы хотите ограничить количество действий или использования для конкретного пользователя. \Надеюсь, эта информация будет для вас полезной!\
                         (инфо_бот) - это функция, которая помогает вам просмотреть информацию о пользователях, зарегистрированных в базе данных. \
                         Кроме того, она также позволяет вам просмотреть лимиты, установленные для каждого пользователя. \
                         Это может быть полезно, если вы хотите оценить активность пользователей или выяснить, какой пользователь использует большую часть своего лимита. \
                         Используйте (инфо_бот) для более детального понимания активности пользователей в вашей базе данных!\
                         лог_инфо - выводит все логи с тегом INFO.\
                         удалить_логи - очищает файл формата CSV со всеми логами бота.", random_id=0)
                        else:
                            vk.messages.send(user_id=event.user_id, message="К сожалению, доступ к этой функции предоставлен только администраторам", random_id=0)
                            


                            

                    
                    if message.lower().startswith("help"):
                        vk.messages.send(user_id=event.user_id, message=("Наш бот имеет две доступные команды:  'gen' и 'ии'.\
                        Команда 'gen' запускает процесс генерации картинки с заданным количеством шагов. Наш бот выполнит все необходимые действия и сгенерирует картинку для вас.\
                        Также, у нас есть функция искусственного интеллекта и обычный чат-бот с использованием GPT. Просто напишите в начале своего сообщения 'ии',\
                        и наш чат-бот ответит на ваши вопросы и запросы, используя передовые технологии искусственного интеллекта и GPT. "), random_id=0)

                    if message.lower().startswith("ии"):
                        message = event.text
                        print(message)
                        # Генерируем ответ с помощью GPT-3
                        response = generate_response(promptGPT=message)
                        # Отправляем сгенерированный ответ
                        vk.messages.send(user_id=event.user_id, message=response, random_id=0)
                        continue
#########################################

                    if message.startswith("test"):
                        response_tu=gen_promt(promptGPT=message)
                        print(response_tu)
                        generet_img_group(response_tu)
                        repost_vk_group()
                        
                    if "repost_vk" in message.lower():
                        generet(message,steps)
                        repost_vk_name(user_name)
                            


########################################                    


                    if "gen" in message.lower():
                        if user_limits[3] is not None and user_limits[3] > 0:
                            # пользователь еще не исчерпал свой лимит для функции gen
                            vk.messages.send(user_id=event.user_id, message="Время генерации может составлять от 1 до 4 минут, \
                            в зависимости от текущей загрузки. Мы делаем все возможное, чтобы обеспечить быструю и эффективную работу генератора для Вас. Благодарим за понимание!", random_id=0)
                            generet(message,steps)
                            send_photo(event, user_id, user_limits )


                        else:
                            # пользователь уже исчерпал свой лимит и время игнорирования еще не истекло
                            vk.messages.send(user_id=event.user_id, message="К сожалению, Ваш лимит исчерпан, но не переживайте!\
                                        Вы можете приобрести 30 дополнительных генераций всего за 50 рублей. Обратитесь к https://vk.com/sasha99199, \
                                        чтобы совершить покупку. Мы всегда готовы помочь Вам получить необходимые ресурсы для продолжения работы.", random_id=0)



                            # уменьшаем лимит пользователя для gen
                            cursor.execute('UPDATE users SET gen_limit=? WHERE id=?', (user_limits[3] - 1, user_id))
                            conn.commit()          


                    if "dalle" in message.lower():
                        prompt=message
                        image_url = dalle_ai(message,event, user_id,prompt)
                        send_dalle(message, event, user_id,image_url)


        
    except Exception as e:
        print ("An error occurred:", e)
        




