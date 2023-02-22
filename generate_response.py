import openai

# Функция для генерации ответа с помощью GPT-3 
def generate_response(promptGPT):
    # Отправляем запрос на генерацию текста с помощью GPT-3
    response = openai.Completion.create(engine="text-davinci-003", prompt=promptGPT, max_tokens=1024, n=1,stop=None,temperature=0.5)
    # Получаем сгенерированный текст
    response_text = response['choices'][0]['text']
    return response_text
