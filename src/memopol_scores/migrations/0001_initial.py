# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memopol_settings', '0001_initial'),
        ('memopol_themes', '0001_initial'),
        ('representatives', '0001_initial'),
        ('representatives_votes', '0001_initial'),
        ('representatives_positions', '0001_initial'),
        ('representatives_recommendations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DossierScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('dossier', models.ForeignKey(to='representatives_votes.Dossier')),
                ('representative', models.ForeignKey(related_name='dossier_scores', to='representatives.Representative')),
            ],
        ),
        migrations.CreateModel(
            name='PositionScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('position', models.OneToOneField(related_name='position_score', to='representatives_positions.Position')),
            ],
        ),
        migrations.CreateModel(
            name='RepresentativeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('representative', models.OneToOneField(related_name='representative_score', to='representatives.Representative')),
            ],
        ),
        migrations.CreateModel(
            name='ThemeScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('representative', models.ForeignKey(related_name='theme_scores', to='representatives.Representative')),
                ('theme', models.ForeignKey(to='memopol_themes.Theme')),
            ],
        ),
        migrations.CreateModel(
            name='VoteScore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.FloatField()),
                ('vote', models.OneToOneField(related_name='vote_score', to='representatives_votes.Vote')),
            ],
        ),

        migrations.RunSQL(
            """
            CREATE FUNCTION decay_score(
                score NUMERIC,
                vote_date timestamp with time zone,
                decay_num NUMERIC,
                decay_denom NUMERIC,
                exponent NUMERIC,
                decimals integer)
            RETURNS NUMERIC AS $$
                SELECT ROUND(
                    CAST(
                        $1 * EXP(
                            GREATEST(
                                -700,
                                LEAST(
                                    700,
                                    -(($3 * EXTRACT(days FROM CURRENT_DATE - $2) / $4) ^ (2 * $5))
                                )
                            )
                        )
                        AS NUMERIC
                    ),
                    $6
                )
            $$ LANGUAGE SQL;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_vote_score"
            AS SELECT
                "representatives_votes_vote"."id" AS "vote_id",
                decay_score(
                    CAST(CASE
                        WHEN "representatives_votes_vote"."position"::text = "representatives_recommendations_recommendation"."recommendation"::text
                        THEN "representatives_recommendations_recommendation"."weight"
                        ELSE 0 - "representatives_recommendations_recommendation"."weight"
                    END AS NUMERIC),
                    "representatives_votes_proposal"."datetime",
                    "decay_num"."value",
                    "decay_denom"."value",
                    "exponent"."value",
                    "decimals"."value"
                ) AS "score"
            FROM "representatives_votes_vote"
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECAY_NUM') "decay_num" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECAY_DENOM') "decay_denom" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_EXPONENT') "exponent" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS INTEGER) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECIMALS') "decimals" ON 1=1
                JOIN "representatives_votes_proposal" ON "representatives_votes_vote"."proposal_id" = "representatives_votes_proposal"."id"
                LEFT JOIN "representatives_recommendations_recommendation" ON "representatives_votes_proposal"."id" = "representatives_recommendations_recommendation"."proposal_id"
            WHERE "representatives_recommendations_recommendation"."id" IS NOT NULL;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_dossier_score"
            AS SELECT
                "representatives_votes_vote"."representative_id" AS "representative_id",
                "representatives_votes_proposal"."dossier_id" AS "dossier_id",
                SUM("memopol_scores_votescore"."score") AS "score"
            FROM
                "memopol_scores_votescore"
                INNER JOIN "representatives_votes_vote"
                    ON "memopol_scores_votescore"."vote_id" = "representatives_votes_vote"."id"
                INNER JOIN "representatives_votes_proposal"
                    ON "representatives_votes_vote"."proposal_id" = "representatives_votes_proposal"."id"
            GROUP BY
                "representatives_votes_vote"."representative_id",
                "representatives_votes_proposal"."dossier_id"
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_position_score"
            AS SELECT
                "representatives_positions_position"."id" AS "position_id",
                decay_score(
                    "representatives_positions_position"."score",
                    "representatives_positions_position"."datetime",
                    "decay_num"."value",
                    "decay_denom"."value",
                    "exponent"."value",
                    "decimals"."value"
                ) AS "score"
            FROM
                "representatives_positions_position"
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECAY_NUM') "decay_num" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECAY_DENOM') "decay_denom" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS NUMERIC) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_EXPONENT') "exponent" ON 1=1
                JOIN (SELECT CAST(TO_NUMBER("value", '99999') AS INTEGER) AS "value" FROM "memopol_settings_setting" WHERE "key" = 'SCORE_DECIMALS') "decimals" ON 1=1;
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_representative_score"
            AS SELECT
                "source"."representative_id" AS "representative_id" ,
                SUM("source"."score") AS "score"
            FROM
                (
                    SELECT
                        "memopol_scores_dossierscore"."representative_id" AS "representative_id",
                        "memopol_scores_dossierscore"."score" AS "score"
                    FROM "memopol_scores_dossierscore"
                    UNION ALL
                    SELECT
                        "representatives_positions_position"."representative_id" AS "representative_id",
                        "memopol_scores_positionscore"."score" AS "score"
                    FROM
                        "memopol_scores_positionscore"
                        INNER JOIN "representatives_positions_position"
                            ON "memopol_scores_positionscore"."position_id" = "representatives_positions_position"."id"
                ) "source"
            GROUP BY
                "source"."representative_id"
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE VIEW "memopol_scores_v_theme_score"
            AS SELECT
                "scoresource"."representative_id" AS "representative_id",
                "scoresource"."theme_id" AS "theme_id",
                SUM("scoresource"."score") AS "score"
            FROM
                (
                    -- Score contribution for proposals
                    SELECT
                        "representatives_votes_vote"."representative_id" AS "representative_id",
                        "proposal_themes"."theme_id" AS "theme_id",
                        "memopol_scores_votescore"."score" AS "score"
                    FROM
                        "memopol_scores_votescore"
                        INNER JOIN "representatives_votes_vote"
                            ON "representatives_votes_vote"."id" = "memopol_scores_votescore"."vote_id"
                        INNER JOIN (
                                -- Proposals with a theme
                                SELECT
                                    "representatives_votes_proposal"."id" AS "proposal_id",
                                    "memopol_themes_theme_proposals"."theme_id" AS "theme_id"
                                FROM
                                    "representatives_votes_proposal"
                                    INNER JOIN "memopol_themes_theme_proposals"
                                        ON "representatives_votes_proposal"."id" = "memopol_themes_theme_proposals"."proposal_id"
                                UNION
                                -- Proposals in a dossier with a theme
                                SELECT
                                    "representatives_votes_proposal"."id" AS "proposal_id",
                                    "memopol_themes_theme_dossiers"."theme_id" AS "theme_id"
                                FROM
                                    "representatives_votes_proposal"
                                    INNER JOIN "representatives_votes_dossier"
                                        ON "representatives_votes_dossier"."id" = "representatives_votes_proposal"."dossier_id"
                                    INNER JOIN "memopol_themes_theme_dossiers"
                                        ON "memopol_themes_theme_dossiers"."dossier_id" = "representatives_votes_dossier"."id"
                            ) "proposal_themes"
                            ON "proposal_themes"."proposal_id" = "representatives_votes_vote"."proposal_id"
                    UNION ALL
                    -- Score contribution for positions
                    SELECT
                        "representatives_positions_position"."representative_id" AS "representative_id",
                        "memopol_themes_theme_positions"."theme_id" AS "theme_id",
                        "memopol_scores_positionscore"."score" AS "score"
                    FROM
                        "memopol_scores_positionscore"
                        INNER JOIN "representatives_positions_position"
                            ON "representatives_positions_position"."id" = "memopol_scores_positionscore"."position_id"
                        INNER JOIN "memopol_themes_theme_positions"
                            ON "memopol_themes_theme_positions"."position_id" = "memopol_scores_positionscore"."position_id"
                ) "scoresource"
            GROUP BY
                "scoresource"."representative_id",
                "scoresource"."theme_id"
            """
        ),

        migrations.RunSQL(
            """
            CREATE OR REPLACE FUNCTION refresh_scores()
            RETURNS VOID AS $$
            BEGIN
                TRUNCATE TABLE "memopol_scores_representativescore";

                TRUNCATE TABLE "memopol_scores_dossierscore";

                TRUNCATE TABLE "memopol_scores_votescore";

                INSERT INTO "memopol_scores_votescore" ("vote_id", "score")
                SELECT "vote_id", "score" FROM "memopol_scores_v_vote_score";

                INSERT INTO "memopol_scores_dossierscore" ("representative_id", "dossier_id", "score")
                SELECT "representative_id", "dossier_id", "score" FROM "memopol_scores_v_dossier_score";

                TRUNCATE TABLE "memopol_scores_positionscore";

                INSERT INTO "memopol_scores_positionscore" ("position_id", "score")
                SELECT "position_id", "score" FROM "memopol_scores_v_position_score";

                TRUNCATE TABLE "memopol_scores_themescore";

                INSERT INTO "memopol_scores_themescore" ("representative_id", "theme_id", "score")
                SELECT
                    "representatives_representative"."id",
                    "memopol_themes_theme"."id",
                    COALESCE("memopol_scores_v_theme_score"."score", 0)
                FROM
                    "representatives_representative"
                    INNER JOIN "memopol_themes_theme" ON 1=1
                    LEFT OUTER JOIN "memopol_scores_v_theme_score"
                        ON "memopol_scores_v_theme_score"."representative_id" = "representatives_representative"."id"
                        AND "memopol_scores_v_theme_score"."theme_id" = "memopol_themes_theme"."id";

                INSERT INTO "memopol_scores_representativescore" ("representative_id", "score")
                SELECT
                    "representatives_representative"."id",
                    COALESCE("memopol_scores_v_representative_score"."score", 0)
                FROM
                    "representatives_representative"
                    LEFT OUTER JOIN "memopol_scores_v_representative_score"
                        ON "memopol_scores_v_representative_score"."representative_id" = "representatives_representative"."id";
            END;
            $$ LANGUAGE PLPGSQL;
            """
        ),

        migrations.RunSQL(
            """
            SELECT refresh_scores();
            """
        )
    ]
