import requests

class SpeechKit:
    def __init__(self, iam_token, folder_id):
        self.iam_token = iam_token
        self.folder_id = folder_id
        self.headers = {
            'Authorization': f'Bearer {self.iam_token}',
        }

    def text_to_speech(self, text):
        data = {
            'text': text,
            'lang': 'ru-RU',
            'voice': 'filipp',
            'folderId': self.folder_id,
        }
        response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=self.headers, data=data)
        if response.status_code == 200:
            return response.content
        else:
            return None


    def handle_message(self, message):
        user_id = message.from_user.id
        if message.voice:
            # обработка голосового сообщения
            voice_file_info = self.bot.get_file(message.voice.file_id)
            voice_file = self.bot.download_file(voice_file_info.file_path)
            text = self.speechkit.recognize(voice_file)
            if not text:
                self.bot.reply_to(message, "Ошибка при распознавании голоса.")
                return
            response = self.gpt.ask(text)
            if response:
                self.bot.reply_to(message, response)
            else:
                self.bot.reply_to(message, "Не удалось получить ответ от модели.")
        elif message.text.startswith("/ask"):
            # обработка текстового запроса
            question = message.text[5:].strip()
            response = self.gpt.ask(question)
            self.bot.reply_to(message, response)
        elif message.text == "/start":
            # обработка старта бота
            self.bot.reply_to(message, "Привет! Я могу отвечать на ваши вопросы. Напишите /ask [вопрос].")

    def recognize(self, voice_file):
        # загрузите файл аудио
        r = requests.post('https://speechkit.ai/api/v1/asr', files={'file': voice_file})
        if r.status_code == 200:
            return r.json()['text']
        else:
            return None
