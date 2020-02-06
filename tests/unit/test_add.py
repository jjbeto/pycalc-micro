import msgpack
import pytest

from add.add_operation import add
from add.main import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_post_add(client):
    json = {'t': 'add',
            'v': {
                'l': {'t': 'num', 'v': 1},
                'r': {'t': 'num', 'v': 1}
            }}
    response = client.post("/", data=msgpack.packb(json), content_type='application/msgpack')
    assert response.status_code == 200

    result = msgpack.unpackb(response.data, raw=False)
    assert result.get('v') == 2


def test_add():
    json = {'t': 'add',
            'v': {
                'l': {'t': 'num', 'v': 1},
                'r': {'t': 'num', 'v': 1}
            }}
    response = add(json)
    assert response.get('t') == 'num'
    assert response.get('v') == 2


def test_add_sub_levels():
    json = {'t': 'add',
            'v':
                {
                    'l': {'t': 'num', 'v': 1},
                    'r':
                        {
                            't': 'add',
                            'v':
                                {
                                    'l': {'t': 'num', 'v': 1},
                                    'r': {'t': 'num', 'v': 1}
                                }
                        }
                }}
    response = add(json)
    assert response.get('t') == 'num'
    assert response.get('v') == 3
