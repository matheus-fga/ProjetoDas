# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=photos.models.user_directory_path),
        ),
    ]
