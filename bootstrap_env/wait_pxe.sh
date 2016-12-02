#!/bin/bash
str=`for i in $(cobbler system list); do NETBOOT=$(cobbler system report --name $i | awk '/^Netboot/ {print $NF}'); if [[ ${NETBOOT} == True ]]; then echo -e "$i: netboot_enabled : ${NETBOOT}"; fi; done`
while  [ -n "$str" ]; do
  sleep 1;
  str=`for i in $(cobbler system list); do NETBOOT=$(cobbler system report --name $i | awk '/^Netboot/ {print $NF}'); if [[ ${NETBOOT} == True ]]; then echo -e "$i: netboot_enabled : ${NETBOOT}"; fi; done`;
done
