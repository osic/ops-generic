# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# This tool is used to check if instances within the same anti-affinity group are violating
# the group's policy or not. It can be also used to list the instances in the group id 
# specified in the argument.
#

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client

class KeystoneClient(object):
    """
    Keystone connection base class
    """
    def __init__(self,auth):
        """
        Constructor for creating a keystone object
        """
        self.keystone = client.Client(session=auth.sess)

    def project_list(self):
        """
        Returns the list og project ids
        """
        return self.keystone.projects.list()
    
    def get_user_dict(self):
        """
        Returns list of users in dictionary format
        """
        _users_hash = {}
        users = self.keystone.users.list()
        for user in users:
           _users_hash[user.id] = user
        return _users_hash

