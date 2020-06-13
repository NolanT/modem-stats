FROM python:3.8

#install python dependancies for parsing HTML
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

#install script used to query modem and push to splunk
COPY run_scrape.sh .
#COPY xfi-scraper.py .
COPY sb8200-scraper.py .

#first entry used for debug
#ENTRYPOINT [ "/bin/bash" ]
#second entry used for builds
ENTRYPOINT [ "/bin/bash", "run_scrape.sh" ]