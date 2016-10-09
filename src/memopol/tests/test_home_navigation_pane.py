from .base import BaseTest


class NavigationPaneTest(BaseTest):
    url = '/'

    def test_queries(self):
        # First query to set session variables
        self.client.get(self.url)

        """
        Today mep
        - 1 for count reps with non null score
        - 1 for random mep
        - 1 for prefetch main mandate
        Latest votes
        - 1 for latest votes count setting
        - 1 for latest votes (proposal)
        - 1 for prefetching latest votes themes
        - 1 for prefetching latest votes dossier themes
        - 1 for prefetching latest votes dossier documents
        - 1 for prefetching latest votes dossier documents chambers
        Featured themes
        - 1 for featured themes
        """
        home_queries = 10

        with self.assertNumQueries(self.left_pane_queries + home_queries):
            self.client.get(self.url)

    def test_rep_search_chambers(self):
        self.selector_test('#form-rep #chamber-rep option')

    def test_rep_search_countries(self):
        self.selector_test('#form-rep #country option')

    def test_rep_search_parties(self):
        self.selector_test('#form-rep #party option')

    def test_rep_search_committee(self):
        self.selector_test('#form-rep #committee option')

    def test_rep_search_delegation(self):
        self.selector_test('#form-rep #delegation option')

    def test_dossier_search_chambers(self):
        self.selector_test('#form-dossier #chamber-dossier option')
