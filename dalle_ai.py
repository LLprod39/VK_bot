from googletrans import Translator
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import openai
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import openai
import requests

vk_token = ("vk1.a.mxEpwbhYSgGnpFgHcckzsynpF7KCCaYOzVSnVcbrfV_XohaDteWezoCS8hgGCZOPW_JMi1w2uoDdW25SYnGygtRXQeJfNDXLszRY1wLacY63CQ_h3Y2jdbriUp4a-AWd42jAw2IgxFH-y_sn36PLb5HyCYlOSVj8NcSg_uGBWqK7DB0q3h-KxCrCMc3K0dWNminmPhInw5d1igJAsB8lXA")
vk_session = vk_api.VkApi(token=vk_token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def dalle_ai(message,event, user_id,prompt):

    texte = message
    words = texte.split()
    text = " ".join(words[1:])
    print(text)
    translator = Translator()
    translated_text = translator.translate(text, dest='en').text
    promt = translated_text

    print(promt)
    # Отправляем запрос на генерацию картинки с помощью DALL-E
    response = openai.Image.create(prompt=promt,n=1)
    # Получаем URL генерированной картинки
    image_url = response['data'][0]['url']
    return image_url
