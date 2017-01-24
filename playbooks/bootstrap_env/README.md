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

       ansible-playbook -i inventory/static-inventory.yml bootstrap_env_osa.yml --forks 22 --ask-pass


Run into pxebooting problems!
-----------------------------

Attach to the osic-prep container

       lxc-attach -n osic-prep

check quick which servers didn't pxeboot with this command

       for i in $(cobbler system list); do
         NETBOOT=$(cobbler system report --name $i | awk '/^Netboot/ {print $NF}')
         if [[ ${NETBOOT} == True ]]; then
         echo -e "$i: netboot_enabled : ${NETBOOT}"
         fi
       done

Create a tmp.csv file from the ilo.csv and then **leave the lines with only the unpxebooted servers from the last command**

       cd /root
       cp ilo.csv tmp.csv
       vi tmp.csv

set those servers to boot from network and reboot them: (**change PASSWORD to the Ilo password provided**)

       for i in $(cat /root/tmp.csv); do
         NAME=$(echo $i | cut -d',' -f1)
         IP=$(echo $i | cut -d',' -f2)
         echo $NAME
         ipmitool -I lanplus -H $IP -U root -P PASSWORD chassis bootdev pxe
         sleep 1
         ipmitool -I lanplus -H $IP -U root -P PASSWORD power reset
       done

