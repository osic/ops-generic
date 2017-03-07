#Summary:

This script will import hosts from the openstack json inventory file "/etc/openstack_deploy/openstack_inventory.json".
To use this script you'll need to rename the example cratonrc file to the name of your choosing "cratonrc" if you will.
You will want to edit this file with the proper information from your craton install. Then proceed to source the file
using the "source" bash command into your bash environment (ex: source cratonrc).

#####To begin using the script, you will need to pass the following flags:

    --load (action for adding inventory)
    --inventory (path to inventory file) (ex: /etc/openstack_deploy/openstack_inventory.json)
    --cloud (id of the cloud you're importing to) (int)
    --region (id of the region you're importing to) (int)
    --ansible-facts (if you add this flag the script will attempt to gather ansible host facts from the hosts) (requires ssh)
     
You can also pass the option --delete to remove all hosts from craton inventory to start fresh. (requires above flags as well) 
You cannot use --load and --delete at the same time. 
