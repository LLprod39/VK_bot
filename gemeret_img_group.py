from googletrans import Translator
import requests
import io
import base64
from PIL import Image, PngImagePlugin

name_img_post = ("ЕБАТЬ КАРТИНКА")
# Генерация картинки с API через SD
def generet_img_group(response_tu):
    print ("Это промт гена если че"+response_tu)
 
    # Подключение к ВЕБ SD применение настроек и генерация
    url = "http://127.0.0.1:7860"
    payload = {
        "prompt": response_tu,
        "steps": 50,
        "restore_faces": True,
        "negative_prompt": "ugly face, ugly body, ugly eyes,ugly mouth, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, bad-hands-5",
        }
    

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()
    # Сохранение изоброжение
    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))


        png_payload = {
        "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save(f'{name_img_post}.png', pnginfo=pnginfo)
