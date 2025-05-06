FROM python:3.12.3

RUN apt-get update && apt-get install -y gettext libgettextpo-dev
RUN mkdir /backend
WORKDIR /backend
ADD requirements.txt /backend/

RUN pip install -r requirements.txt
ADD . /backend/
WORKDIR /backend/website
CMD ["watchmedo", "auto-restart", "--recursive", "--pattern=*.py", "--", "celery", "-A", "website", "worker", "-B", "-l", "info"]
