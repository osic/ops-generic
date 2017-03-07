#! /usr/bin/env python

import os
import sys
import json
import requests
import argparse
import time

class osa_import(object):

    def __init__(self, inventory, region, cloud):
        self.inv = inventory
        self.region = region
        self.cloud = cloud
        self.headers = {}
        self.headers['X-Auth-User'] = os.environ['OS_USERNAME']
        self.headers['X-Auth-Project'] = os.environ['OS_PROJECT_ID']
        self.headers['X-Auth-Token'] = os.environ['OS_PASSWORD']
        self.headers['Content-type'] = 'application/json'

    def query_craton(self, endpoint, headers, next_link=None):
        url = ('%s/%s' % (os.environ['CRATON_URL'], endpoint))
        try:
            if next_link is not None:
                url = (next_link)
            r = requests.get(
                url = url,
                headers=self.headers
                )
        except:
            print("\nOops, something went wrong. Is Craton API up?\n")
            sys.exit()

        return r.text
   
    def delete_host(self, host_id):
        url = ('%s/hosts/%s' % (os.environ['CRATON_URL'], host_id))
        try:
            r = requests.delete(
                url = url,
                headers=self.headers
                )
        except:
            print("\nOops, something went wrong. Is Craton API up?\n")
            sys.exit()

        return r.status_code

    def get_hosts(self, next_link=None):
        baremetal_hosts = []
        container_hosts = []
        unknown_hosts = []
        while True:
            #Sleep 1 second to not overwhelm Craton API.
            time.sleep(1)
            data = json.loads(self.query_craton(('hosts?limit=100&region_id=%s'
                               % self.region), self.headers, next_link))
            try:
                next_link = [s for s in data.get('links', None) if 'next' in s.get('rel',
                            None)][0].get('href')
            except IndexError:
                break
            for k,v in data.items():
                for item in v:
                    if item.get('id', None) is not None:
                        host_var = {}
                        host_var['name'] = item.get('name')
                        host_var['ip_address'] = item.get('ip_address')
                        host_var['id'] = item.get('id')
                        host_var['parent_id'] = item.get('parent_id', None)
                        host_var['device_type'] = d = item.get('device_type')
                        if 'baremetal' in d:
                            baremetal_hosts.append(host_var)
                        elif 'container' in d:
                            container_hosts.append(host_var)
                        else:
                            unknown_hosts.append(host_var)

        #returns id of hosts.
        return baremetal_hosts,container_hosts,unknown_hosts
             

    def insert_craton(self, endpoint, data, method='post'):
        url = ('%s/%s' % (os.environ['CRATON_URL'], endpoint))
        try:
            if 'post' in method:
                r = requests.post(
                    url = url,
                    data=json.dumps(data),
                    headers=self.headers
                    )
            if 'put' in method:
                r = requests.put(
                    url = url,
                    data=json.dumps(data),
                    headers=self.headers
                    )
        except:
            print("\nOops, something went wrong. Is Craton API up?\n")
            sys.exit()

        return r.status_code, r.text
    

    def gen_baremetal(self):
        baremetal_list = []
        for k, v in self.inv['_meta']['hostvars'].items():
            if v.get('is_metal', False):
                dev = {}
                dev['name'] = k
                dev['ip_address'] = v['ansible_ssh_host']
                dev['region_id'] = int(self.region)
                dev['cloud_id'] = int(self.cloud)
                dev['device_type'] = 'baremetal'
                baremetal_list.append(dev)
        return baremetal_list


    def gen_containers(self):
        b,c,u = self.get_hosts()
        parents = b
        container_list = []
        for k, v in self.inv['_meta']['hostvars'].items():
            for parent in parents:
                pname = parent.get('name', None)
                pid = parent.get('id', None)
                if v.get('is_metal', False) is False and pname in v['physical_host']:
                    dev = {}
                    dev['name'] = k
                    dev['ip_address'] = v['ansible_ssh_host']
                    dev['region_id'] = int(self.region)
                    dev['cloud_id'] = int(self.cloud)
                    dev['device_type'] = 'container'
                    dev['parent_id'] = pid
                    container_list.append(dev)
        return container_list

    def import_vars(self, host):
        hname = host.get('name')
        hid = host.get('id')
        var_data = self.inv['_meta']['hostvars'].get(hname, None)
        s,t = self.insert_craton(('hosts/%s/variables' % hid), var_data,
                                method = 'put')
        return s


    def import_ansible_facts(self, host):
        from subprocess import PIPE
        from subprocess import Popen
        hname = host.get('name')
        hip = host.get('ip_address')
        hid = host.get('id')
        cmd = ("ansible -i %s, 'all' -m setup" % hip)
        proc = Popen(cmd, shell=True, stderr=PIPE, stdout=PIPE).stdout.read()
        facts = proc.split('=>')[1]
        var_data = json.loads(facts)['ansible_facts']
        s,t = self.insert_craton(('hosts/%s/variables' % hid), var_data,
                                method = 'put')
        return s


    def label_hosts(self, labels, host):
        hname = host.get('name')
        hid = host.get('id')
        var_data = {"labels": labels}
        if 'nova' in hname:
            var_data = {'labels': labels + ['nova']}
        if 'glance' in hname:
            var_data = {'labels': labels + ['glance']}
        if 'galera' in hname:
            var_data = {'labels': labels + ['galera']}
        if 'swift' in hname:
            var_data = {'labels': labels + ['swift']}
        if 'cinder' in hname:
            var_data = {'labels': labels + ['cinder']}
        if 'keystone' in hname:
            var_data = {'labels': labels + ['keystone']}
        if 'neutron' in hname:
            var_data = {'labels': labels + ['neutron']}
        if 'heat' in hname:
            var_data = {'labels': labels + ['heat']}
        if 'rabbit' in hname:
            var_data = {'labels': labels + ['rabbit']}
        s,t = self.insert_craton(('hosts/%s/labels' % hid), var_data, 
                                method = 'put')
        return s

    def action_status(self, status, item, host):
        if s == 200:
            msg = ('Action %s for host %s was successful.' %
                    (item, host.get('name', None)))
        elif s == 201:
            msg = ('Create action %s for host %s was successful.' %
                    (item, host.get('name', None)))
        elif s == 204:
            msg = ('Delete action %s for host %s was successful.' %
                    (item, host.get('name', None)))
        elif s == 409:
            msg = ('Action %s for host %s failed (Duplicate entry).' %
                    (item, host.get('name', None)))
        else:
            msg = ('Action %s for host %s has failed (Unknown reason).' %
                    (item, host.get('name', None)))
        return msg

if __name__ == '__main__':


    #check for environment vars
    try:
        os.environ['OS_USERNAME']
        os.environ['OS_PASSWORD']
        os.environ['CRATON_URL']
        os.environ['OS_PROJECT_ID']
    except KeyError:
        print """

 Please source your craton RC file first. 

 The following OS variables are missing:

 OS_USERNAME
 OS_PASWORD
 OS_PROJECT_ID
 CRATON_URL
                
"""
        sys.exit()


    #call argparse
    parser = argparse.ArgumentParser(description="""Import OSA iventory into
                                    Craton.""")
    parser.add_argument('--inventory', help='--inventory inventory file.',
                        required=True)
    parser.add_argument('--cloud', help='--cloud <cloud_id> (int)',
                        required=True)
    parser.add_argument('--region', help='--region <region_id> (int).',
                        required=True)
    parser.add_argument('--load', help='Load inventory into Craton.',
                        action='store_true')
    parser.add_argument('--delete', help='Delete all hosts from Craton.',
                        action='store_true')
    parser.add_argument('--ansible-facts', help='Gather ansible host facts.',
                        action='store_true')    
    args = parser.parse_args()
    cloud = args.cloud
    region = args.region
    invfile = args.inventory
    host_import = args.load
    truncate = args.delete
    ansible_facts = args.ansible_facts

    if host_import and truncate:
        print('Please only choose one action at a time.')
        sys.exit()
    if host_import is False and truncate is False:
        print('No action was provided. Plase specify --load or --truncate')
        sys.exit()
    
    #load inventory
    try:
        with open(os.path.expanduser(invfile)) as f:
            inventory = json.loads(f.read())
    except IOError:
        print """ OSA inventory file not provided. Please pass the path 
 of the file as the first argument to this script.
"""

    #init osa class
    osa = osa_import(inventory, region, cloud)


    #import baremetal
    if host_import:
        print("\n Importing baremetal hosts into Craton from inventory.\n")
        for host in osa.gen_baremetal():
            s,t = osa.insert_craton('hosts', host)
            response = osa.action_status(s, 'host', host)
            print response

    #import containers
    if host_import:
        print("\n Importing container hosts into Craton from inventory.\n")
        for host in osa.gen_containers():
            s,t = osa.insert_craton('hosts', host)
            response = osa.action_status(s, 'host', host)
            print response

    #import variables for hosts and create labels
    if host_import:
        print("\n Importing host variables into Craton from inventory.\n")
        b,c,u = osa.get_hosts()
        all_hosts = b + c
        for host in b:
            s = osa.label_hosts(['baremetal', 'on-metal','physical'], host)
            response = osa.action_status(s, 'label', host)
            print response
        for host in c:
            s = osa.label_hosts(['container', 'lxc', 'virtual'], host)
            response = osa.action_status(s, 'label', host)
            print response
        for host in all_hosts:
            s = osa.import_vars(host)
            response = osa.action_status(s, 'variable', host)
            print response
            if ansible_facts:
                s = osa.import_ansible_facts(host)
                response = osa.action_status(s, 'ansible_facts', host)
                print response

    #delete all hosts from craton inventory
    if truncate:
        print("\n Deleting all hosts from Craton inventory.\n")
        b,c,u = osa.get_hosts()
        #delete all containers first (required to delete parent post
        for host in c:
            s = osa.delete_host(host.get('id', None))
            response = osa.action_status(s, 'host', host)
            print response

        #delete all baremetal hosts
        for host in b:
            s = osa.delete_host(host.get('id', None))
            response = osa.action_status(s, 'host', host)
            print response
