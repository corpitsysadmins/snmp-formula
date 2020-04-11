#! python
'''SNMP agent execution module.
This module implements the execution actions related to SNMP.

Version: 0.0.1

TODO:
- everything

Refs:
- https://stackoverflow.com/questions/6819399/remove-user-in-snmp-by-agent
'''

import logging

LOGGER = logging.getLogger(__name__)


def check_user(username, snmpd_conf_path = '/etc/snmp/snmpd.conf'):
	'''Check user list
	Finds a user in the list of registered users. Returns true if is in the list, false otherwise.
	'''

	with open(snmpd_conf_path, 'r') as f:
		for	line in f.readlines():
			if username in line:
				LOGGER.debug('User %s is enabled', username)
				return True
		LOGGER.debug('User %s not found in the system', username)
		return False

def add_user(username, authpass, privpass, service_name = 'snmpd' read_only = True, auth_hash_sha = True, encryption_aes = True):
	'''Add user
	Adds a user to the user list. Returns None.

	Parameters:
	- username: the user name
	- authpass: snmpv3 authentication password
	- privpass: snmpv3 privacy password

	'''
	__salt__['service.stop'](service_name)

	parameters = []

	if read_only:
		parameters.append('-ro')
	parameters += ['-A', authpass]
	parameters += ['-a', 'SHA' if auth_hash_sha else 'MD5']
	parameters += ['-X', privpass]
	parameters += ['-x', 'AES' if encryption_aes else 'DES']
	parameters += [username]
	LOGGER.debug('Adding user %s ', username)
	command_str = __salt__['cmd.run']('net-snmp-create-v3-user ' + ' '.join(parameters))

	__salt__['service.start'](service_name)

def del_user(username, service_name = 'snmpd', snmpd_conf_path = '/etc/snmp/snmpd.conf', snmpd_conf_var_path = '/var/lib/net-snmp/snmpd.conf'):
	'''Delete user
	Removes a user from the user list. Returns None.
	'''
	LOGGER.debug('Removing user %s ', username)
	__salt__['service.stop'](service_name)

	with open (snmpd_conf_path, 'r') as f:
		etc_lines = f.readlines()
	with open (snmpd_conf_var_path, 'r') as f1:
		var_lines = f1.readlines()

	with open (snmpd_conf_path, 'w') as f:
		for line in etc_lines:
			if username not in line.strip("\n"):
				f.write(line)
	with open (snmpd_conf_var_path, 'w') as f1:
		for line in var_lines:
			if 'usmUser' not in line.strip("\n"):
				f1.write(line)

	__salt__['service.start'](service_name)
