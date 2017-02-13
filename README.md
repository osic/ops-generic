This repo is meant for the operators to use different tools 
to make there tasks/troubleshooting easier.

The structure of the repo is as follows:

ops-generic/
           /ansible/
                   /playbooks
                   /scripts
           /common/
                  /lib/
           /tools/
                 /libvert_compare/
                 /osa_refresh/
                 /vms_for_host/
                 .
                 .
                 .
                 .
           /tests/
       
Ansible playbooks are located under /ansible directory.

Different tools useful for operators are stored under /tools/ directory.

Commonly used libraries are located under /common/lib directory.

Operators can write there own tools and add it under tools directory.
