FROM python:3.8

COPY ./sources.list /etc/apt/sources.list
RUN mkdir /code
WORKDIR /code
RUN apt-get update && apt-get install -y cron

RUN pip install pip -U -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY requirements.txt /code/
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
COPY . /code/
RUN python manage.py crontab add && python manage.py crontab show
