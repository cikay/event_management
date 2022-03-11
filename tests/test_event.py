
import random
from datetime import datetime, timedelta
from wsgiref import headers

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


def test_admin_user_update_event():
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


    #login user
    login_fields = {
        'username': username,
        'password': password
    }
    response = client.post('/users/login', data=login_fields)
    data = response.json()
    assert 'access_token' in data


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
    created_event = response.json()
    created_event_id = created_event['id']

    # update event
    event_new_description = generate_random_string(10)
    update_open_window = str(datetime.now() + timedelta(days=20))
    event_create_fields = {
        'description': f'Test Event {event_new_description}',
        'open_window': update_open_window
    }

    response = client.patch(
        f'/events/update/{created_event_id}',
        json=event_create_fields,
        headers=headers
    )
    assert response.status_code == status.HTTP_200_OK


def test_admin_user_event_list():
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


    #login user
    login_fields = {
        'username': username,
        'password': password
    }
    response = client.post('/users/login', data=login_fields)
    token_data = response.json()
    assert 'access_token' in token_data

    # list events
    headers = {
        'Authorization': f'Bearer {token_data["access_token"]}'
    }
    all_events_response = client.get('/events/', data=data, headers=headers)
    assert all_events_response.status_code == 200, response.text
    all_events = all_events_response.json()
    'id' in all_events[0]


def test_admin_user_event_retreive():
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
    event_data = response.json()
    assert event_data['username'] == user_create_fields['username']
    assert event_data['is_admin'] is True
    assert 'id' in event_data


    #login user
    login_fields = {
        'username': username,
        'password': password
    }
    response = client.post('/users/login', data=login_fields)
    token_data = response.json()
    assert 'access_token' in token_data

    # retreive an event
    headers = {
        'Authorization': f'{token_data["token_type"]} {token_data["access_token"]}'
    }
    url = f'/events/{event_data["id"]}'
    all_events_response = client.get(url, headers=headers)
    assert all_events_response.status_code == 200, response.text
    event = all_events_response.json()
    'id' in event


def test_remain_tickets_count_value():
    # create user
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
    created_event_data = response.json()
    assert created_event_data['total_tickets_count'] == created_event_data['remain_tickets_count']


def test_create_ticket():
    # create user
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
    created_event_data = response.json()
    assert created_event_data['total_tickets_count'] == created_event_data['remain_tickets_count']

    ticket_create_fields = {
        'event_id': created_event_data['id'],
        'seat_no': 'A1'
    }

    ticket_response = client.post(
        '/tickets/create',
        json=ticket_create_fields,
        headers=headers
    )
    assert ticket_response.status_code == status.HTTP_200_OK


def test_no_ticket_available():
    # create user
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
    event_description = generate_random_string(10)
    open_window = str(datetime.now() + timedelta(days=10))
    event_create_fields = {
        'description': f'Test Event {event_description}',
        'total_tickets_count': 0,
        'open_window': open_window,
        'start_date': str(datetime.now() + timedelta(days=20)),
        'end_date': str(datetime.now() + timedelta(days=20, hours=2))
    }
    headers = {
        'Authorization': f'Bearer {data["access_token"]}'
    }
    response = client.post('/events/create', json=event_create_fields, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    created_event_data = response.json()
    assert created_event_data['total_tickets_count'] == created_event_data['remain_tickets_count']

    ticket_create_fields = {
        'event_id': created_event_data['id'],
        'seat_no': 'A1'
    }

    ticket_response = client.post(
        '/tickets/create',
        json=ticket_create_fields,
        headers=headers
    )
    assert ticket_response.status_code == status.HTTP_403_FORBIDDEN


def test_listing_tickets():
    # create user
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

    #login user
    login_fields = {
        'username': username,
        'password': password
    }
    response = client.post('/users/login', data=login_fields)
    token_data = response.json()
    assert 'access_token' in token_data

    # create event
    event_description = generate_random_string(10)
    total_tickets_count = random.randint(20, 1000)
    open_window = str(datetime.now() + timedelta(days=10))
    event_create_fields = {
        'description': f'Test Event {event_description}',
        'total_tickets_count': total_tickets_count,
        'open_window': open_window,
        'start_date': str(datetime.now() + timedelta(days=20)),
        'end_date': str(datetime.now() + timedelta(days=20, hours=2))
    }
    headers = {
        'Authorization': f'{token_data["token_type"]} {token_data["access_token"]}'
    }
    response = client.post('/events/create', json=event_create_fields, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    created_event_data = response.json()
    assert created_event_data['total_tickets_count'] == created_event_data['remain_tickets_count']

    ticket_create_fields = {
        'event_id': created_event_data['id'],
        'seat_no': 'A1'
    }

    ticket_response = client.post(
        '/tickets/create',
        json=ticket_create_fields,
        headers=headers
    )
    assert ticket_response.status_code == status.HTTP_200_OK

    ticket_list_response = client.get('tickets/', headers=headers)
    ticket_list_response.status_code == status.HTTP_200_OK
    ticket_list = ticket_list_response.json()
    assert 'id' in ticket_list[0]


def test_retrieving_ticket():
        # create user
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

    #login user
    login_fields = {
        'username': username,
        'password': password
    }
    response = client.post('/users/login', data=login_fields)
    token_data = response.json()
    assert 'access_token' in token_data

    # create event
    event_description = generate_random_string(10)
    total_tickets_count = random.randint(20, 1000)
    open_window = str(datetime.now() + timedelta(days=10))
    event_create_fields = {
        'description': f'Test Event {event_description}',
        'total_tickets_count': total_tickets_count,
        'open_window': open_window,
        'start_date': str(datetime.now() + timedelta(days=20)),
        'end_date': str(datetime.now() + timedelta(days=20, hours=2))
    }
    headers = {
        'Authorization': f'{token_data["token_type"]} {token_data["access_token"]}'
    }
    response = client.post('/events/create', json=event_create_fields, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    created_event_data = response.json()
    assert created_event_data['total_tickets_count'] == created_event_data['remain_tickets_count']

    ticket_create_fields = {
        'event_id': created_event_data['id'],
        'seat_no': 'A1'
    }

    ticket_create_response = client.post(
        '/tickets/create',
        json=ticket_create_fields,
        headers=headers
    )
    assert ticket_create_response.status_code == status.HTTP_200_OK

    created_ticket = ticket_create_response.json()

    url = f'tickets/{created_ticket["id"]}'
    ticket_response = client.get(url, headers=headers)
    ticket_response.status_code == status.HTTP_200_OK
    ticket = ticket_response.json()
    assert 'id' in ticket
