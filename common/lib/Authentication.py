from keystoneclient.auth import identity
from keystoneclient import session
import os
import sys

class Authentication(object):

    def __init__(self):
        try:
                credentials = {}
                credentials['project_domain_name'] = os.environ['OS_PROJECT_DOMAIN_NAME']
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
