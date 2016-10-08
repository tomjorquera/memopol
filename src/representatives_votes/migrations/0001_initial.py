# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('representatives', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=1000)),
                ('kind', models.CharField(default=b'', max_length=255, blank=True)),
                ('link', models.URLField(max_length=1000)),
                ('chamber', models.ForeignKey(to='representatives.Chamber')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Dossier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=1000)),
                ('reference', models.CharField(unique=True, max_length=200)),
                ('text', models.TextField(default=b'', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Proposal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(unique=True, max_length=1000)),
                ('description', models.TextField(default=b'', blank=True)),
                ('reference', models.CharField(max_length=200, null=True, blank=True)),
                ('datetime', models.DateTimeField(db_index=True)),
                ('kind', models.CharField(default=b'', max_length=200, blank=True)),
                ('total_abstain', models.IntegerField()),
                ('total_against', models.IntegerField()),
                ('total_for', models.IntegerField()),
                ('dossier', models.ForeignKey(related_name='proposals', to='representatives_votes.Dossier')),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('representative_name', models.CharField(max_length=200, blank=True)),
                ('position', models.CharField(max_length=10, choices=[(b'abstain', b'abstain'), (b'for', b'for'), (b'against', b'against')])),
                ('proposal', models.ForeignKey(related_name='votes', to='representatives_votes.Proposal')),
                ('representative', models.ForeignKey(related_name='votes', to='representatives.Representative', null=True)),
            ],
            options={
                'ordering': ['proposal__datetime'],
            },
        ),
        migrations.AddField(
            model_name='proposal',
            name='representatives',
            field=models.ManyToManyField(related_name='proposals', through='representatives_votes.Vote', to='representatives.Representative'),
        ),
        migrations.AlterUniqueTogether(
            name='dossier',
            unique_together=set([('title', 'reference')]),
        ),
        migrations.AddField(
            model_name='document',
            name='dossier',
            field=models.ForeignKey(related_name='documents', to='representatives_votes.Dossier'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('proposal', 'representative')]),
        ),
        migrations.AlterUniqueTogether(
            name='proposal',
            unique_together=set([('dossier', 'title', 'reference', 'kind', 'total_abstain', 'total_against', 'total_for')]),
        ),
    ]
