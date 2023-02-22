import openai
import random

openai_api_key = "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"
openai.api_key = openai_api_key

# Задаем текст, который будет использоваться для генерации
prompt = "generate a different photo description for dalle-2"

# Функция генерации текста
def gen_promt(promptGPT):
    # Отправляем запрос на генерацию текста с помощью GPT-3
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=1024, n=1,stop=None,temperature=0.5)
    # Получаем сгенерированный текст
    response_text = response['choices'][0]['text']
    # Извлекаем текст из ответа API
    text = response.choices[0].text.strip()
    print(text)
    return text

