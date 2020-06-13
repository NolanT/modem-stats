#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
import os
XFI_IP = os.getenv('XFI_IP')
XFI_USERNAME = os.getenv('XFI_USERNAME')
XFI_PASSWORD = os.getenv('XFI_PASSWORD')
CONTAINER_HOSTNAME = os.getenv('HOSTNAME')

if __name__ == "__main__":
    headers = {
         'User-Agent':
         'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:64.0) Gecko/20100101 Firefox/64.0'
    }
    payload = {'username': XFI_USERNAME, 'password': XFI_PASSWORD }
    login_url = 'http://' + XFI_IP + '/check.php'
    network_status_url = 'http://' + XFI_IP + '/network_setup.php'
    logging.info("starting session")
    with requests.Session() as s:
        logging.info("post login")
        rLogin = s.post(login_url, data=payload, headers=headers)
        logging.info("get cable stats")
        rStatus = s.get(network_status_url)
    soup = BeautifulSoup(rStatus.text, 'lxml')
    infoTables = soup.findAll('table')
    for div in soup.find_all("div", {'class':'div_mta'}): 
        div.decompose()
    for div in soup.find_all("div", {'class':'div_cm'}): 
        div.decompose()
    dataDivs = soup.findAll("div", {"class": "form-row"})
    #start json
    print("{\"event\": {")
    print("\"Container Hostname\": \"" + CONTAINER_HOSTNAME + "\",")
    downstreamTable=str(infoTables[0])
    #downstreamFullTable=str(infoTables[0]) + str(infoTables[2])
    #print(downstreamFullTable)
    upstreamTable=str(infoTables[1])
    #errorsTable=str(infoTables[2])
    downstreamDF = pd.read_html(downstreamTable, header=1, index_col=0)[0]
    upstreamDF = pd.read_html(upstreamTable, header=1, index_col=0)[0]
    #errorsDF = pd.read_html(errorsTable, header=None, index_col=0)[0]
    #fullDownstream = downstreamDF.append(errorsDF)
    downstreamJSON = downstreamDF.to_json()
    upstreamJSON = upstreamDF.to_json()
    #errorsJSON = errorsDF.to_json()
    for d in dataDivs:
        print("\"" + d.findChild('span',{"class":"readonlyLabel"}).text.strip().replace(':','') + "\":\"" + d.findChild('span',{"class":"value"}).text.strip() + "\",")
    print("\"downstreamChannels\": " + downstreamJSON + ",")
    print("\"upstreamChannels\": " + upstreamJSON + "")
    #print("\"errorsChannels\": " + errorsJSON + ",")
    #print("\"fullDownstream\": " + fullDownstream.to_json())
    #end json
    print("}}")