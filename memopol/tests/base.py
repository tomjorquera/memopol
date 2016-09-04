from django import test
from responsediff.test import ResponseDiffTestMixin


class BaseTest(ResponseDiffTestMixin, test.TestCase):
    fixtures = ['data_sample.json']

    """
    Common queries
    - 5 for search forms
        - 1 for chambers
        - 1 for countries
        - 1 for parties
        - 1 for committees
        - 1 for delegations
    - 2 for the position form
        - 1 for representatives
        - 1 for themes
    """
    left_pane_queries = 7

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
    - 1 for chamber abbreviations (helper for chamber websites)
    - 1 for the representative
    - 1 for the main mandate
    - 1 for emails
    - 1 for social websites
    - 1 for chamber websites
    - 1 for other websites
    - 1 for addresses
    - 1 for address country
    - 1 for phone numbers related to addresses
    - 1 for other phone numbers
    """
    queries = BaseTest.left_pane_queries + 11

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
    """
    queries = BaseTest.left_pane_queries + 1

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
