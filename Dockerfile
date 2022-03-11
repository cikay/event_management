
FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code/

RUN pip install pipenv

COPY Pipfile Pipfile.lock /code/

RUN pipenv install --system --dev

COPY . /code/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
