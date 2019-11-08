# Ansible Meraki Inventory Plugin

This plugin was designed to query Meraki's API and get a list of devices to use as an inventory.
Groups are auto generated off of which Network a device belongs to. So for example `New York Office` would create the following inventory :
```
    "all": {
        "children": [
            "organization_id"
        ]
    },
    "organization_id": {
        "children": [
            "new_york_office"
        ]
    },
    "new_york_office": {
        "hosts": [
            "switch1"
        ]
    }
```

## Prerequisites

The Meraki inventory works with python2 and python3.

### Configuration
Place the file `meraki_inventory.py` into your base folder under `.\plugins\inventory\`

Create a file that ends with `meraki.yaml` in your base directory. 
It is recommended you vault the entire file (until ansible supports vaulted strings in config files) `ansible-vault edit company_meraki.yaml`

Example `company_meraki.yaml` :
```(yaml)
---
plugin: meraki_inventory
api_key: '234klj3223423423432'
network_filter:  ''
```
Additional options:
```(yaml)
exclude_groups: "windows_group1,windows_group2"
exclude_hosts: "hostname1,hostname2"
```
 
**api_key** - This is the API Key with permissions to Read your domain.

**exclude_hosts** - exclude a list of hosts from being included in the inventory. This will match substrings.

**exclude_groups** - exclude a list of groups from being included in the inventory. This wil match substrings.



### Testing the inventory with Ansible

`ansible-inventory -i meraki.yaml --list`

`ansible-inventory -i meraki.yaml --list --vault-id=@prompt` (when vaulted)

** Running a playbook **

`ansible-playbook -i meraki.yaml adhoc.yaml --vault-id@prompt `
