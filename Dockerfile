# syntax=docker/dockerfile:1

FROM python:3.9-alpine

WORKDIR /app

COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 5000/tcp

CMD [ "python", "-m" , "gr_watcher"]