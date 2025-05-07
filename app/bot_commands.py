from django.conf import settings

from .models import TelegramSubscriber

bot = settings.TELEGRAM_BOT


@bot.message_handler(commands=["start", "subscribe"])
def subscribe(message):
    chat_id = message.chat.id
    if not TelegramSubscriber.objects.filter(chat_id=chat_id).exists():
        TelegramSubscriber.objects.create(chat_id=chat_id)
        bot.send_message(chat_id, "Вы успешно подписались на уведомления!")
    else:
        bot.send_message(chat_id, "Вы уже подписаны.")
