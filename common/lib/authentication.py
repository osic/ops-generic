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
# This tool is used to check if instances within the same anti-affinity
# group are violating  the group's policy or not. It can be also used to
# list the instances in the group id
# specified in the argument.
#
#

from keystoneclient.auth import identity
from keystoneclient import session
import os
import sys


class Authentication(object):
    """
    Authentication base class
    """

    def __init__(self):
        """
        Constructor for authenticating openrc credentials
        """
        try:
            credentials = {}
            credentials['project_domain_name'] =\
                os.environ['OS_PROJECT_DOMAIN_NAME']
            credentials['user_domain_name'] = os.environ['OS_USER_DOMAIN_NAME']
            credentials['project_name'] = os.environ['OS_PROJECT_NAME']
            credentials['username'] = os.environ['OS_USERNAME']
            credentials['password'] = os.environ['OS_PASSWORD']
            credentials['auth_url'] = os.environ['OS_AUTH_URL']
            auth = identity.v3.Password(**credentials)
            self.sess = session.Session(auth=auth)
            self.authenticated = True
        except KeyError as k:
            self.authenticated = False
            print "Please source the openrc file"
            sys.exit(1)
