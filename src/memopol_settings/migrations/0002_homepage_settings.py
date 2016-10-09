# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core import serializers
from django.db import migrations, models


fixture_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../fixtures'))
fixture_filename = 'homepage_settings.json'


def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, fixture_filename)

    fixture = open(fixture_file, 'rb')
    objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
    for obj in objects:
        obj.save()
    fixture.close()


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_settings', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_fixture),
    ]
