import requests
import logging

class YandexGPT:
    def __init__(self, iam_token, folder_id):
        self.iam_token = iam_token
        self.folder_id = folder_id
        self.headers = {
            'Authorization': f'Bearer {self.iam_token}',
            'Content-Type': 'application/json'
        }
        self.url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def ask(self, text):
        data = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.6,
                "maxTokens": 200
            },
            "messages": [
                {
                    "role": "user",
                    "text": text
                }
            ]
        }
        response = requests.post(self.url, headers=self.headers, json=data)
        if response.status_code == 200:
            try:
                response_json = response.json()
                choices = response_json.get('choices', [])
                if choices:
                    return choices[0].get('text', 'Ошибка: в ответе отсутствует текст ответа.')
                else:
                    return "Ошибка: в ответе отсутствуют данные выбора текста."
            except ValueError as e:
                return f"Ошибка при разборе JSON-ответа: {e}"
        else:
            return f"Ошибка: {response.status_code} {response.text}"