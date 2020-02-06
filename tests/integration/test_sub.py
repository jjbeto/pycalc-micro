import msgpack
import requests


def test_post_add():
    json = {'t': 'sub',
            'v': {
                'l': {'t': 'num', 'v': 1},
                'r': {'t': 'num', 'v': 1}
            }}
    response = requests.post('http://localhost:5000/',
                             data=msgpack.packb(json),
                             headers={'Content-Type': 'application/msgpack'})
    assert response.status_code == 200

    result = msgpack.unpackb(response.content, raw=False)
    assert result.get('v') == 0
