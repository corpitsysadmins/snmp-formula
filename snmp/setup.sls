{%- from "./defaults/map.jinja" import snmp with context -%}

snmp-packages:
  pkg.installed:
    - pkgs: {{ snmp.packages|json }}

{{ snmp.snmpd_conf.path }}:
  file.managed:
    - source: salt://snmp/files/snmpd.conf.jinja
    - template: jinja
    - context: {{ snmp|json }}
    - user: {{ snmp.snmpd_conf.user }}
    - group: {{ snmp.snmpd_conf.group }}
    - mode: {{ snmp.snmpd_conf.mode }}
    - require:
      - snmp-packages
    - require_in:
      - service: {{ snmp.service_name }}
    - watch_in:
      - service: {{ snmp.service_name }}

{%- if snmp.v3users is defined %}
{%- for v3user, v3user_data in snmp.v3users.items() %}
{{ v3user }}:
  snmp.user_exists:
{%- for v3user_param, v3user_value in v3user_data.items() %}
    - {{ v3user_param }}: {{ v3user_value }}
{%- endfor %}
    - require:
      - snmp-packages
    - require_in:
      - service: {{ snmp.service_name }}
    - watch_in:
      - service: {{ snmp.service_name }}
{%- endfor %}
{%- endif %}

{{ snmp.service_name }}:
  service.running:
    - enable: true
