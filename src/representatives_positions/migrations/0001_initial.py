# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateField()),
                ('kind', models.CharField(default=b'other', max_length=64, choices=[(b'other', b'Other'), (b'blog', b'Blog post'), (b'social', b'Social network'), (b'press', b'Press interview'), (b'parliament', b'Parliament debate')])),
                ('title', models.CharField(max_length=500, null=True)),
                ('text', models.TextField()),
                ('link', models.URLField(max_length=500)),
                ('score', models.IntegerField(default=0)),
                ('published', models.BooleanField(default=False)),
                ('representative', models.ForeignKey(related_name='positions', to='representatives.Representative')),
            ],
        ),
    ]
