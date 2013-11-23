#import xml.etree.ElementTree as et
from datetime import datetime, timedelta
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
                [BODY]
              </soap:Body>
            </soap:Envelope>""" % (username, password)

    def do_action(self, action, params=None):
        url = 'https://webservices.listrak.com/v31/IntegrationService.asmx'

        headers = {
            'SOAPAction': 'http://webservices.listrak.com/v31/%s' % action,
            'Content-Type': 'text/xml; charset=utf-8'
        }

        data = self.soap_header
        if params:
            body = '<%s xmlns="http://webservices.listrak.com/v31/">' % action
            for k,v in params.items():
                body += "<%s>%s</%s>" % (k, v, k)
            body += '</%s>' % action
            data = data.replace('[BODY]', body)
        else:
            data = data.replace('[BODY]', '<%s xmlns="http://webservices.listrak.com/v31/" />' % action)

        response = requests.post(url, data=data, headers=headers)
        print response.text
        # Handle nil response with empty list
        #if '<WSException xsi:nil="true" />' in response.text: return [];
        print response.text
        results = xmltodict.parse(response.text)
        return results['soap:Envelope']['soap:Body']['%sResponse'%action]['%sResult'%action].items()[0][1]

    def get_lists(self):
        r = self.do_action('GetContactListCollection')
        return r

    def get_saved_messages(self, list_id):
        r = self.do_action('GetSavedMessageCollection', {'ListID': list_id})
        return r

    def get_message_activity(self, list_id, days=30):
        start = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
        end = datetime.today().strftime("%Y-%m-%d")
        
        data = {'ListID': list_id, 'StartDate':start, 'EndDate':end}
        r = self.do_action('ReportListMessageActivity', data)
        return r        