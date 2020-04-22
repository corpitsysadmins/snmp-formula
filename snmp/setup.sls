{%- from "./defaults/map.jinja" import snmp_data with context -%}

snmp-packages:
  pkg.installed:
    - pkgs: {{ snmp_data.packages|json }}

{{ snmp_data.snmpd_conf.path }}:
  file.managed:
    - source: salt://snmp/files/snmpd.conf.jinja
    - template: jinja
    - context: {{ snmp_data|json }}
    - user: {{ snmp_data.snmpd_conf.user }}
    - group: {{ snmp_data.snmpd_conf.group }}
    - mode: {{ snmp_data.snmpd_conf.mode }}
    - require:
      - snmp-packages
    - require_in:
      - service: {{ snmp_data.service_name }}
    - watch_in:
      - service: {{ snmp_data.service_name }}

{%- if snmp_data.v3users is defined %}
{%- for v3user, v3user_data in snmp_data.v3users.items() %}
{{ v3user }}:
  snmp.user_exists:
{%- for v3user_param, v3user_value in v3user_data.items() %}
    - {{ v3user_param }}: {{ v3user_value }}
{%- endfor %}
    - service_name: {{ snmp_data.service_name }}
    - snmpd_conf_path: {{ snmp_data.snmpd_conf.path }}
    - require:
      - snmp-packages
    - require_in:
      - file: {{ snmp_data.snmpd_conf.path }}
    - watch_in:
      - service: {{ snmp_data.service_name }}
{%- endfor %}
{%- endif %}

{{ snmp_data.service_name }}:
  service.running:
    - enable: true
