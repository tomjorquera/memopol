# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recommendation', models.CharField(max_length=10, choices=[(b'abstain', b'abstain'), (b'for', b'for'), (b'against', b'against')])),
                ('title', models.CharField(max_length=1000, blank=True)),
                ('description', models.TextField(blank=True)),
                ('weight', models.FloatField(default=0)),
                ('proposal', models.OneToOneField(related_name='recommendation', to='representatives_votes.Proposal')),
            ],
            options={
                'ordering': ['proposal__datetime'],
            },
        ),
    ]
