Summary:

This tool is used to check if instances within the same anti-affinity group are violating
the group's policy or not. It can be also used to list the instances in the group id
specified in the argument.

How to use:

source openrc
run script from deployment host

Python requirements:
pip install -r requirements.txt

Run the tool
# Check in all the groups if any of the group is violating the anti-affinity policy or not
python antiaffinity_check.py --all

# List the instances belonging to the affinity group specified
python antiaffinity_check.py --list <server-group-id> --json

# Check if any instances are violating the group's policy or not
python antiaffinity_check.py --check <server-group-id> --json
