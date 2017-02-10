from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

class KeystoneClient(object):

    def __init__(self,auth):
        self.keystone = client.Client(session=auth.sess)

    def project_list(self):
        return self.keystone.projects.list()
    
    def get_user_dict(self):
        _users_hash = {}
        users = self.keystone.users.list()
        for user in users:
           _users_hash[user.id] = user
        return _users_hash

