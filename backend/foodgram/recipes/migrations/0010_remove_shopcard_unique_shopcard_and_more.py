# Generated by Django 4.2.15 on 2024-08-08 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0009_shopcard_shopcard_unique_shopcard'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='shopcard',
            name='unique_shopcard',
        ),
        migrations.AlterField(
            model_name='shopcard',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inshop_cart', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='shopcard',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inshop_cart', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddConstraint(
            model_name='shopcard',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopcart'),
        ),
    ]
