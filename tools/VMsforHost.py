# This tool is used to get the list of Virtual Machine on particular compute host
# It prints the List of VMs with their owner's user ID
# USAGE
# python VMSforHost.py --host <FQDN of Compute Host>

import sys
sys.path.append('../common/')

# Import needed libraries located in common directory
from ArgParser import ArgParser
from NovaClient import NovaClient
from KeystoneClient import KeystoneClient
from Authentication import Authentication

# Inherit the Class ArgParser and override method validate according to your requirements
class childArgParser(ArgParser):
      def validate(self):
        if not '.' in self.getArgs().host:
          print "Please call with the FQDN of the host"
          sys.exit(1)

class VMsforHost(object):

      # A constructor that validates arguments and setup necessary clients needed for the tool
      def __init__(self):
          self.checkArguments()
          self.setupClients()

      # A method to validate arguments - Called by Constructor
      def checkArguments(self):
          parser = childArgParser()
          parser.addRule("--host",True,"Provide the hostname")
          parser.parseArgs()
          parser.validate()
          self.parser = parser

      # A method to seting up authentication and necessary clients for the tool - Called by Constructor
      def setupClients(self):
          auth = Authentication()
          self.novaclient = NovaClient(auth)
          self.keystoneclient = KeystoneClient(auth)

      # Call this method to print the VMs specific to the compute host
      def printVMsforHost(self):
          vms = self.novaclient.get_vms_for_host(self.parser.getArgs().host)
          users = self.keystoneclient.get_user_dict()
          for vm in vms:
                print "%-45s: %-15s" % (vm.name, users[vm.user_id].name)

def main():
    vmsforhost = VMsforHost()
    vmsforhost.printVMsforHost()

if __name__ == "__main__":
    main()
