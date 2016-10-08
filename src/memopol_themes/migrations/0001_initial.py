# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('representatives_votes', '0001_initial'),
        ('representatives_positions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField(default=0)),
            ],
            options={
                'ordering': ['theme__slug'],
                'db_table': 'memopol_themes_themescore',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('slug', autoslug.fields.AutoSlugField(populate_from=b'name', editable=False)),
                ('description', models.TextField()),
                ('dossiers', models.ManyToManyField(related_name='themes', to='representatives_votes.Dossier')),
                ('positions', models.ManyToManyField(related_name='themes', to='representatives_positions.Position')),
                ('proposals', models.ManyToManyField(related_name='themes', to='representatives_votes.Proposal')),
            ],
        ),
        migrations.CreateModel(
            name='ThemeLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=511)),
                ('datetime', models.DateField()),
                ('link', models.URLField(max_length=500)),
                ('theme', models.ForeignKey(related_name='links', to='memopol_themes.Theme')),
            ],
        ),
    ]
