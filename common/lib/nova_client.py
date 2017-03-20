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
import os
from collections import Counter


class NovaClient(object):
    """
    Nova connection base class
    """

    def __init__(self, config):
        """
        Constructor for creating a nova object

        :param config: `os_client_config.cloud_config.CloudConfig` object
        """
        self.nova = config.get_legacy_client('compute')

    def nova_vm_list(self):
        """
        Return the list of Virtual Machines
        """
        return self.nova.servers.list()

    def get_vms_for_host(self, host):
        """
        Return the list of Virtual Machines along with their owner
        based on the compute host specified
        """
        vms = []
        for server in self.nova.servers.list(search_opts={'all_tenants': 1}):
            if host == getattr(server, 'OS-EXT-SRV-ATTR:hypervisor_hostname'):
                vms.append(server)
        return vms

    def get_server(self, serverid):
        """
        Return Server object
        """
        return self.nova.servers.get(serverid)

    def get_all(self):
        """
        Get a list of all Server Groups
        """
        server_groups = self.nova.server_groups.list(all_projects=True)
        return server_groups

    def get_group_members(self, server_group_id):
        """
        Return list of instance UUIDs present in a Server Group
        """
        server_group = self.nova.server_groups.get(server_group_id)
        if 'anti-affinity' in server_group.policies:
            return server_group.members
        else:
            return False

    def get_hypervisors(self, uid_list):
        """
        Return a dict with hypervisors and names given a list of server uids
        """
        ret = []
        for uid in uid_list:
            instance = self.get_server(uid)
            hypervisor = getattr(instance,
                                 'OS-EXT-SRV-ATTR:hypervisor_hostname'
                                 .split('.')[0])
            ret.append({'id': uid,
                        'name': instance.name,
                        'hypervisor': hypervisor})
        return ret

    def get_group_detail(self, server_group_id):
        """
        Output detail on Server Group instances and their hypervisors
        """
        group_members = self.get_group_members(server_group_id)
        if group_members:
            output = self.get_hypervisors(group_members)
            return output
        else:
            return False

    def test_group_duplicates(self, server_group_id):
        """
        Evaluate whether any instances in a SG
        have been scheduled to the same hypervisor
        """
        group_members = self.get_group_members(server_group_id)
        if group_members:
            hypervisors = []
            instances = self.get_hypervisors(group_members)
            for instance in instances:
                instance['server_group_id'] = server_group_id
                hypervisors.append(instance['hypervisor'])
            dupes = [k for k, v in Counter(hypervisors).items() if v > 1]
            if dupes:
                instance_dupes = [instance for instance in instances
                                  if instance['hypervisor'] in dupes]
                return instance_dupes
            else:
                return False
        else:
            return False

    def check_all(self, json):
        """
        Check all server groups for violations
        """
        groups = self.get_all()
        merged_output = []
        for group in groups:
            output = self.test_group_duplicates(group.id)
            if output and self.json:
                merged_output += output
            elif output and not self.json:
                print "Anti-affinity rules violated in Server Group:",\
                    group.id
                print_table(output)
        if json and merged_output:
            print json.dumps(merged_output)
        else:
            print "No groups violated anti-affinity policy"
