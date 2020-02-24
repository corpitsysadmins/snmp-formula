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

def start_snmpd(init_binary = 'systemctl', parameters = ('start', 'snmpd.service')):
	'''Start the SNMPd deamon
	Use the init program to start the SNMPd deamon.
	'''
	
	service_start_command = 'systemctl start snmpd.service'
	return __salt__['cmd.run'](service_stop_command)
	
def stop_snmpd(init_binary = 'systemctl', parameters = ('stop', 'snmpd.service')):
	'''Stop the SNMPd deamon
	Use the init program to stop the SNMPd deamon.
	'''
	
	service_stop_command = 'systemctl stop snmpd.service'
	return  __salt__['cmd.run'](service_stop_command)

def check_user(username, snmpd_conf_path = '/etc/snmp/snmpd.conf'):
	'''Check user list
	Finds a user in the list of registered users. Returns true if is in the list, false otherwise.
	'''
	
	with open(snmpd_conf_path, 'r') as f:
		for	line in f.readlines():
			if username in line:
				return True
		return False

def add_user(username, authpass, privpass, read_only = False, auth_hash_sha = True, encryption_aes = True):
	'''Add user
	Adds a user to the user list. Returns None.
	'''
	parameters = []

	parameters.append('-ro')
	parameters += ['-A', authpass]
	parameters += ['-a', 'SHA' if auth_hash_sha else 'MD5']
	parameters += ['-X', privpass]
	parameters += ['-x', 'AES' if encryption_aes else 'DES']
	parameters += [username]

	command_str = __salt__['cmd.run']('net-snmp-create-v3-user ' + ' '.join(parameters))

def del_user(username, snmpd_conf_path = '/etc/snmp/snmpd.conf', snmpd_conf_var_path = '/var/lib/net-snmp/snmpd.conf'):
	'''Delete user
	Removes a user from the user list. Returns None.
	'''
	
	stop_snmpd()

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
	
	start_snmpd()
