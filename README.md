python-listrak
==============

Python wrapper for Listrak v31 SOAP API

Installation
------------
Requirements: requests, xmltodict

TODO: register with PyPI

Usage
-----
```python
from listrak import ListrakClient

client = ListrakClient('username', 'password')

lists = client.get_lists()

for l in lists:
    print "%s - %s" % (l['ListId'], l['ListName'])
```

Methods
-------
* get_lists()
* get_saved_messages(list_id)
* get_message_activity(list_id)
* get_message_opens(msg_id)
* get_msg_clicks(msg_id)
* get_msg_unsubs(msg_id)
* validate() # For user/pass and ip access validation
* update_contact()
* upload_contacts() # TODO


Version History
---------------
* 0.6 - get_list_attributes and update_contact methods added
* 0.5 - get_msg methods
* 0.4 - Custom exception handling, user/pass validation, auto datetime conversion
* 0.3 - New message methods, added param passing to SOAP request
* 0.2 - SOAP requests working.  get_lists() added as first method
* 0.1 - First commit
