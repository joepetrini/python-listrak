python-listrak
==============

Python wrapper for Listrak v31 SOAP API

Installation
------------
Requirements: SOAPpy
TODO: register with pip

Usage
-----
'''python
from listrak import ListrakClient

client = ListrakClient('username', 'password')

lists = client.get_lists()

for l in lists:
    print "%s - %s" % (l['ListId'], l['ListName'])
'''


Version History
---------------
* 0.2 - SOAP requests working.  get_lists() added as first method
* 0.1 - First commit