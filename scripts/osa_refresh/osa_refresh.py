#!/usr/bin/env python

import os
import sys
from openstack import connection
from openstack import profile
from openstack import utils

# Load shared libraries
sys.path.append('../../common/lib/')
import cleaner_utils

white_list_file = 'osa_whitelist.yml'
project_domain = os.environ['OS_PROJECT_DOMAIN_NAME']
user_domain = os.environ['OS_USER_DOMAIN_NAME']
project = os.environ['OS_PROJECT_NAME']
user = os.environ['OS_USERNAME']
password = os.environ['OS_PASSWORD']
auth_url = os.environ['OS_AUTH_URL']
region = os.environ['OS_REGION_NAME']
client_obj = cleaner_utils.client(project_domain, user_domain, project, user,
                                  password, auth_url, region)
session = client_obj.auth()
#uncomment to enable requst debugging
#utils.enable_logging(debug=True, stream=sys.stdout) 
    
#load whitelist
if os.path.exists(white_list_file):
    cfl = cleaner_utils.config_loader(white_list_file)
    white_list = cfl.load()
else:
    white_list = None   
    print """
             Whitelist file osa_whitelist.yml does not exist. Even if 
             you have no intention of whitelisting anything please 
             create this file as an empty place holder. To use this
             file simply create a yaml formatted file that looks like
             the following (id's/uuid's only):
                 
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
             roles
             security_groups
             routers
          """
    sys.exit(1337) 
     
#clean compute (servers/images/keypairs)
print("\nPreparing to Clean Nova as user %s." % user)
client_obj.clean_nova(session, white_list)

#clean neutron
print("\nPreparing to Clean Neutron as user %s." % user)
client_obj.clean_neutron(session, white_list)
   
#clean cinder
print("\nPreparing to Clean Cinder as user %s." % user)
client_obj.clean_cinder(session, white_list)

#clean identity
print("\nPreparing to Clean Identity as user %s." % user)
client_obj.clean_identity(session, white_list)
