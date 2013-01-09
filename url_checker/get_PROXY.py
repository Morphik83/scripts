#!/usr/bin/python
# Copyright (C) 2008 Manu Garg.
# Author: Manu Garg <manugarg@gmail.com>
#
# pacparser is a library that provides methods to parse proxy auto-config
# (PAC) files. Please read README file included with this package for more
# information about this library.
#
# pacparser is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.

# pacparser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301,
# USA

"""
This script demonstrates how python web clients can be made proxy
auto-config (PAC) files intelligent using pacparser module. It take a
PAC file and an url as arguments, fetches the URL using the proxy as
determined by PAC file and URL and returns the retrieved webpage.
"""

__author__ = 'manugarg@gmail.com (Manu Garg)'
__copyright__ = 'Copyright (C) 2008 Manu Garg'
__license__ = 'LGPL'

import pacparser
import socket
import sys
import pprint

def get_proxy_from_pac(pac, url):
  try:
    proxy_string = pacparser.just_find_proxy(pac, url)
  except:
    sys.stderr.write('could not determine proxy using Pacfile\n')
    return None
  proxylist = proxy_string.split(";")
  proxies = None        # Dictionary to be passed to urlopen method of urllib
  while proxylist:
    proxy = proxylist.pop(0).strip()
    if 'DIRECT' in proxy:
      proxies = {}
      break
    if proxy[0:5].upper() == 'PROXY':
      proxy = proxy[6:].strip()
      if isproxyalive(proxy):
        proxies = {'http': 'http://%s' % proxy}
        break
  return proxies

def isproxyalive(proxy):
  host_port = proxy.split(":")
  if len(host_port) != 2:
    sys.stderr.write('proxy host is not defined as host:port\n')
    return False
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.settimeout(10)
  try:
    s.connect((host_port[0], int(host_port[1])))
  except Exception, e:
    sys.stderr.write('proxy %s is not accessible\n' % proxy)
    sys.stderr.write(str(e)+'\n')
    return False
  s.close()
  return True