#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
MODEM_IP = os.getenv('MODEM_IP')
MODEM_IP = "192.168.100.1"
CONTAINER_HOSTNAME = os.getenv('HOSTNAME')

if __name__ == "__main__":
    headers = {
         'User-Agent':
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
    }
    connectionstatus_url = 'http://' + MODEM_IP + '/cmconnectionstatus.html'
    logging.info("starting session")
    with requests.Session() as s:
        logging.info("get cable stats")
        rStatus = s.get(connectionstatus_url)

    #extract tables
    soup = BeautifulSoup(rStatus.text, 'lxml')
    infoTables = soup.findAll('table')
    startupTable=str(infoTables[0])
    downstreamTable=str(infoTables[1])
    upstreamTable=str(infoTables[2])

    #process HTML tables
    startupDF = pd.read_html(startupTable, header=1, index_col=None)[0]
    #downstreamCols = ["Lock Status", "Modulation", "Frequency", "Power", "SNR/MER", "Corrected", "Uncorrectables"]
    downstreamDF = pd.read_html(downstreamTable, header=1, index_col=0)[0]
    #"Channel ID",
    downstreamDF.columns = ["Lock Status", "Modulation", "Frequency", "Power Level", "SNR", "Corrected", "Uncorrectables"]
    #downstreamDF.transpose()
    upstreamDF = pd.read_html(upstreamTable, header=1, index_col=0)[0]
    upstreamDF.columns = ["Channel ID", "Lock Status", "Channel Type", "Frequency", "Symbol Rate", "Power Level"]
    #upstreamDF.transpose()

    #convert to JSON
    startupJSON = startupDF.to_json(orient="index")
    downstreamJSON = downstreamDF.to_json(orient="index")
    upstreamJSON = upstreamDF.to_json(orient="index")

    print("{\"event\": {")
    print("\"containerHostname\": \"" + CONTAINER_HOSTNAME + "\",")
    print("\"startup\": " + startupJSON + ",")
    print("\"downstreamChannels\": " + downstreamJSON + ",")
    print("\"upstreamChannels\": " + upstreamJSON + "")
    print("}}")