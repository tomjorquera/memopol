from .base import BaseTest


class HomeTest(BaseTest):
    url = '/'

    def test_queries(self):
        # First query to set session variables
        self.client.get(self.url)

        """
        - 3 for Today mep
            - 1 for count reps with non null score
            - 1 for random mep
            - 1 for prefetch main mandate
        - 6 for Latest votes
            - 1 for latest votes count setting
            - 1 for latest votes (proposal)
            - 1 for prefetching latest votes themes
            - 1 for prefetching latest votes dossier themes
            - 1 for prefetching latest votes dossier documents
            - 1 for prefetching latest votes dossier documents chambers
        - 1 for Featured themes
            - 1 for featured themes
        - 1 for Chambers
            - 1 for chambers and dossier/proposal counts
        """
        home_queries = 11

        with self.assertNumQueries(self.left_pane_queries + home_queries):
            self.client.get(self.url)
