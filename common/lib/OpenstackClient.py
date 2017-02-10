from openstackclient import client as openstack_client
from keystoneclient.auth import identity
from keystoneclient import session
import os


class OpenstackClient(object):

    def __init__(self,auth):
        self.openstack = openstack_client.Client('2',session=auth.sess)

