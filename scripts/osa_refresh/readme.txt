Summary:

This script refreshes a osa environment and cleans up any servers/images/flavors/networks and more that are not white listed 
or required by a default osa install. If you wish to preserve anything simply create a file called osa_whitelist.yml which 
is required to exist anyways whether blank or populated.

osa_whitelist.yml format example (uuid or id only):
                 
                 instances:
                     <uuid>
                     <uuid>
                 
                 You can use the following keywords:
                 
                 instances
                 networks
                 flavors
                 images
                 volumes
                 keypairs
                 users
                 projects
                 domains

How to use:

source openrc
run script from deployment host

Python requirements:

openstacksdk
yaml
