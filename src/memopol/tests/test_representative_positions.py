from .base import RepresentativeBaseTest


class RepresentativePositionsTest(RepresentativeBaseTest):
    tab = 'positions'

    """
    - One for positions
    - One for position scores
    - One for position themes
    - One for position representatives
    """
    queries = RepresentativeBaseTest.queries + 4

    def test_queries(self):
        self.do_query_test()

    def test_position_buttons(self):
        self.selector_test('.position-button')

    def test_position_details(self):
        self.selector_test('.position-details')

    def test_no_positions(self):
        url = '/representatives/francois-asensi-1945-06-01/%s/'
        self.selector_test('.no-positions', url % self.tab)
