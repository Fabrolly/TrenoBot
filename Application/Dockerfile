FROM python:3.8

WORKDIR /Application

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD python starter.py
