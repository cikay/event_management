
import random
from datetime import datetime, timedelta

from fastapi.testclient import TestClient
from fastapi import status
from main import app
from tests.random_string import generate_random_string

client = TestClient(app)

def test_user_create_event():
    #create user
    user_string = generate_random_string(10)
    username = f'test_{user_string}'
    password = f'test_{user_string}'

    user_create_fields = {
        'firstname': f'Test {user_string}',
        'lastname': f'Test {user_string}',
        'username': username,
        'password': password,
        'is_admin': False
    }
    response = client.post('/users/create', json=user_create_fields)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['username'] == user_create_fields['username']
    assert data['is_admin'] is False
    assert 'id' in data
    print(data)
    #login user
    login_fields = {
        'username': username,
        'password': password
    }
    response = client.post('/users/login', data=login_fields)
    data = response.json()
    assert 'access_token' in data
    print(data)

    # create event
    total_tickets_count = random.randint(20, 1000)
    event_description = generate_random_string(10)
    open_window = str(datetime.now() + timedelta(days=10))
    event_create_fields = {
        'description': f'Test Event {event_description}',
        'total_tickets_count': total_tickets_count,
        'open_window': open_window,
        'start_date': str(datetime.now() + timedelta(days=20)),
        'end_date': str(datetime.now() + timedelta(days=20, hours=2))
    }
    headers = {
        'Authorization': f'Bearer {data["access_token"]}'
    }
    response = client.post('/events/create', json=event_create_fields, headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_user_create_event():
    #create user
    user_string = generate_random_string(10)
    username = f'test_{user_string}'
    password = f'test_{user_string}'

    user_create_fields = {
        'firstname': f'Test {user_string}',
        'lastname': f'Test {user_string}',
        'username': username,
        'password': password,
        'is_admin': True
    }
    response = client.post('/users/create', json=user_create_fields)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data['username'] == user_create_fields['username']
    assert data['is_admin'] is True
    assert 'id' in data
    print(data)
    #login user
    login_fields = {
        'username': username,
        'password': password
    }
    response = client.post('/users/login', data=login_fields)
    data = response.json()
    assert 'access_token' in data
    print(data)

    # create event
    total_tickets_count = random.randint(20, 1000)
    event_description = generate_random_string(10)
    open_window = str(datetime.now() + timedelta(days=10))
    event_create_fields = {
        'description': f'Test Event {event_description}',
        'total_tickets_count': total_tickets_count,
        'open_window': open_window,
        'start_date': str(datetime.now() + timedelta(days=20)),
        'end_date': str(datetime.now() + timedelta(days=20, hours=2))
    }
    headers = {
        'Authorization': f'Bearer {data["access_token"]}'
    }
    response = client.post('/events/create', json=event_create_fields, headers=headers)
    assert response.status_code == status.HTTP_200_OK

