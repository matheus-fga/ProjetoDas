# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('photos', '0002_auto_20161201_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='user',
            field=models.ForeignKey(default=3, to=settings.AUTH_USER_MODEL),
        ),
    ]
