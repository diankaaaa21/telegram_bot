import logging

import telebot
from django.conf import settings

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
logger = logging.getLogger(__name__)


def send_admin_login_notification(username, login_time):
    from .models import TelegramSubscriber

    message = f"Успешный вход в админку\nДата: {login_time.strftime('%Y-%m-%d %H:%M:%S')}\nПользователь: {username}"
    subscribers = TelegramSubscriber.objects.all()

    for subscriber in subscribers:
        try:
            bot.send_message(subscriber.chat_id, message)
            logger.info(f"Уведомление отправлено {subscriber.chat_id}")
        except Exception as e:
            logger.error(f"Ошибка отправки для {subscriber.chat_id}: {e}")
