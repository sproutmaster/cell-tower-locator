FROM python:3.10-bullseye

COPY . /cell-tower-locator
WORKDIR /cell-tower-locator

RUN apt update \
  && rm -rf /var/lib/apt/lists/ \
  && pip3 install -r req.txt

ENV API_KEY=${API_KEY}

CMD gunicorn -b 0.0.0.0:5000 -w 4 main:app
