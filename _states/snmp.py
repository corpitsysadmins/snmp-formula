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


def user_exists(name, authpass, privpass, snmpd_conf_path='/etc/snmp/snmpd.conf', **kwargs):
	'''Add an SNMPv3 user
	Creates an SNMPv3 user/password pair in the required configuration file.

	Parameters:
	- name: the user name
	- snmpd_conf_path: the net-snmp configuration file
	'''
	ret	=	{
		'name'		: username,
		'result'	: False,
		'changes'	: {},
		'comment'	: '',
	}

	if not __salt__['file.file_exists'](file):
		if __opts__['test']:
			ret['result'] = None
			ret['comment'] = "The snmp-net doesn't seem to be installed; if installed in this state run, snmp user would have been created."
		else:
			ret['result'] = False
			ret['comment'] = "The snmp-net doesn't seem to be installed. SNMP user cannot be created."
		return ret

	try:
		user_is_there = __salt__['snmp.check_user'](username)
	except RuntimeError as error:
		ret['comment'] = 'Getting existence of snmp user failed: ' + str(error)
		return ret

	if user_is_there:
			ret['result'] = True
			ret['comment'] = 'User {} is already on the system'.format(username)
			ret['changes'].update({'SNMPv3' : {'new' : name}})
	else:
		if __opts__['test']:
			ret['result'] = None
			ret['comment'] = 'The {} would be created'.format(username)
		else:
			try:
				create_user = __salt__['snmp.add_user'](username, authpass, privpass, read_only = False, auth_hash_sha = True, encryption_aes = True)
			except RuntimeError:
				ret['comment'] = "add_user command didn't run successfully"
				return ret

	return ret

def user_gone(name, authpass, privpass, snmpd_conf_path='/etc/snmp/snmpd.conf', **kwargs):
	'''Unlink agent
	Unlink an already configured agent from the Nessus/Tenable server/cloud.
	'''

	ret	=	{
		'name'		: name,
		'result'	: False,
		'changes'	: {},
		'comment'	: '',
	}

	if not __salt__['nessus_agent.is_configurable'](nessuscli):
		ret['result'] = True
		ret['comment'] = "The Nessus agent doesn't seems to be installed; if installed in this state run, it would have been unlinked"
		return ret

	try:
		status_results = __salt__['nessus_agent.run_agent_command'](nessuscli, 'status')
	except RuntimeError as error:
		ret['comment'] = 'Getting the status of the agent failed: ' + str(error)
		return ret

	if status_results > status_messages['unlinked']:
		linked = False
	elif status_results > status_messages['linked']:
		linked = True
		link_details = status_results(status_messages['linked'])
	else:
		ret['comment'] = 'Getting the status of the agent failed'
		return ret

	if linked:
		if __opts__['test']:
			ret['result'] = None
			ret['comment'] = 'The agent would be unlinked from {}:{}'.format(link_details.server_host, link_details.server_port)
		else:
			try:
				unlink_results = __salt__['nessus_agent.run_agent_command'](nessuscli, 'unlink')
			except RuntimeError:
				ret['comment'] = "The unlink command didn't run successfully"
				return ret
			if unlink_results > status_messages['unlink_success']:
				unlink_details = unlink_results(status_messages['unlink_success'])
				ret['result'] = True
				ret['comment'] = str(unlink_details)
				ret['changes'].update({'nessus_agent' : {'old' : str(link_details), 'new' : str(unlink_details)}})
			else:
				ret['result'] = False
				ret['comment'] = 'Unlinking failed: {}'.format(str(unlink_results))
	else:
		ret['result'] = True
		ret['comment'] = 'The agent is already unlinked'

	return ret
