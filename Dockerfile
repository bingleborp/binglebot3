FROM python:3.8
ENV PROJECT_NAME=binglebot3

WORKDIR /usr/src/${PROJECT_NAME}

COPY . /usr/src/${PROJECT_NAME}

RUN pip install pyTelegramBotAPI

CMD ["python", "main.py"]