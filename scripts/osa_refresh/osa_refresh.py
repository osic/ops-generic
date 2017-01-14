#!/usr/bin/env python

import os
import sys
import yaml
from openstack import connection
from openstack import profile
from openstack import utils


class config_loader(object):
    
    def __init__(self, white_list_file):
        self.white_list = white_list_file
    
    def load(self):
        with open(self.white_list, 'r') as f:
            data = yaml.load(f)
        return data

class client(object):
    
    def __init__(self, project_domain, user_domain, project, user, password, auth_url, region):
        self.project_domain = project_domain
        self.user_domain = user_domain
        self.project = project
        self.user = user
        self.password = password
        self.auth_url = auth_url
        self.region = region

    def auth(self):
        prof=profile.Profile()
        prof.set_interface('compute', 'internal')
        prof.set_interface('volume', 'internal')
        prof.set_interface('network', 'internal')
        prof.set_interface('image', 'internal')
        prof.set_interface('identity', 'internal')
        conn = connection.Connection(
            profile = prof,
            auth_url = self.auth_url,
            project_domain_name = self.project_domain,
            user_domain_name = self.user_domain,
            project_name = self.project,
            username = self.user,
            password = self.password
           )
        return conn
 
    def clean_nova(self, session, white_list=None):
        nova = session.compute
        s_gen = nova.servers(details=False)
        f_gen = nova.flavors(details=False)
        i_gen = nova.images(details=False)
        k_gen = nova.keypairs()
        if white_list is None:
            wservers = ''
            wflavors = ''
            wimages = ''
            wkeypairs = ''
        else:
            wservers = white_list.get('servers', '')
            wflavors = white_list.get('flavors', '')
            wimages = white_list.get('images', '')
            wkeypairs = white_list.get('keypairs', '')
        wservers = wservers.split()
        wflavors = wflavors.split()
        wimages = wimages.split()
        wkeypairs = wkeypairs.split()
        f_list = []
        for s in s_gen:
            if s.id not in wservers:
                nova.delete_server(s.id)
                print("Server: %s has been marked for deletion." % s.id)
        # Working around weird generator bug which results
        # in bad http request and python exception when
        # iterating through f_gen.
        for f in f_gen:
            f_list.append((f.name,f.id))
        for f_name,f_id in f_list:
            if f_id not in wflavors:        
                nova.delete_flavor(f_id)
                print("Flavor: %s with id %s has been marked for deletion." % (f_name,f_id))
        for i in i_gen:
            if i.id not in wimages:
                nova.delete_image(i.id)
                print("Image: %s has been marked for deletion." % i.id)
        for k in k_gen:
            if k.id not in wkeypairs:
                nova.delete_keypair(k.id)
                print("Keypair: %s has been marked for deletion." % k.id)
        return
        
    def clean_neutron(self, session, white_list=None):
        neutron = session.network
        n_gen = neutron.networks(details=False)
        if white_list is None:
            wnetworks = ''
        else:
            wnetworks = white_list.get('networks', '')
        wnetworks = wnetworks.split()
        for n in n_gen:
            if n.id not in wnetworks:
                network = neutron.find_network(n.id)
                for subnet in network.subnet_ids:
                    ports = neutron.ports(subnet_id=subnet.id)
                    for pid in ports:
                        neutron.delete_port(pid)
                    neutron.delete_subnet(subnet.id)
                neutron.delete_network(n.id)
                print("Network: %s has been marked for deletion." % n.id)       
        return

    def clean_cinder(self, session, white_list=None):
        cinder = session.block_store
        v_gen = cinder.volumes(details=False)
        if white_list is None:
            wvolumes = ''
        else:
            wvolumes = white_list.get('volumes', '')
        wvolumes = wvolumes.split()
        for v in v_gen:
            if v.id not in wvolumes:
                cinder.delete_volume(v.id)
                print("Volume: %s has been marked for deletion." % n.id)
        return
        
    def clean_identity(self, session, white_list=None):
        ident = session.identity
        u_gen = ident.users()
        p_gen = ident.projects()
        d_gen = ident.domains()
        r_gen = ident.roles()
        if white_list is None:
            wusers = ''
            wprojects = ''
            wdomains = ''
            wroles = ''
        else:
            wusers = white_list.get('users', '')
            wprojects = white_list.get('projects', '')
            wdomains = white_list.get('domains', '')
            wroles = white_list.get('roles', '')
        wusers = wusers.split()
        wprojects = wprojects.split()
        wdomains = wdomains.split()
        wroles = wroles.split()

        protected_users = ['keystone','glance','stack_domain_admin','neutron',
                           'nova','cinder','admin','swift','dispersion',
                           'heat']
        protected_projects = ['service','admin']
        protected_domains = ['Default', 'heat']
        protected_roles = ['heat_stack_user','swiftoperator','ResellerAdmin',
                           'admin','_member_','heat_stack_owner']
        for u in u_gen:
            if u.id not in wusers and u.name not in protected_users:
                ident.delete_user(u.id)
                print("User: %s with alias %s has been marked for deletion." % (u.id,u.name))
        for p in p_gen:
            if p.id not in wprojects and p.name not in protected_projects:
                ident.delete_project(p.id)
                print("Project: %s with alias %s has been marked for deletion." % (p.id,p.name))
        for d in d_gen:
            if d.id not in wdomains and d.name not in protected_domains:
                ident.delete_domain(d.id)
                print("Domain: %s with alias %s has been marked for deletion." % (d.id,d.name))
        for r in r_gen:
            if r.id not in wroles and r.name not in protected_roles:
                ident.delete_role(r.id)
                print("Role: %s with alias %s has been marked for deletion." % (r.id,r.name))

if __name__ == '__main__':
    
    white_list_file = 'osa_whitelist.yml'
    project_domain = os.environ['OS_PROJECT_DOMAIN_NAME']
    user_domain = os.environ['OS_USER_DOMAIN_NAME']
    project = os.environ['OS_PROJECT_NAME']
    user = os.environ['OS_USERNAME']
    password = os.environ['OS_PASSWORD']
    auth_url = os.environ['OS_AUTH_URL']
    region = os.environ['OS_REGION_NAME']
    client_obj = client(project_domain, user_domain, project, user, password, auth_url, region)
    session = client_obj.auth()
    #utils.enable_logging(debug=True, stream=sys.stdout) 
    
    #load whitelist
    if os.path.exists(white_list_file):
        cfl = config_loader(white_list_file)
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
              """
        sys.exit(1337) 
   
    #clean compute (servers/images/keypairs)
    client_obj.clean_nova(session, white_list)

    #clean neutron
    client_obj.clean_neutron(session, white_list)
   
    #clean cinder
    client_obj.clean_cinder(session, white_list)

    #clean identity
    client_obj.clean_identity(session, white_list)
