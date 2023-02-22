import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import openai
import requests


vk_token = ("")
vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)


def send_dalle(message, event, user_id,image_url):                      
    # Скачиваем картинку и сохраняем ее в файл
    response = requests.get(image_url)
    open("cat.jpg", "wb").write(response.content)

    # Загружаем картинку в альбом
    upload_response = vk.photos.getMessagesUploadServer()
    upload_url = upload_response['upload_url']
    # Отправляем картинку на сервер загрузки
    with open('cat.jpg', 'rb') as f:
        files = {'photo': f}
        response = requests.post(upload_url, files=files)
        # Сохраняем картинку в альбом
        response_json = response.json()
        save_response = vk.photos.saveMessagesPhoto(**response_json)
        photo = save_response[0]
        photo_id = f'photo{photo["owner_id"]}_{photo["id"]}'

        # Отправляем сообщение с картинкой
        vk.messages.send(user_id=event.user_id, attachment=photo_id, random_id=0)
        print("Сгенерированая картинка отправлена")
