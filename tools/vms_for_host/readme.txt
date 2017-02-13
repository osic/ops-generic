Summary:

This script returns the list of Virtual instances based on the compute host along with the owner of the virtual instance.
Name of the compute host with full FQDN needs to be passed as an argument to the script.

How to use:

source openrc
run script from deployment host

Python requirements:
pip install -r requirements.txt 

Run the tool
python vms_for_host.py --host <FQDN of the compute host>

For Example:
python vms_for_host.py --host compute08.local.lan
