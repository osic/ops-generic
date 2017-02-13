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
# This tool is used to get the list of Virtual Machine on particular compute host
# It prints the List of VMs with their owner's user ID
#
# USAGE
# python VMSforHost.py --host <FQDN of Compute Host>

import sys
import argparse

sys.path.append('../../common/lib/')

# Import needed libraries located in common directory
from nova_client import NovaClient
from keystone_client import KeystoneClient
from authentication import Authentication

class ChildArgParser(argparse.ArgumentParser):
      """
      A class that Inherits the class ArgumentParser
      """
      def validate(self,args):
        """
        A method that validates the arguments.
        """
        if not '.' in args.host:
          print "Please call with the FQDN of the host"
          sys.exit(1)

class VMsforHost(object):
      """
      A base class for the tool.
      """
      def __init__(self):
          """
          Constructor that validates arguments and setup necessary clients needed for the tool
          """
          self.check_arguments()
          self.setup_clients()

      def check_arguments(self):
          """
          A method to validate arguments - Called by Constructor
          """
          parser = ChildArgParser()
          parser.add_argument("--host", required=True, help='FQDN required!')
          self.args=parser.parse_args()
          parser.validate(self.args)

      def setup_clients(self):
          """
          A method to seting up authentication and necessary clients for the tool - Called by Constructor
          """
          auth = Authentication()
          self.novaclient = NovaClient(auth)
          self.keystoneclient = KeystoneClient(auth)

      def print_vms_for_host(self):
          """
          A method to print the VMs specific to the compute host
          """
          vms = self.novaclient.get_vms_for_host(self.args.host)
          users = self.keystoneclient.get_user_dict()
          for vm in vms:
                print "%-45s: %-15s" % (vm.name, users[vm.user_id].name)

def main():

    vmsforhost = VMsforHost()
    vmsforhost.print_vms_for_host()

if __name__ == "__main__":

    main()
