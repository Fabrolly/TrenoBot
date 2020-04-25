FROM python:3.8

WORKDIR /frontend

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD python -m frontend.frontend
