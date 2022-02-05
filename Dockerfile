FROM python:3.9-slim-buster

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv  \
    && pipenv lock --keep-outdated --requirements > requirements.txt \
    && pip install -r requirements.txt

COPY ./ ./

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
