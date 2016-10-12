# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_scores', '0001_initial')
    ]

    operations = [
        migrations.RunSQL(
            """
            DROP FUNCTION refresh_scores();
            """
        ),

        migrations.RunSQL(
            """
            DROP VIEW memopol_scores_v_representative_score;
            """
        ),

        migrations.RunSQL(
            """
            DROP VIEW memopol_scores_v_theme_score;
            """
        ),
    ]
