from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.conf import settings


tanks = 'TNK'
hils = 'HIL'
dd = 'DD'
merchants = 'MCH'
guild_masters = 'GMA'
quest_givers = 'QMA'
blacksmiths = 'BLM'
tanners = 'TAN'
potion_makers = 'PMK'
spell_masters = 'SMA'

CATEGORY = [
    (tanks, 'Танки'),
    (hils, 'Хилы'),
    (dd, 'ДД'),
    (merchants, 'Торговцы'),
    (guild_masters, 'Гилдмастеры'),
    (quest_givers, 'Квестгиверы'),
    (blacksmiths, 'Кузнецы'),
    (tanners, 'Кожевники'),
    (potion_makers, 'Зельевары'),
    (spell_masters, 'Мастера заклинаний'),
]


class Post(models.Model):
    CATEGORY = CATEGORY
    title = models.CharField(max_length=255)
    text = RichTextUploadingField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=3, choices=CATEGORY)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Reaction(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return self.text

    def send_notification_email(self):
        subject = 'Отклик на ваше объявление'
        message = f'Здравствуйте!\n\nНа ваше объявление "{self.post}" появился новый отклик.\n\nС уважением сайт MMORPG.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.post.user.email]

        send_mail(subject, message, from_email, recipient_list)

    def send_accepted_email(self):
        subject = 'Ваш отклик принят'
        message = f'Здравствуйте!\n\nВаш отклик "{self.text[:15]}" принят.\n\nС уважением,\nВаш сайт MMORPG.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.user.email]

        send_mail(subject, message, from_email, recipient_list)

    def send_reject_email(self):
        subject = 'Ваш отклик отклонен'
        message = f'Здравствуйте!\n\nВаш отклик "{self.text[:15]}" отклонен.\n\nС уважением,\nВаш сайт MMORPG.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [self.user.email]

        send_mail(subject, message, from_email, recipient_list)
