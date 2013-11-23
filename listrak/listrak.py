#import xml.etree.ElementTree as et
import xmltodict
import requests
from exceptions import *


class ListrakClient():
    def __init__(self, username, password):
        self.soap_header = """<?xml version="1.0" encoding="utf-8"?>
            <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
              <soap:Header>
                <WSUser xmlns="http://webservices.listrak.com/v31/">
                  <UserName>%s</UserName>
                  <Password>%s</Password>
                </WSUser>
              </soap:Header>
              <soap:Body>
                <GetContactListCollection xmlns="http://webservices.listrak.com/v31/" />
              </soap:Body>
            </soap:Envelope>""" % (username, password)

    def do_action(self, action):
        url = 'https://webservices.listrak.com/v31/IntegrationService.asmx'
        headers = {
            'SOAPAction': 'http://webservices.listrak.com/v31/%s' % action,
            'Content-Type': 'text/xml; charset=utf-8'
        }
        response = requests.post(url, data=self.soap_header, headers=headers)
        results = xmltodict.parse(response.text)
        return results['soap:Envelope']['soap:Body']['%sResponse'%action]['%sResult'%action].items()[0][1]

    def get_lists(self):
        r = self.do_action('GetContactListCollection')
        return r
