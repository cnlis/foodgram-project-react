from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    AbstractUser
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(_('Имя'), max_length=150)
    last_name = models.CharField(_('Фамилия'), max_length=150)
    email = models.EmailField(_('Адрес электронной почты'))
    password = models.CharField(_('Пароль'), max_length=150)

    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Subscribe(models.Model):
    user = models.ForeignKey(
        User,
        related_name='subscriber',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['user', 'author'],
                name='unique_follow'
            ),
            CheckConstraint(
                check=~models.Q(user=models.F('author')),
                name='check_self_follow'
            ),
        ]

    def __str__(self):
        return f'{self.user} subscribed to {self.author}'
