# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='chamber',
            field=models.ForeignKey(related_name='documents', to='representatives.Chamber'),
        ),
    ]
