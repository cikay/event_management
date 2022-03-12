
1. Clone the app by `git clone https://github.com/cikay/event_management`
2. Navigate to the app folder by `cd event_management`

In order to run the app, environment variables need to be set up

## Run App In Docker Container

Create a file called `docker.env` and define the following variables

```
POSTGRES_USER=your_username        # Set your own
POSTGRES_PASSWORD=your_password    # Set your own
POSTGRES_DB=your_database          # Needs to be created
POSTGRES_SERVER=postgres_db        # No need to be change, the same in the docker-compose.yml
POSTGRES_PORT=5432                 # No need to be change
```

After that you can run the app in container by `docker-compose up`

## Run App Locally

1. Create a file called `local.env` and define the following variables

```
POSTGRES_USER=your_username        # Set your own
POSTGRES_PASSWORD=your_password    # Set your own
POSTGRES_DB=your_database          # Needs to be created
POSTGRES_SERVER=localhost          # No need to change
POSTGRES_PORT=5432                 # No need to change
```

2. Create virtual environment by `python3.8 -m venv venv`
3. Activate virtual environment. The command depens on the OS you are using
4. Install dependencies by `pipenv install`
5. Run the app by `uvicorn main:app --port 7000`


If you are running the app either in container or locally go to `/docs` 
endpoint you will see all endpoint documented


After creating user you need to authorize to use the rest of endpoints

Hit the authorize button and pass your credentials you will see it is logged in the close the
dialog and use the rest endpoint
