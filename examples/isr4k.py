#!/usr/bin/env python
# -*- coding: utf-8 -*-

# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2013 Cisco Systems, Inc.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# @author: Hareesh Puthalath, Cisco Systems, Inc.

import sys
import logging
from ncclient import manager

log = logging.getLogger(__name__)




# Various IOS Snippets

ADD_IP_ROUTE = """
<nc:config>
    <nc:cli-config-data>
        <cmd>ip route %s</cmd>
    </nc:cli-config-data>
</nc:config>
"""

REMOVE_IP_ROUTE = """
<nc:config>
    <nc:cli-config-data>
        <cmd>no ip route %s</cmd>
    </nc:cli-config-data>
</nc:config>
"""

SHOW_IP_ROUTE = """
<nc:oper-data-format-text-block>
    <show>%s</show>
</nc:oper-data-format-text-block>
"""

#<config-format-text-cmd> %s </config-format-text-cmd>

def isr_connect(host, port, user, password):
    return manager.connect(host=host,
                           port=port,
                           username=user,
                           password=password,
                           device_params={'name': "iosxe"},
                           timeout=30
            )


def _check_response(rpc_obj, snippet_name):
    log.debug("RPCReply for %s is %s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    if "<ok />" in xml_str:
        log.info("%s successful" % snippet_name)
    else:
        log.error("Cannot successfully execute: %s" % snippet_name)


def show_ip_route(conn, cmd=None):
	try:
		confstr = SHOW_IP_ROUTE %(cmd)	
		rpc_obj = conn.get( filter=('subtree', confstr)) 
		_check_response( rpc_obj, 'SHOW_CMD')
	except Exception:
		log.exception("Exception in show cmmand %s" % cmd)

def add_ip_route(conn, routecfg):
	try:
		confstr = ADD_IP_ROUTE %(routecfg)
		rpc_obj = conn.edit_config(target='running', config=confstr)
		_check_response( rpc_obj, 'ADD_IP_ROUTE')
	except Exception:
		log.exception("Exception in add ip route %s" % routecfg)

def remove_ip_route(conn, routecfg):
    try:
        confstr = ADD_IP_ROUTE %(routecfg)
        rpc_obj = conn.edit_config(target='running', config=confstr)
        _check_response( rpc_obj, 'REMOVE_IP_ROUTE')
    except Exception:
        log.exception("Exception in remove ip route %s" % routecfg)	
	
def test_isr(host, user, password):
    with isr_connect(host, port=22, user=user, password=password) as m:
        show_ip_route(m, 'ip route')
        add_ip_route(m, '4.4.4.0 255.255.255.0 null 0')
        remove_ip_route(m, '4.4.4.0 255.255.255.0 null 0')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    test_isr(sys.argv[1], sys.argv[2], sys.argv[3])
