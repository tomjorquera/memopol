# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.core import serializers
from django.db import migrations, models


fixture_dir = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        '../fixtures'))
fixture_filename = 'country_initial_data.json'


def load_fixture(apps, schema_editor):
    fixture_file = os.path.join(fixture_dir, fixture_filename)

    fixture = open(fixture_file, 'rb')
    objects = serializers.deserialize('json', fixture, ignorenonexistent=True)
    for obj in objects:
        obj.save()
    fixture.close()


def unload_fixture(apps, schema_editor):
    "Brutally deleting all entries for this model..."

    MyModel = apps.get_model("representatives", "Country")
    MyModel.objects.all().delete()


def create_ep_chamber(apps, schema_editor):
    name = 'European Parliament'
    abbr = 'EP'

    Chamber = apps.get_model("representatives", "Chamber")
    Constituency = apps.get_model("representatives", "Constituency")
    Group = apps.get_model("representatives", "Group")

    ep_chamber, _ = Chamber.objects.get_or_create(name=name, abbreviation=abbr)
    ep_constituency, _ = Constituency.objects.get_or_create(name=name)
    ep_group, _ = Group.objects.get_or_create(name=name, kind='chamber',
        abbreviation=abbr, chamber=ep_chamber)

    ep_chamber.save()
    ep_constituency.save()
    ep_group.save()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('city', models.CharField(default=b'', max_length=255, blank=True)),
                ('street', models.CharField(default=b'', max_length=255, blank=True)),
                ('number', models.CharField(default=b'', max_length=255, blank=True)),
                ('postcode', models.CharField(default=b'', max_length=255, blank=True)),
                ('floor', models.CharField(default=b'', max_length=255, blank=True)),
                ('office_number', models.CharField(default=b'', max_length=255, blank=True)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
                ('name', models.CharField(default=b'', max_length=255, blank=True)),
                ('location', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Chamber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('abbreviation', models.CharField(default=b'', max_length=10, db_index=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Constituency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(unique=True, max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(max_length=254)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=511, db_index=True)),
                ('abbreviation', models.CharField(default=b'', max_length=10, db_index=True, blank=True)),
                ('kind', models.CharField(max_length=255, db_index=True)),
                ('chamber', models.ForeignKey(related_name='groups', to='representatives.Chamber', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Mandate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('role', models.CharField(default=b'', help_text=b'Eg.: president of a political group', max_length=255, blank=True)),
                ('begin_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('link', models.URLField()),
                ('constituency', models.ForeignKey(related_name='mandates', to='representatives.Constituency', null=True)),
                ('group', models.ForeignKey(related_name='mandates', to='representatives.Group', null=True)),
            ],
            options={
                'ordering': ('-end_date',),
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('number', models.CharField(default=b'', max_length=255, blank=True)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
                ('address', models.ForeignKey(related_name='phones', to='representatives.Address', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True, max_length=100)),
                ('first_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('last_name', models.CharField(default=b'', max_length=255, blank=True)),
                ('full_name', models.CharField(max_length=255)),
                ('gender', models.SmallIntegerField(default=0, choices=[(0, b'N/A'), (1, b'F'), (2, b'M')])),
                ('birth_place', models.CharField(default=b'', max_length=255, blank=True)),
                ('birth_date', models.DateField(null=True, blank=True)),
                ('cv', models.TextField(default=b'', blank=True)),
                ('photo', models.CharField(max_length=512, null=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['last_name', 'first_name'],
            },
        ),
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('url', models.CharField(default=b'', max_length=2048, blank=True)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
                ('representative', models.ForeignKey(to='representatives.Representative')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='phone',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
        ),
        migrations.AddField(
            model_name='mandate',
            name='representative',
            field=models.ForeignKey(related_name='mandates', to='representatives.Representative'),
        ),
        migrations.AddField(
            model_name='email',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
        ),
        migrations.AddField(
            model_name='constituency',
            name='country',
            field=models.ForeignKey(related_name='constituencies', blank=True, to='representatives.Country', null=True),
        ),
        migrations.AddField(
            model_name='chamber',
            name='country',
            field=models.ForeignKey(related_name='chambers', to='representatives.Country', null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(to='representatives.Country'),
        ),
        migrations.AddField(
            model_name='address',
            name='representative',
            field=models.ForeignKey(to='representatives.Representative'),
        ),

        migrations.RunPython(load_fixture, reverse_code=unload_fixture),

        migrations.RunPython(create_ep_chamber),
    ]
