FROM python:3.10-bullseye

LABEL maintainer="Prashant <prashantn@riseup.net>"

WORKDIR /manga_downloader

COPY . .

RUN apt update && apt install -y p7zip-full && pip3 install -r requirements.txt && mkdir -p static

ENV URL="https://www.webtoons.com/en/action/samurai-no-tora/list?title_no=3654"
ENV EMAIL="prashantn@riseup.net"
ENV START=1

CMD [ "python3","app.py"]