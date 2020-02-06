import msgpack
import pytest

from sub.sub_operation import sub
from sub.main import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_post_sub(client):
    json = {'t': 'sub',
            'v': {
                'l': {'t': 'num', 'v': 1},
                'r': {'t': 'num', 'v': 1}
            }}
    response = client.post("/", data=msgpack.packb(json), content_type='application/msgpack')
    assert response.status_code == 200

    result = msgpack.unpackb(response.data, raw=False)
    assert result.get('v') == 0


def test_sub():
    json = {'t': 'sub',
            'v': {
                'l': {'t': 'num', 'v': 1},
                'r': {'t': 'num', 'v': 1}
            }}
    response = sub(json)
    assert response.get('t') == 'num'
    assert response.get('v') == 0


def test_add_sub_levels():
    json = {'t': 'sub',
            'v':
                {
                    'l': {'t': 'num', 'v': 1},
                    'r':
                        {
                            't': 'sub',
                            'v':
                                {
                                    'l': {'t': 'num', 'v': 1},
                                    'r': {'t': 'num', 'v': 1}
                                }
                        }
                }}
    response = sub(json)
    assert response.get('t') == 'num'
    assert response.get('v') == 1
