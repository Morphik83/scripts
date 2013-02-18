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
        sys.stderr.write('trying to fetch the page using proxy %s\n' % proxy)
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