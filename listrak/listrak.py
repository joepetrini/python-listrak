#import xml.etree.ElementTree as et
import socket, re
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
        #print response.text
        if "[InvalidLogonAttempt]" in response.text:
            raise InvalidLogonAttempt("Invalid user name or password")
        if "[LoginAttemptsExceeded]" in response.text:
            raise InvalidLogonAttempt("Login attempts exceeded")
        if "[ProhibitedIPAddress]" in response.text:
            raise InvalidLogonAttempt(
                "IP address not allowed.  You need to add %s to your approved list." % socket.gethostbyaddr("traklis.com")[2][0])
        # Handle nil response with empty list
        #if '<WSException xsi:nil="true" />' in response.text: return [];

        results = xmltodict.parse(response.text)
        try:
            ret = results['soap:Envelope']['soap:Body']['%sResponse'%action]['%sResult'%action].items()[0][1]
        except AttributeError:
            # Single value response, no need to build a response list
            return results['soap:Envelope']['soap:Body']['%sResponse'%action]['%sResult'%action]
        except KeyError:
            return []
        for i in ret:
            for k,v in i.items():
                #if type(v) != "<type 'unicode'>":
                #    i.pop(k, None)
                if "Date" in k:
                    #print v
                    i[k] = datetime.strptime(re.sub('\.\d{1,3}','',v), "%Y-%m-%dT%H:%M:%S")
        return ret

    def get_lists(self):
        r = self.do_action('GetContactListCollection')
        # Assign list size values
        for l in r:
            c = self.do_action('GetFilteredListCount', {'ListID': l['ListID']})
            l['ListSize'] = c
        return r

    def get_saved_messages(self, list_id):
        r = self.do_action('GetSavedMessageCollection', {'ListID': list_id})
        return r

    def get_message_activity(self, list_id, days=30):
        start = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
        end = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        data = {'ListID': list_id, 'StartDate':start, 'EndDate':end}
        r = self.do_action('ReportListMessageActivity', data)
        print r
        return r

    def get_msg_opens(self, msg_id, page=1):
        data = {'MsgID': msg_id, 'Page': page}
        ret = self.do_action('ReportMessageContactOpen', data)
        return ret

    def get_msg_clicks(self, msg_id, page=1, days=30):
        start = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
        end = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")        

        data = {'MsgID': msg_id, 'Page': page, 'StartDate':start, 'EndDate':end}
        ret = self.do_action('ReportRangeMessageContactClick', data)
        return ret

    def get_msg_unsubs(self, msg_id, page=1):
        data = {'MsgID': msg_id, 'Page': page}
        ret = self.do_action('ReportMessageContactRemoval', data)
        return ret

    def upload_contacts(self):
        #TODO
        pass

    def validate(self):
        try:
            self.get_lists()
            return True
        except Exception, e:
            return e
