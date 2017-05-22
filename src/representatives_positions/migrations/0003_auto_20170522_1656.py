# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_positions', '0002_multi_rep_positions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='kind',
            field=models.CharField(default=b'other', max_length=64, choices=[(b'other', b'Other'), (b'blog', b'Blog post'), (b'social', b'Social network'), (b'press', b'Press interview'), (b'parliament', b'Parliament debate'), (b'amendment', b'Amendment')]),
        ),
    ]
