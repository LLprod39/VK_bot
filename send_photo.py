import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import os
import requests
import time
import sqlite3
import shutil

vk_token = ("")
vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

# отправка фото пользователю после генерации
def send_photo(event, user_id,user_limits):
    # Загружаем картинку в альбом
    upload_response = vk.photos.getMessagesUploadServer()
    upload_url = upload_response['upload_url']
                            
    # укажите каталог, содержащий изображения
    picture_dir = 'D:\\aitest\\webui\\outputs\\txt2img-images\\vkbot'

    # получить список всех файлов в каталоге
    all_files = os.listdir(picture_dir )

    # отфильтруйте список, чтобы он содержал только файлы изображений
    picture_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg'))]

    # отсортируйте список по времени изменения, чтобы самая последняя добавленная картинка была первой
    picture_files.sort(key=lambda x: os.path.getmtime(os.path.join( picture_dir, x)), reverse=True)

        # отправить самую последнюю фотографию
    if picture_files:
        with open(os.path.join(picture_dir, picture_files[0]), 'rb') as f:
            files = {'photo': f}
            response = requests.post(upload_url, files=files)
            response_json = response.json()
            save_response = vk.photos.saveMessagesPhoto(**response_json)
            photo = save_response[0]
            photo_id = f'photo{photo["owner_id"]}_{photo["id"]}'
            vk.messages.send(user_id=event.user_id, attachment=photo_id, random_id=0)
            #vk.messages.send(user_id=event.user_id, message="Если Вам понравилась картинка, пожалуйста, поставьте + или - в зависимости от того, понравилась ли Вам картинка или нет. Спасибо!", random_id=0)
            # уменьшаем лимит пользователя для gen и устанавливаем время игнорирования на 5 минут
            cursor.execute('UPDATE users SET gen_limit=?, gen_ignore_time=? WHERE id=?', (user_limits[3] - 1, time.time() + 1*60, user_id))
            conn.commit()
            pass
 
                                
