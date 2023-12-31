from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Reaction


@receiver(post_save, sender=Reaction)
def send_notification_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Отклик на ваше объявление'
        message = f'Здравствуйте!\n\nНа ваше объявление "{instance.post}" появился новый отклик.\n\nС уважением сайт MMORPG.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.post.user.email]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Reaction)
def send_accepted_email(sender, instance, **kwargs):
    if instance.accepted:
        subject = 'Ваш отклик принят'
        message = f'Здравствуйте!\n\nВаш отклик "{instance.text[:15]}" принят.\n\nС уважением,\nВаш сайт MMORPG.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

        send_mail(subject, message, from_email, recipient_list)


@receiver(post_save, sender=Reaction)
def send_reject_email(sender, instance, **kwargs):
    if not instance.accepted:
        subject = 'Ваш отклик отклонен'
        message = f'Здравствуйте!\n\nВаш отклик "{instance.text[:15]}" отклонен.\n\nС уважением,\nВаш сайт MMORPG.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.user.email]

        send_mail(subject, message, from_email, recipient_list)
