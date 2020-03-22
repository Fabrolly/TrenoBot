FROM python:3.8

WORKDIR /old_bot

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD python starter.py
