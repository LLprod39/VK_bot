from googletrans import Translator
import requests
import io
import base64
from PIL import Image, PngImagePlugin


opis=("PhotoGeneret")

# Генерация картинки с API через SD
def generet(message,steps,):
    texte = message
    words = texte.split()
    text = " ".join(words[1:])
    print(text)
    
    translator = Translator()
    translated_text = translator.translate(text, dest='en').text
    promt = translated_text

    print ("описание картинки "+promt)

    # Подключение к ВЕБ SD применение настроек и генерация
    url = "http://127.0.0.1:7860"
    payload = {
        "prompt": promt,
        "steps": steps,
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
        image.save(f'{opis}.png', pnginfo=pnginfo)
