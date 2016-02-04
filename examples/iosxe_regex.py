#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from pyskate.iosxe_netconf import IOSXEDevice


router = IOSXEDevice('192.168.100.4','admin','cisco')
router.connect()
config = router.get_config()

show_ip_route = router.exec_command('show ip route')
for resp in show_ip_route:
	matchObj = re.match( r'(^[D|S|C|L].*) ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}) .*', resp, re.M|re.I)
	if matchObj:
		print 'type = %s destination = %s' %(matchObj.group(1), matchObj.group(2))



