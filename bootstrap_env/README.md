Bootstrap a cloud environment for Openstack installation
========================================================

Intro
-----
This is part of the one button Openstack installation for OSIC clouds.

Usage
-----

Clone repo:

       git clone https://github.com/osic/ops-generic /opt/ops-generic
       cd /opt/ops-generic/bootstrap_env

export environment variable:

       export ANSIBLE_HOST_KEY_CHECKING=False

bootstrap the environment: (when propmpt for passowrd enter: cobbler)

       ansible-playbook -i inventory/static-inventory.yml create-network-interfaces.yml --forks 22 --ask-pass

