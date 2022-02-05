FROM python:3.8-slim-buster

WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install pipenv 

RUN pip install -r ./requirements.txt

COPY ./ ./

CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]
