from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now

from .telegram_bot import send_admin_login_notification


@receiver(user_logged_in)
def notify_admin_login(sender, request, user, **kwargs):
    if request.path.startswith("/admin/"):
        send_admin_login_notification(user.username, now())
