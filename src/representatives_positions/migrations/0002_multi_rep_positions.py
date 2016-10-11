# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def migrate_position_representatives(apps, schema_editor):

    Position = apps.get_model("representatives_positions", "Position")

    for pos in Position.objects.all():
        pos.representatives = [pos.representative]
        pos.save()


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_scores', '0002_pre_multi_rep_positions'),
        ('representatives_positions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='representatives',
            field=models.ManyToManyField(to='representatives.Representative'),
        ),

        migrations.RunPython(migrate_position_representatives),

        migrations.RemoveField(
            model_name='position',
            name='representative',
        ),

        migrations.AlterField(
            model_name='position',
            name='representatives',
            field=models.ManyToManyField(related_name='positions', to='representatives.Representative'),
        ),
    ]
