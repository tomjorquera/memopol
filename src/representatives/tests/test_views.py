from django import test

from responsediff.response import Response


class RepresentativeManagerTest(test.TestCase):
    fixtures = ['representatives_test.json']

    def functional_test(self, queries, url):
        client = test.client.Client()

        # First query to setup session
        client.get(url)

        with self.assertNumQueries(queries):
            result = client.get(url)
        Response.for_test(self).assertNoDiff(result)

    def test_constituencies_api(self):
        self.functional_test(1, '/api/constituencies/?format=json')

    def test_groups_api(self):
        self.functional_test(1, '/api/groups/?format=json')

    def test_mandates_api(self):
        self.functional_test(1, '/api/mandates/?format=json')

    def test_chambers_api(self):
        self.functional_test(1, '/api/chambers/?format=json')

    def test_representatives_api(self):
        """
        Queries:

        - representatives,
        - emails,
        - websites,
        - addresses,
        - phones,
        - mandates.
        """
        self.functional_test(6, '/api/representatives/?format=json')
        # Test the filters

    def test_representatives_api_mandates(self):
        self.functional_test(1, '/api/representatives/' +
                '?active_mandates=INTA' + '&format=json')

    def test_representatives_api_constituency(self):
        self.functional_test(6, '/api/representatives/' +
                '?active_constituency=European%20Parliament' + '&format=json')
