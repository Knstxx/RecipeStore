from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=32,
                            null=False, blank=False)
    slug = models.SlugField(max_length=32, unique=True,
                            null=False, blank=False)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=128, unique=True,
                            null=False, blank=False)
    measurement_unit = models.CharField(max_length=64,
                                        null=False, blank=False)

    class Meta:
        verbose_name = 'Ингредиент '
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
