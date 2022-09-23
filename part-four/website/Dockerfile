FROM ubuntu:20.04

COPY app /app

WORKDIR /app

EXPOSE 80

RUN apt-get update && \
    apt install -y gcc python3-dev python3-pip python-markupsafe

COPY requirements.txt /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "server.py" ]