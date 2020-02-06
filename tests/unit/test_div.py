import msgpack
import pytest

from div.div_operation import div
from div.main import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_post_div(client):
    json = {'t': 'div',
            'v': {
                'l': {'t': 'num', 'v': 2},
                'r': {'t': 'num', 'v': 2}
            }}
    response = client.post("/", data=msgpack.packb(json), content_type='application/msgpack')
    assert response.status_code == 200

    result = msgpack.unpackb(response.data, raw=False)
    assert result.get('v') == 1


def test_div():
    json = {'t': 'div',
            'v': {
                'l': {'t': 'num', 'v': 2},
                'r': {'t': 'num', 'v': 2}
            }}
    response = div(json)
    assert response.get('t') == 'num'
    assert response.get('v') == 1


def test_add_div_levels():
    json = {'t': 'div',
            'v':
                {
                    'l': {'t': 'num', 'v': 2},
                    'r':
                        {
                            't': 'div',
                            'v':
                                {
                                    'l': {'t': 'num', 'v': 4},
                                    'r': {'t': 'num', 'v': 2}
                                }
                        }
                }}
    response = div(json)
    assert response.get('t') == 'num'
    assert response.get('v') == 1
