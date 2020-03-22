FROM python:3.8

WORKDIR /backend

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD python backend.py
