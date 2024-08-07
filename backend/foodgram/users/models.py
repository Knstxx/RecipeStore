from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db.models import UniqueConstraint


class User(AbstractUser):
    email = models.EmailField('Email', unique=True, max_length=254)
    username = models.CharField('Никнейм', max_length=150,
                                null=False, blank=False)
    first_name = models.CharField('Имя', max_length=150,
                                  null=False, blank=False)
    last_name = models.CharField('Фамилия', max_length=150,
                                 null=False, blank=False)
    avatar = models.ImageField(upload_to='avatar',
                               null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    groups = models.ManyToManyField(
        Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_permissions_set', blank=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


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
        ordering = ['-id']
        constraints = [
            UniqueConstraint(fields=['user', 'author'],
                             name='unique_subscription')
        ]
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
