from novaclient import client as nova_client
from keystoneclient.auth import identity
from keystoneclient import session
import os


class NovaClient(object):

    def __init__(self,auth):
        self.nova = nova_client.Client('2',session=auth.sess)

    def nova_vm_list(self):
        return self.nova.servers.list()

    def get_vms_for_host(self,host):
        vms = []
        for server in self.nova.servers.list(search_opts={'all_tenants': 1}):
            if host == getattr(server, 'OS-EXT-SRV-ATTR:hypervisor_hostname'):
                vms.append(server)
        return vms

