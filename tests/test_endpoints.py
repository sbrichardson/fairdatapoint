import pytest

from fdp.fdp import app, initGraph


@pytest.fixture
def client():
    '''Build http client'''
    with app.test_client() as client:
        yield client
    # Nothing to do, no connections to close.


class BaseEndpointTests:
    '''All implementations fo FDP should work for all endpoints.'''

    # datadir fixture provided via pytest-datadir-ng
    def test_fdp(self, client, datadir):
        """Testing post and get to fdp"""
        rv = client.post('/fdp', data=datadir['fdp_post.ttl'])
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        # TODO check fdp shacl
        # rv = client.post('/fdp', data=datadir['fdp_post_invalid.ttl'])
        # assert rv.status_code == 500
        # assert 'message' in rv.json
        # assert 'Validation Report' in rv.json['message']

        rv = client.get('/fdp')
        assert rv.status_code == 200
        assert 'Allow' in rv.headers
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'rdfs:seeAlso <http://0.0.0.0:8080/catalog/pbg-ld>' in rv.data

        rv = client.delete('/fdp')
        assert rv.status_code == 405
        assert 'message' in rv.json
        assert rv.json['message'] == 'Method Not Allowed'

    def test_catalog(self, client, datadir):
        """Testing post and get to catalog"""
        rv = client.post('/catalog/', data=datadir['catalog01_post.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/catalog/', data=datadir['catalog01_post_invalid.ttl'])
        assert rv.status_code == 500
        assert 'Validation Report' in rv.json['message']

        rv = client.post('/catalog/', data=datadir['catalog02_post.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/catalog/')
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/plain'
        assert b'catalog-01' in rv.data
        assert b'catalog-02' in rv.data

        rv = client.get('/catalog/catalog-01')
        assert rv.status_code == 200
        assert 'Allow' in rv.headers
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'catalog-01' in rv.data

        rv = client.get('/catalog/catalog-02',
                        headers = {'Accept': 'application/ld+json'})
        assert rv.status_code == 200
        assert 'Allow' in rv.headers
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'application/ld+json'
        assert b'catalog-02' in rv.data

        rv = client.delete('/catalog/catalog-01')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/catalog/catalog-01')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.delete('/catalog/catalog-01')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/catalog/')
        assert rv.status_code == 200
        assert b'catalog-01' not in rv.data
        assert b'catalog-02' in rv.data

        rv = client.delete('/catalog/catalog-02')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/catalog/')
        assert rv.status_code == 204

    def test_dataset(self, client, datadir):
        """Testing post and get to dataset"""
        rv = client.post('/dataset/', data=datadir['dataset01_post.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/dataset/', data=datadir['dataset01_post_invalid.ttl'])
        assert rv.status_code == 500
        assert 'Validation Report' in rv.json['message']

        rv = client.post('/dataset/', data=datadir['dataset02_post.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/dataset/')
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/plain'
        assert b'breedb' in rv.data
        assert b'dataset02' in rv.data

        rv = client.get('/dataset/breedb', )
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'breedb' in rv.data

        rv = client.get('/dataset/dataset02',
                        headers = {'Accept': 'application/ld+json'})
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'application/ld+json'
        assert b'dataset02' in rv.data

        rv = client.delete('/dataset/breedb')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/dataset/breedb')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.delete('/dataset/breedb')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/dataset/')
        assert rv.status_code == 200
        assert b'breedb' not in rv.data
        assert b'dataset02' in rv.data

        rv = client.delete('/dataset/dataset02')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/dataset/')
        assert rv.status_code == 204

    def test_distribution(self, client, datadir):
        """Testing post and get to distribution"""

        rv = client.post('/distribution/', data=datadir['dist01_post.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.post('/distribution/', data=datadir['dist01_post_invalid.ttl'])
        assert rv.status_code == 500
        assert 'message' in rv.json
        assert 'Validation Report' in rv.json['message']

        rv = client.post('/distribution/', data=datadir['dist02_post.ttl'])
        assert rv.status_code == 200
        assert rv.json['message'] == 'Ok'

        rv = client.get('/distribution/')
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/plain'
        assert b'breedb-sparql' in rv.data
        assert b'dist02' in rv.data

        rv = client.get('/distribution/breedb-sparql')
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'text/turtle'
        assert b'breedb-sparql' in rv.data

        rv = client.get('/distribution/dist02',
                        headers = {'Accept': 'application/ld+json'})
        assert rv.status_code == 200
        assert 'GET' in rv.headers['Allow']
        assert rv.mimetype == 'application/ld+json'
        assert b'dist02' in rv.data

        rv = client.delete('/distribution/breedb-sparql')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/distribution/breedb-sparql')
        assert rv.status_code == 404
        assert 'message' in rv.json
        assert rv.json['message'] == 'Not Found'

        rv = client.get('/distribution/')
        assert rv.status_code == 200
        assert b'breedb-sparql' not in rv.data
        assert b'dist02' in rv.data

        rv = client.delete('/distribution/dist02')
        assert rv.status_code == 200
        assert 'message' in rv.json
        assert rv.json['message'] == 'Ok'

        rv = client.get('/distribution/')
        assert rv.status_code == 204


class TestFairgraphEndpoints(BaseEndpointTests):
    '''Test endpoints the in-memory graph implementation'''
    def setup_class(self):
        initGraph(host='0.0.0.0', port=8080, dataFile='./samples/minimal.ttl', endpoint=None)


class TestMetadataEndpoints(BaseEndpointTests):
    '''Test endpoints using the metadata.py graph implementation'''
    def setup_class(self):
        initGraph(host='0.0.0.0', port=8080, dataFile='./samples/config.ini', endpoint=None)


class TestStoregraphEndpoints(BaseEndpointTests):
    '''Test endpoints using the SPARQL graph implementation'''
    def setup_class(self):
        initGraph(host='0.0.0.0', port=8080, dataFile=None, endpoint='http://0.0.0.0:8890/sparql')
