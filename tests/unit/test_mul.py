import msgpack
import pytest

from mul.main import create_app
from mul.mul_operation import mul


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_post_mul(client):
    json = {'t': 'mul',
            'v': {
                'l': {'t': 'num', 'v': 2},
                'r': {'t': 'num', 'v': 2}
            }}
    response = client.post("/", data=msgpack.packb(json), content_type='application/msgpack')
    assert response.status_code == 200

    result = msgpack.unpackb(response.data, raw=False)
    assert result.get('v') == 4


def test_mul():
    json = {'t': 'mul',
            'v': {
                'l': {'t': 'num', 'v': 2},
                'r': {'t': 'num', 'v': 2}
            }}
    response = mul(json)
    assert response.get('t') == 'num'
    assert response.get('v') == 4


def test_add_mul_levels():
    json = {'t': 'mul',
            'v':
                {
                    'l': {'t': 'num', 'v': 2},
                    'r':
                        {
                            't': 'mul',
                            'v':
                                {
                                    'l': {'t': 'num', 'v': 2},
                                    'r': {'t': 'num', 'v': 2}
                                }
                        }
                }}
    response = mul(json)
    assert response.get('t') == 'num'
    assert response.get('v') == 8
