from django import test
from responsediff.test import ResponseDiffTestMixin
from memopol_scores.models import RepresentativeScore


class BaseTest(ResponseDiffTestMixin, test.TestCase):
    fixtures = ['data_sample.json']

    """
    Common queries
    - 1 for settings
    - 5 for search forms
        - 1 for chambers
        - 1 for countries
        - 1 for parties
        - 1 for committees
        - 1 for delegations
    """
    left_pane_queries = 6

    def setUp(self):
        RepresentativeScore.refresh()

    def request_test(self, url=None):
        self.assertResponseDiffEmpty(self.client.get(url or self.url))

    def selector_test(self, selector, url=None):
        self.assertResponseDiffEmpty(self.client.get(url or self.url),
                                     selector)


class RepresentativeBaseTest(BaseTest):
    tab = 'none'
    base_url = '/representatives/olivier-dussopt-1978-08-16/%s/'

    """
    Common queries plus:
    - 1 for session key
    - 1 for chamber abbreviations (helper for chamber websites)
    - 1 for the representative
    - 1 for the main mandate
    - 1 for emails
    - 1 for social websites
    - 1 for chamber websites
    - 1 for other websites
    - 1 for addresses
    - 2 for phone numbers related to addresses
    - 1 for other phone numbers
    - 2 for themes and theme scores
    - 1 for DAL to fetch its initial value in the position form
    """
    queries = BaseTest.left_pane_queries + 15

    @property
    def url(self):
        return self.base_url % self.tab

    def do_query_test(self):
        # First query to set session variables
        self.client.get(self.url)

        with self.assertNumQueries(self.queries):
            self.client.get(self.url)


class ThemeBaseTest(BaseTest):
    tab = 'none'
    base_url = '/themes/etat-durgence/%s/'

    """
    Common queries plus:
    - 1 for the theme
    - 1 for DAL to fetch its initial value in the position form
    """
    queries = BaseTest.left_pane_queries + 2

    @property
    def url(self):
        return self.base_url % self.tab

    def do_query_test(self):
        # First query to set session variables
        self.client.get(self.url)

        with self.assertNumQueries(self.queries):
            self.client.get(self.url)


class DossierBaseTest(BaseTest):
    tab = 'none'
    base_url = '/dossiers/15409/%s/'

    """
    Common queries plus:
    - 1 for the dossier
    - 1 for related themes
    """
    queries = BaseTest.left_pane_queries + 2

    @property
    def url(self):
        return self.base_url % self.tab

    def do_query_test(self):
        # First query to set session variables
        self.client.get(self.url)

        with self.assertNumQueries(self.queries):
            self.client.get(self.url)
