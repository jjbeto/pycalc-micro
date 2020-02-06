import msgpack
import requests


def test_post_div():
    json = {'t': 'div',
            'v': {
                'l': {'t': 'num', 'v': 4},
                'r': {'t': 'num', 'v': 2}
            }}
    response = requests.post('http://localhost:5000/',
                             data=msgpack.packb(json),
                             headers={'Content-Type': 'application/msgpack'})
    assert response.status_code == 200

    result = msgpack.unpackb(response.content, raw=False)
    assert result.get('v') == 2
