import random

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def generate_random_string(length):
    sample_string = 'abcdefghijklmnopqrstuvwxy_123456789'
    return ''.join((random.choice(sample_string)) for _ in range(length))  


def test_create_user():
    random_string = generate_random_string(10)
    fields = {
        'firstname': f'Test {random_string}',
        'lastname': f'Test {random_string}',
        'username': f'test_{random_string}',
        'password': f'test_{random_string}',
        'is_admin': False
    }
    response = client.post('/users/create', json=fields)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['username'] == fields['username']
    assert data['is_admin'] is False
    assert 'id' in data


def test_create_admin():
    random_string = generate_random_string(10)
    fields = {
        'firstname': f'Test {random_string}',
        'lastname': f'Test {random_string}',
        'username': f'test_{random_string}',
        'password': f'test_{random_string}',
        'is_admin': True
    }
    response = client.post('/users/create', json=fields)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['username'] == fields['username']
    assert data['is_admin'] is True
    assert 'id' in data
