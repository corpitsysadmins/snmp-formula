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


def user_exists(name, authpass, privpass, read_only = True, auth_hash_sha = True, encryption_aes = True, snmpd_conf_path='/etc/snmp/snmpd.conf', **kwargs):
	'''Add an SNMPv3 user
	Creates an SNMPv3 user/password pair in the required configuration file.

	Parameters:
	- name: the user name
	- authpass: snmpv3 authentication password
	- privpass: snmpv3 privacy password
	- read_only: If set to true (default) net-snmp-create-v3-user is executed with the -ro switch
	- auth_hash_sha: If set to true (default) net-snmp-create-v3-user is executed with -a SHA. Otherwise -a MD5
	- encryption_aes: If set to true (default) net-snmp-create-v3-user is executed with -x AES. Otherwise -x DES
	- snmpd_conf_path: the net-snmp configuration file
	'''
	ret	=	{
		'name'		: name,
		'result'	: False,
		'changes'	: {},
		'comment'	: '',
	}

	if not __salt__['file.file_exists'](snmpd_conf_path):
		if __opts__['test']:
			ret['result'] = None
			ret['comment'] = "The snmp-net doesn't seem to be installed; if installed in this state run, snmp user would have been created."
		else:
			ret['result'] = False
			ret['comment'] = "The snmp-net doesn't seem to be installed. SNMP user cannot be created."
		return ret

	try:
		user_is_there = __salt__['snmp.check_user'](name)
	except RuntimeError as error:
		ret['comment'] = 'Getting existence of snmp user failed: ' + str(error)
		return ret

	if user_is_there:
			ret['result'] = True
			ret['comment'] = 'User {} is already on the system'.format(name)
	else:
		if __opts__['test']:
			ret['result'] = None
			ret['comment'] = 'The {} would be created'.format(name)
			ret['changes'].update({'SNMPv3' : {'new' : name}})
		else:
			try:
				create_user = __salt__['snmp.add_user'](name, authpass, privpass, read_only = False, auth_hash_sha = True, encryption_aes = True)
			except RuntimeError:
				ret['comment'] = "add_user command didn't run successfully"
				return ret


	return ret

def user_gone(name, snmpd_conf_path='/etc/snmp/snmpd.conf', snmpd_conf_var_path = '/var/lib/net-snmp/snmpd.conf', **kwargs):
	'''Delete an SNMPv3 user
Removes an SNMPv3 user/password pair in the required configuration file. It triggers a service restart.

	Parameters:
	- name: the user name
	- snmpd_conf_path: the net-snmp configuration file
	- snmpd_conf_var_path: the net-snmp var configuration file
	'''
	ret	=	{
		'name'		: name,
		'result'	: False,
		'changes'	: {},
		'comment'	: '',
	}

	if not __salt__['file.file_exists'](snmpd_conf_path):
		if __opts__['test']:
			ret['result'] = None
			ret['comment'] = "The snmp-net doesn't seem to be installed; if installed in this state run, snmp user would have been created."
		else:
			ret['result'] = False
			ret['comment'] = "The snmp-net doesn't seem to be installed. SNMP user cannot be created."
		return ret

	try:
		user_is_there = __salt__['snmp.check_user'](name)
	except RuntimeError as error:
		ret['comment'] = 'Getting existence of snmp user failed: ' + str(error)
		return ret

	if user_is_there:
			ret['result'] = True
			ret['comment'] = 'User {} is already on the system'.format(name)
	else:
		if __opts__['test']:
			ret['result'] = None
			ret['comment'] = 'The {} would be deleted'.format(name)
			ret['changes'].update({'SNMPv3' : {'new' : name}})
		else:
			try:
				create_user = __salt__['snmp.del_user'](username, snmpd_conf_path = '/etc/snmp/snmpd.conf', snmpd_conf_var_path = '/var/lib/net-snmp/snmpd.conf')
			except RuntimeError:
				ret['comment'] = "del_user command didn't run successfully"
				return ret


	return ret
