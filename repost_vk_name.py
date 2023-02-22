import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import time
import os
import requests
from vk_api.upload import VkUpload


vk_token = ("vk1.a.mxEpwbhYSgGnpFgHcckzsynpF7KCCaYOzVSnVcbrfV_XohaDteWezoCS8hgGCZOPW_JMi1w2uoDdW25SYnGygtRXQeJfNDXLszRY1wLacY63CQ_h3Y2jdbriUp4a-AWd42jAw2IgxFH-y_sn36PLb5HyCYlOSVj8NcSg_uGBWqK7DB0q3h-KxCrCMc3K0dWNminmPhInw5d1igJAsB8lXA")
vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

# отправка фото пользователю после генерации
def repost_vk_name(user_name):
    # укажите каталог, содержащий изображения
    picture_dir = 'D:\\aitest\\webui\\outputs\\txt2img-images\\vkbot'

    # получить список всех файлов в каталоге
    all_files = os.listdir(picture_dir)

    # отфильтруйте список, чтобы он содержал только файлы изображений
    picture_files = [f for f in all_files if f.endswith(('.png', '.jpg', '.jpeg'))]

    # отсортируйте список по времени изменения, чтобы самая последняя добавленная картинка была первой
    picture_files.sort(key=lambda x: os.path.getmtime(os.path.join(picture_dir, x)), reverse=True)

    # отправить самую последнюю фотографию
    if picture_files:
        upload = VkUpload(vk)
        try:
            photo = upload.photo_wall(picture_dir + '/' + picture_files[0])
        except VkApiError as e:
            print('Error:', e)
        else:
            photo = f'photo{photo[0]["owner_id"]}_{photo[0]["id"]}'
            # формируем параметры для поста
            post_params = {
                'owner_id': -218920636,  # ID группы, на стене которой будет опубликован пост
                'from_group': 1,         # флаг, указывающий, что пост будет опубликован от имени группы
                'message': 'Описание этой картины было созадно '+user_name,  # текст поста
                'attachments': photo     # прикрепленная фотография
            }
            # отправляем пост
            vk.wall.post(**post_params)
    else:
        print('No pictures found in the directory')
