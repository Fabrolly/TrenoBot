FROM python:3.8

WORKDIR /telegram-bot

ADD requirements.txt .
RUN pip install -r requirements.txt

ADD . .

CMD python -m telegram_bot.bot
