import json

from .base import BaseTest


class ChartViewsTest(BaseTest):
    def test_theme_score(self):
        url = '/charts/data/theme-scores/1/'

        data = json.loads(self.client.get(url).content)
        expected = {
            "theme": "Etat d'urgence",
            "scores": [-305.0, -305.0, -265.0, -235.0, -220.0, -215.0, -205.0,
                       -205.0, -195.0, -195.0, -190.0, -185.0, -135.0, -115.0,
                       -110.0, -105.0, -100.0, -100.0, -100.0, -90.0, -90.0,
                       -90.0, -90.0, -55.0, -25.0, -5.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 35.0]
        }

        assert data == expected

    def test_chamber_score(self):
        url = '/charts/data/chamber-scores/1/'

        data = json.loads(self.client.get(url).content)
        expected = {
            "chamber": "European Parliament",
            "scores": [-1312.0, -1216.0, -1216.0, -1216.0, -1216.0, -1216.0,
                       -1216.0, -1208.0, -1200.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1208.0,
                       1224.0, 1468.0, 1468.0, 1480.0]
        }

        assert data == expected

    def test_theme_score_queries(self):
        url = '/charts/data/theme-scores/1/'

        # First query to set session variables
        self.client.get(url)

        with self.assertNumQueries(2):
            # 1 query for the theme
            # 1 query for theme scores
            self.client.get(url)

    def test_chamber_score_queries(self):
        url = '/charts/data/chamber-scores/1/'

        # First query to set session variables
        self.client.get(url)

        with self.assertNumQueries(2):
            # 1 query for the chamber
            # 1 query for chamber scores
            self.client.get(url)
