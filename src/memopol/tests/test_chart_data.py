from .base import BaseTest


class ChartViewsTest(BaseTest):
    def test_theme_score(self):
        url = '/charts/data/theme-scores/1/'
        self.request_test(url)

    def test_chamber_score(self):
        url = '/charts/data/chamber-scores/1/'
        self.request_test(url)

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
