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
	''' (str, str) -> bool
	Check user list
	Finds a user in the list of registered users. Returns true if is in the list, false otherwise.

	>>>check_user('john', snmpd_conf_path = snmpd_conf_path)
	True
	>>>check_user('jane', snmpd_conf_path = snmpd_conf_path)
	False
	'''

	with open(snmpd_conf_path, 'r') as f:
		for	line in f.readlines():
			if username in line:
				LOGGER.debug('User %s is enabled', username)
				return True
		LOGGER.debug('User %s not found in the system', username)
		return False

def add_user(username, authpass, privpass, service_name = 'snmpd', read_only = True, auth_hash_sha = True, encryption_aes = True):
	'''Add user

	Adds param username to snmpv3 list of users. Uses the net-snmp-create-v3-user which accept the following parameters:
		-ro    creates a user with read-only permissions
		-A authpass
              specifies the authentication password
		-a MD5|SHA
              specifies the authentication password hashing algorithm
		-X privpass
              specifies the encryption password
 		-x DES|AES
              specifies the encryption algorithm


	This function returns None.

	Parameters:
	- username: the user name.
	- authpass: snmpv3 authentication password.
	- privpass: snmpv3 privacy password.
	- service_name = 'snmpd': Systemd service name.
	- snmpd_conf_path = '/etc/snmp/snmpd.conf': SNMP service main configuration file

	'''
 	service_running = __salt__['service.status'](service_name)
	# Adding logging
	LOGGER.debug('Service %s is running' if service_running else 'Service %s is not running', service_name)
 	if service_running:
		# Adding logging
 		LOGGER.debug('Stopping service %s', service_name)
 		__salt__['service.stop'](service_name)

	parameters = []

	if read_only:
		parameters.append('-ro')
	parameters += ['-A', authpass]
	parameters += ['-a', 'SHA' if auth_hash_sha else 'MD5']
	parameters += ['-X', privpass]
	parameters += ['-x', 'AES' if encryption_aes else 'DES']
	parameters += [username]
	# Adding logging
	LOGGER.debug('Adding user %s ', username)
	try:
		command_str = __salt__['cmd.run']('net-snmp-create-v3-user ' + ' '.join(parameters), raise_err = True)
	except Exception:
		raise
	#finally:
	if service_running:
		# Adding logging
		LOGGER.debug('Starting service %s', service_name)
 		__salt__['service.start'](service_name)

def del_user(username, service_name = 'snmpd', snmpd_conf_path = '/etc/snmp/snmpd.conf', snmpd_conf_var_path = '/var/lib/net-snmp/snmpd.conf'):
	'''

	Delete user. Removes param username from "snmpd_conf_var_path".
	Removes line that contains string 'usmUser' from snmpd_conf_var_path.


	This function returns None.

	Parameters:
	- username: the user name.
	- service_name = 'snmpd': Systemd service name.
	- snmpd_conf_path = '/etc/snmp/snmpd.conf': SNMP service main configuration file
	- snmpd_conf_var_path = '/var/lib/net-snmp/snmpd.conf': SNMP localized key is saved on this file.
	'''

	service_running = __salt__['service.status'](service_name)
	# Adding logging
	LOGGER.debug('Service %s is running' if service_running else 'Service %s is not running', service_name)
 	if service_running:
		# Adding logging
 		LOGGER.debug('Stopping service %s', service_name)
 		__salt__['service.stop'](service_name)

	# Adding logging
	LOGGER.debug('Removing user %s ', username)
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

	if service_running:
		# Adding logging
		LOGGER.debug('Starting service %s', service_name)
		__salt__['service.start'](service_name)
