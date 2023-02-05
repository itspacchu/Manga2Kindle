FROM python:3.10-bullseye

LABEL maintainer="Prashant <prashantn@riseup.net>"

WORKDIR /manga_downloader

COPY . .

RUN apt update && apt install -y p7zip-full && pip3 install -r requirements.txt && mkdir -p static

CMD [ "flask","run","--host=0.0.0.0" ]