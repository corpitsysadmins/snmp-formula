{%- from "./defaults/map.jinja" import snmp with context -%}

snmp-packages:
  pkg.installed:
    - pkgs: {{ snmp.packages }}


2 - Backup the original snmpd.conf and create a new one with the bellow content:

view    systemview    included   .1.3.6.1
syslocation Unknown (edit /etc/snmp/snmpd.conf)
syscontact Root <root@localhost> (configure /etc/snmp/snmp.local.conf)
dontLogTCPWrappersConnects yes

3 - Create SNMPv3 Read Only User:

net-snmp-create-v3-user -ro -A Abc12345qwert -X Abc12345qwert -a SHA -x AES prtg-linux

4 - Additionally we can add to snmpd.conf file the line (depending on the process to be monitored):
proc <process name>

5 - Configure firewall
# firewall-cmd --permanent --add-service=snmp