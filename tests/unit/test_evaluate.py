import pytest

from evaluate.main import create_app, extract_body


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_post_text(client):
    """
    TODO to be improved: for now its a syntax error that leads to status_code 500
    """
    response = client.post("/", data="abc", content_type='text/plain')
    assert response.json == {'error': {'message': 'An unexpected error occurred - Unexpected character: a'}}
    assert response.status_code == 500


def test_post_with_wrong_content_type(client):
    response = client.post("/", data="abc", content_type='text/html')
    assert response.json == {'error': {'message': 'Invalid request type, only text/plain is accepted'}}
    assert response.status_code == 406


def check_expressions(client, expressions):
    for expr, result in expressions.items():
        response = client.post("/", data=expr, content_type='text/plain')
        assert extract_body(response.data) == result
        assert response.status_code == 200


def test_evaluate_simple_values(client):
    expressions = {
        ' + 1 ': '1.0',
        '-1': '-1.0',
    }
    check_expressions(client, expressions)


def test_evaluate_simple_expressions(client):
    expressions = {
        ' 1 + 1 ': '2.0',
        '100 / 4': '25.0',
        '9 * 9': '81.0',
        '15 - 5': '10.0'
    }
    check_expressions(client, expressions)


def test_evaluate_sequence_expressions(client):
    expressions = {
        ' 2 x 2 / 2 ': '2.0',
        ' 2 / 2 * 2 ': '2.0',
        ' 2 + 2 / 2 ': '3.0',
        ' 2 / 2 + 1 ': '2.0',
    }
    check_expressions(client, expressions)


def test_evaluate_expressions_with_sublevel(client):
    expressions = {
        '(4+4) * 10': '80.0',
        '(10/10) * (-5+1)': '-4.0',
    }
    check_expressions(client, expressions)


def test_evaluate_expressions_with_two_sublevels(client):
    expressions = {
        '(4+(16/4)) * 10': '80.0',
        '((4x2+2)/(5x2)) * ((5-10)+(10-9))': '-4.0',
    }
    check_expressions(client, expressions)


def test_evaluate_expressions_more_complex(client):
    """all expressions from https://teresachiacchio.wixsite.com/matemagica/expressoes"""
    expressions = {
        '4- [-(6+4)+(3-2-1)]': '14.0',
        '15 x 2 - 30 / 3 + 7': '27.0',
        '10 x [30 / (2 x 3 + 4) + 15]': '180.0',
        '25 + {14 - [25 x 4 + 40 - (20 / 2 + 10)]}': '-81.0',
        '37 - 14 + 35 - 10': '48.0',
        '32 / 2 . 3 / 4 . 5': '3.091787439613527',
        '32 / 2 x 3 / 4 x 5': '60.0',
        '180 / 4 * {9 / [3 * (3 * 1)]}': '45.0',
        '16 : (-4) x 2': '-8.0',
        '16 x(-4): 2': '-32.0',
        '10 + 2^2 x 3': '22.0',
        '5^2 - 4 x 2 + 3': '20.0',
        '20 - [4^2 + ( 2^3 - 7 )]': '3.0',
        '10 -{ 10 + [ 8^2 : ( 10 - 2 ) + 3 x 2 ] }': '-14.0',
        '27 + {14 + 3 x [100 : (18 - 4 x 2) + 7] } : 13': '32.0',
        '{100 - 413 x (20 - 5 x 4) + 25} : 5': '25.0',
        '25 + { 12 + [ 2 - ( 8 - 6 ) + 2 ]}': '39.0',
        '38 - { 20 - [ 22 - ( 5 + 3) + ( 7 - 4 +1)]}': '36.0',
        '26 + { 12 - [ ( 30 - 18) + ( 4 - 1) - 6 ] - 1 }': '28.0',
        '(90+10)*2 / (90+(1000/    (   50+25*2)))': '2.0',
    }
    check_expressions(client, expressions)
