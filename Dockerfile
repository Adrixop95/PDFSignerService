FROM python:3.8-slim as python-base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get --no-install-recommends install -y \
    swig \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt /app
RUN  pip install -r requirements.txt
RUN  pip install gunicorn 

FROM python:3.8-slim as prod

EXPOSE 8000
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=python-base /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=python-base /usr/local/bin/ /usr/local/bin/

ADD . /app

CMD [ "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
