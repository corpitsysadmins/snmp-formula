{%- from "./defaults/map.jinja" import snmp with context -%}

snmp-packages:
  pkg.installed:
    - pkgs: {{ snmp.packages }}

{{ snmpd_conf.path }}:
  file.managed:
    - source: salt://snmp/files/snmpd.conf.jinja
  #  - template: jinja
  #  - context:
  #    config: {{ conf.get('settings', {}) | json }}
    - user: {{ snmpd_conf.user }}
    - group: {{ snmpd_conf.group }}
    - mode: {{ snmpd_conf.mode }}
    #- watch_in:
    #  - service: {{ snmp.service }}


#3 - Create SNMPv3 Read Only User:

#net-snmp-create-v3-user -ro -A Abc12345qwert -X Abc12345qwert -a SHA -x AES prtg-linux

#4 - Additionally we can add to snmpd.conf file the line (depending on the process to be monitored):
#proc <process name>

#5 - Configure firewall
# firewall-cmd --permanent --add-service=snmp
