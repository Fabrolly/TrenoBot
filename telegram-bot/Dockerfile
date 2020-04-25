FROM python:3.8
RUN apt-get -q update && apt-get -qy install netcat

WORKDIR /telegram-bot

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD python -m telegram_bot.bot
