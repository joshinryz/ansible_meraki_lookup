# Meraki Lookuip Plugin

This plugin was designed to query Meraki API and get a list of devices to use as a variable in Playbooks.
Properties that are returned can be filter my providing a list to the lookup plugin.

## Prerequisites

The lookup plugin works with python2 and python3.


### Configuration
Place the file `ldap_inventory.py` into your base folder under `.\plugins\lookup\`
Configure you ansible.cfg with the Lookup plugin path.


Example `playbook.yaml` :

```(yaml)
---
hosts: localhost
vars:
  myproperties :
    - name
    - serial
  meraki_inventory: "{{ lookup('meraki_inventory',api_key=myapikey, org_id='12312312312', properties=myproperties, wantlist=True )}}"
tasks:
  - name: Show The meraki data
    debug:
      var: meraki_inventory
```
**api_key** - API Key. Please vault this value.

**org_id** - This is yoru ORG ID in the Meraki portal used for API queries.

**properties** - These are the properties that will be returned. This is not required and is a filter. Not including will return all properties.

**wantlist** - You can force lookup to return a list by using wantlist=True

