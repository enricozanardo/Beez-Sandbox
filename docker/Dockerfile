FROM ubuntu:20.04 as python-base

ENV LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    TZ=Europe/Rome

RUN mkdir /code

WORKDIR /code

ARG DEBIAN_FRONTEND=noninteractive

RUN \
   apt-get -y upgrade && \
   apt -y clean && \
   apt-get -y update && \
   apt-get install -y gcc tini gettext nano && \
   apt-get install -y libreoffice && \
   apt-get install -y texlive-latex-base && \
   apt-get install -y --no-install-recommends --yes python3 && \
   apt-get install -y --no-install-recommends python3-pip && \
   apt-get install -y software-properties-common && \
   apt-get install -y python3-gdal && \
   add-apt-repository ppa:ubuntugis/ppa && \
   apt-get install -y python-numpy gdal-bin libgdal-dev && \
   apt-get install -y --no-install-recommends gdal-bin && \
   apt-get install -y --no-install-recommends gdal-bin && \
   apt-get install -y --no-install-recommends libgdal-dev && \
   apt-get install -y python3-dev && \
   apt-get install -y libpq-dev && \
   apt-get clean && apt-get autoremove -y && \
   rm -rf /var/lib/apt-get/lists/* && \
   pip3 install GDAL && \
   pip3 install -U urllib3

ARG CPLUS_INCLUDE_PATH=/usr/include/gdal
ARG C_INCLUDE_PATH=/usr/include/gdal

COPY . /code

RUN apt-get -y install nginx && \
    apt install build-essential checkinstall zlib1g-dev -y
#   mkdir /etc/nginx/certificates && \
#   mv ./docker/certbot/www/localhost.crt /etc/nginx/certificates/localhost.crt && \
#   mv ./docker/certbot/www/localhost.key /etc/nginx/certificates/localhost.key && \
#   mv ./docker/certbot/www/certificatum.crt /etc/nginx/certificates/certificatum.crt && \
#   mv ./docker/certbot/www/certificatum.key /etc/nginx/certificates/certificatum.key && \
#   systemctl enable nginx && \
#   service nginx start


RUN pip3 install -r requirements.txt && \
    pip3 install --upgrade requests && \
    pip3 install numpy

EXPOSE 80
EXPOSE 443
EXPOSE 9001
