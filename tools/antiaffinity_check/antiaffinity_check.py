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
# group are violating the group's policy or not. It can be also used to
# list the instances in the group id specified in the argument.
#
# USAGE
#
# Check in all the groups if any of the group is violating the
# anti-affinity policy or not
# python antiaffinity_check.py --all
#
# List the instances belonging to the affinity group specified
# python antiaffinity_check.py --list <server-group-id> --json
#
# Check if any instances are violating the group's policy or not
# python antiaffinity_check.py --check <server-group-id> --json
#

import sys
import argparse
import json
import prettytable

sys.path.append('../../common/lib/')

# Import needed libraries located in common directory
from nova_client import NovaClient
from keystone_client import KeystoneClient
from authentication import Authentication


class AntiaffinityCheck(object):
    """
    A base class for the tool.
    """

    def __init__(self):
        """
        Constructor that validates arguments and setup necessary
        clients needed for the tool
        """
        self.check_arguments()
        self.setup_clients()

    def decider(self):
        """
        A decider method based on the argument passed.
        """
        if self.args.check:
            output = self.novaclient.test_group_duplicates(self.args.check)
            if output and self.args.json:
                print json.dumps(output)
            elif output and not self.args.json:
                print "Anti-affinity rules violated in Server Group:",\
                    self.args.check
                self.print_table(output)
            elif not output:
                print "No anti-affinity rules violated for Server Group:",\
                    self.args.check
        if self.args.list:
            output = self.novaclient.get_group_detail(self.args.list)
            if output and self.args.json:
                print json.dumps(output)
            elif output and not self.args.json:
                self.print_table(output)
            elif not output:
                print "Server Group", self.args.list, "empty or does "\
                    "not have an anti-affinity policy set."
        if self.args.all:
            self.novaclient.check_all(self.args.json)

    def check_arguments(self):
        """
        A method to validate arguments - Called by Constructor
        """
        parser = argparse.ArgumentParser(
            description='Nova Server Group anti-affinity rule checker')
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '--check',
            type=str,
            help='Validate the specified Server Group')
        group.add_argument(
            '--list',
            type=str,
            help='List instances and their hypervisors\
            for a given Server Group'
        )
        group.add_argument(
            '--all',
            action='store_true',
            help='Check all server groups')
        parser.add_argument('--json', action='store_true', help='Output JSON')
        self.args = parser.parse_args()

    def setup_clients(self):
        """
        A method to seting up authentication and necessary clients for
        the tool - Called by Constructor
        """
        # This dance can be slightly a bit better, but for now, let's just
        # keep it operating like it was before. This will get a configuration
        # based on envvars. If the user has a clouds.yaml file with more than
        # one cloud defined, the user will need to define OS_CLOUD and maybe
        # OS_REGION_NAME to indicate which one
        config = os_client_config.OpenStackConfig()
        cloud_config = config.get_one_cloud()
        # As a further TODO - we should get rid of NovaClient and
        # KeystoneClient altogether and add whatever they don't have to shade.
        self.novaclient = NovaClient(cloud_config)
        self.keystoneclient = KeystoneClient(cloud_config)

    def create_table(self, fields):
        """
        Boilerplate for PrettyTable
        """
        table = prettytable.PrettyTable(fields, caching=False)
        table.align = 'l'
        return table

    def print_table(self, output):
        """
        Print out a table of instances
        """
        table = self.create_table(
            ['Instance ID', 'Instance Name', 'Hypervisor'])
        for instance in output:
            table.add_row([instance['id'],
                           instance['name'],
                           instance['hypervisor']])
        print table


def main():

    antiaffinitycheck = AntiaffinityCheck()
    antiaffinitycheck.decider()


if __name__ == "__main__":

    main()
