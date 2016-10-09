# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_themes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='theme',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
