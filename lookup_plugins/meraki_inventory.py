# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
     name: meraki_inventory
     author: Joshua Robinett (@jshinryz)
     plugin_type: lookup
     short_description: Meraki Inventory Source
     description:
        - Lookup plugin to provide a data on meraki environment.
        - Recursively get inventory from Meraki using an API Key.
     options:
         api_key:
             description:
                -  API Key used to communicate with Meraki. Please refer to their documentation.
             required: True
             type: str
         org_id:
             description: 
                - "Filter for a specific org id." 
                - "Example: "
                - "   org_id: '32492384290348'"
             required: False
         property:
             description: 
                - "Return only a certain property (good for wantlist=True)." 
                - "Example: "
                - "   property: 'serial''"
             required: False    
'''

EXAMPLES = '''
# Sample configuration file for Meraki lookup plugin
    vars:
      myproperties :
        - name
        - serial
      meraki_inventory: "{{ lookup('meraki_inventory',api_key=myapikey, org_id='12312312312', properties=myproperties, wantlist=True )}}"
    
    tasks:
    
    - name: Show The meraki data
      debug:
        var: meraki_inventory

'''

RETURN = '''
_raw:
  description: comma-separated list of CIDR ranges
'''

import os
import re
import traceback
import requests

from datetime import datetime, timedelta

from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ansible.errors import AnsibleError
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import missing_required_lib


display = Display()
   
class LookupModule(LookupBase):
   
    def run(self, terms, variables, **kwargs):

        if 'api_key' in kwargs:
            api_key = kwargs['api_key']
        else:
            raise AnsibleError("Please specify a api_key in your request.")
        
        url_getorgs =  "https://api.meraki.com/api/v0/organizations"       
        
        try:
            response_orgs =  requests.get(url_getorgs, headers={'X-Cisco-Meraki-API-Key': api_key})
        except requests.exceptions.HTTPError as err:
            response_orgs = []
            display.debug(err)
            raise AnsibleError("Received HTTP error while requesting org IDs: %s" % to_native(err))
            


        org_results = []
        

        #Search for the Organizations found under the API Key
        if len(response_orgs.json()) > 0:
            for i in range(len(response_orgs.json())) :
                
                if 'org_id' in kwargs:
                    if response_orgs.json()[i]['id'] == kwargs['org_id']:
                        org_results.append(response_orgs.json()[i]['id'])
                else:
                    org_results.append(response_orgs.json()[i]['id'])
        else:    
            raise AnsibleError("Unable to find any Organizations in the response. : Status Code %s" % response_orgs.status_code )
            
              
        #Search Organizations for Devices

        device_results = []

        for id in org_results :
            url_getdevices = "https://api.meraki.com/api/v0/organizations/%s/devices" % id
            response =  requests.get(url_getdevices, headers={'X-Cisco-Meraki-API-Key': api_key})
            if (len(response.json()) == 0) :
                continue
            for device in response.json() :
                device['orgid'] = id
                device_results.append(device)
        
        if (len(device_results) == 0) :
            raise AnsibleError("No devices were found under all existing Org IDs: %s" % org_results )
         
        #TODO: Lookup all Network IDs into a hash table using unique values of networkId found in device_results
        # Parse the device results.
        
        if 'properties' in kwargs:
            return_results = [{k:v for k, v in i.items() if k in kwargs['properties']} for i in device_results]
        else:
            return_results = device_results

        return return_results
