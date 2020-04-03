#! python
'''SNMP agent state module.
This module implements the states related to SNMP.

Version: 0.0.1

TODO:
- everything

Refs:
- https://stackoverflow.com/questions/6819399/remove-user-in-snmp-by-agent
'''

import logging

LOGGER = logging.getLogger(__name__)

def check_file(username, authpass, privpass, file='/etc/snmp/snmpd.conf'):
	if __salt__['file.file_exists'](file):
		if __salt__['snmp.check_user'](username):
			LOGGER.debug('User %s is on the system nothing to', username)
		else:
			add_user = __salt__['snmp.add_user'](username, authpass, privpass)
	else:
		install_package = __salt__['pkg.installed']('net-snmp', **kwargs)
		add_user = __salt__['snmp.add_user'](username, authpass, privpass)
	return None
