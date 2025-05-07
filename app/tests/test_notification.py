import logging
import os
from unittest import TestCase
from unittest.mock import patch

import django
from django.utils.timezone import now

from app.models import TelegramSubscriber
from app.telegram_bot import send_admin_login_notification

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "telegram_project.settings")
django.setup()

logger = logging.getLogger(__name__)


class NotificationTestCase(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.login_time = now()
        self.formatted_date = self.login_time.strftime("%Y-%m-%d %H:%M:%S")

    @patch("app.telegram_bot.bot.send_message")
    def test_send_notification_single_subscriber(self, mock_send_message):
        subscriber = TelegramSubscriber.objects.create(chat_id=12345)

        send_admin_login_notification(self.username, self.login_time)

        mock_send_message.assert_called_once_with(
            subscriber.chat_id,
            f"Успешный вход в админку\nДата: {self.formatted_date}\nПользователь: {self.username}",
        )

    @patch("app.telegram_bot.bot.send_message")
    def test_send_notification_multiple_subscribers(self, mock_send_message):
        ids = [111, 222, 333]
        for i in ids:
            TelegramSubscriber.objects.create(chat_id=i)

        send_admin_login_notification(self.username, self.login_time)

        self.assertEqual(mock_send_message.call_count, len(ids))
        sent_ids = [call.args[0] for call in mock_send_message.call_args_list]
        self.assertCountEqual(sent_ids, ids)

    @patch("app.telegram_bot.bot.send_message")
    def test_no_subscribers_does_not_send(self, mock_send_message):
        send_admin_login_notification(self.username, self.login_time)
        mock_send_message.assert_not_called()

    @patch("app.telegram_bot.logger")
    @patch("app.telegram_bot.bot.send_message")
    def test_send_message_error_logged_and_continues(
        self, mock_send_message, mock_logger
    ):
        TelegramSubscriber.objects.create(chat_id=111)
        TelegramSubscriber.objects.create(chat_id=222)

        def side_effect(chat_id, message):
            if chat_id == 111:
                raise Exception("Simulated failure")
            return True

        mock_send_message.side_effect = side_effect

        send_admin_login_notification(self.username, self.login_time)

        self.assertEqual(mock_send_message.call_count, 2)
        mock_logger.error.assert_called_once()
        self.assertIn("Ошибка отправки", mock_logger.error.call_args[0][0])

    @patch("app.telegram_bot.bot.send_message")
    def test_message_format_includes_username_and_date(self, mock_send_message):
        TelegramSubscriber.objects.create(chat_id=12345)

        send_admin_login_notification(self.username, self.login_time)

        sent_message = mock_send_message.call_args[0][1]
        self.assertIn(self.username, sent_message)
        self.assertIn(self.formatted_date, sent_message)
