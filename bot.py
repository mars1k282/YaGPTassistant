from database import Database
from validators import check_character_limit
from yandexGPT import YandexGPT
from speechkit import SpeechKit
import telebot

class TelegramBot:
    def __init__(self, token, folder_id, iam_token, db):
        self.token = token
        self.folder_id = folder_id
        self.iam_token = iam_token
        self.db = db
        self.bot = telebot.TeleBot(token)
        self.gpt = YandexGPT(iam_token, folder_id)  # Инициализация YandexGPT
        self.speechkit = SpeechKit(iam_token, folder_id)  # Инициализация SpeechKit

    def handle_message(self, message):
        user_id = message.from_user.id

        if message.voice:
            voice_file_info = self.bot.get_file(message.voice.file_id)
            voice_file = self.bot.download_file(voice_file_info.file_path)
            text = self.speechkit.recognize(voice_file)
            if not text:
                self.bot.reply_to(message, "Ошибка при распознавании голоса.")
                return
            self.bot.reply_to(message, "Текст распознан: " + text)
            audio_data = self.speechkit.text_to_speech(text)
            if audio_data:
                self.bot.send_voice(user_id, audio_data)
            else:
                self.bot.reply_to(message, "Ошибка при создании аудио из текста.")

        elif message.text.startswith('/ask'):
            question = message.text[5:].strip()
            # Проверка токенов перенесена в YandexGPT
            response = self.gpt.ask(question)
            self.bot.reply_to(message, response)

        elif message.text == '/start':
            self.bot.reply_to(message, "Привет! Я могу отвечать на ваши вопросы. Напишите /ask [вопрос].")

    def run(self):
        @self.bot.message_handler(func=lambda message: True)
        def handler(message):
            try:
                self.handle_message(message)
            except Exception as e:
                self.bot.reply_to(message, f"Произошла ошибка: {e}")

        self.bot.polling()

if __name__ == '__main__':
    db = Database()
    token = ''
    folder_id = ''
    iam_token = ''
    bot = TelegramBot(token, folder_id, iam_token, db)
    bot.run()
