FROM python:3.8

WORKDIR /stats_website

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD python -m stats_website.stats_website
