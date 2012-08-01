'''longtroll: Notify you when your long-running processes finish.'''

import argparse
import getpass
import os
import pickle
import re
import subprocess
import time

collapse_whitespace_re = re.compile('[ \t][ \t]*')

def spawn_notify(notifier, proc_ended):
  cmd = notifier.replace('<cmd>', proc_ended[0])
  cmd = cmd.replace('<pid>', str(proc_ended[1]))
  subprocess.Popen(cmd, shell=True)

def get_user_processes(user):
  def line_to_dict(line):
    line = re.sub(collapse_whitespace_re, ' ', line).strip()
    time, pid, ppid, command = line.split(' ', 3)
    try:
      return {
          'age': etime_to_secs(time),
          'pid': int(pid),
          'ppid': int(ppid),
          'command': command,
          }
    except Exception:
      print('Caught exception for line: %s' % line)
      raise

  ps_out = subprocess.Popen([
    'ps', '-U %s' % user, '-o etime,pid,ppid,command'],
    stdout=subprocess.PIPE).communicate()[0]
  for line in ps_out.split('\n')[1:]:
    if line: yield line_to_dict(line)

def etime_to_secs(etime):
  'Parsing etimes is rougher than it should be.'

  seconds = 0

  etime = etime.split('-')
  if len(etime) == 2:
    seconds += int(etime[0]) * 24 * 60 * 60
    etime = etime[1]
  else:
    etime = etime[0]

  etime = etime.split(':')
  if len(etime) == 3:
    seconds += int(etime[0]) * 60 * 60
    mins, secs = etime[1:]
  else:
    mins, secs = etime

  seconds += 60 * int(mins) + int(secs)
  return seconds

def filter_by_parent(ppid, procs):
  return (proc for proc in procs if proc['ppid'] == ppid)

def filter_by_min_age(min_age, procs):
  return (proc for proc in procs if proc['age'] >= min_age)

def long_procs(ppid, min_age):
  user_processes = get_user_processes(getpass.getuser())
  user_procs_with_parent = filter_by_parent(ppid, user_processes)
  user_procs_with_min_age = filter_by_min_age(min_age, user_procs_with_parent)

  return set(
      (proc['command'], proc['pid']) for proc in user_procs_with_min_age)

def main():
  import sys

  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument(
      '--config_file', '-c', metavar='FILE', default='~/.longtrollrc',
      help='Configuration file to load')
  parser.add_argument(
      '--ppid', '-p', default=os.getppid(), type=int,
      help='The parent PID of processes to notify for. Defaults to the parent '
      'PID of longtroll (usually the PID of your shell).')
  parser.add_argument('mode', action='store', help='Either "bind" or "watch"')
  args = parser.parse_args()

  options_dict = {}
  try:
    with open(os.path.expanduser(args.config_file)) as config_file:
      for line in config_file:
        key, val = line.split(' ', 1)
        options_dict[key] = val
  except IOError:
    print('Could not read config file:')
    raise

  if 'seconds' not in options_dict:
    print('Must specify "seconds" option in config file')
    return
  if 'notify' not in options_dict:
    print('Must specify "notify" option in config file')
    return

  min_age = int(options_dict['seconds'])
  notify = options_dict['notify']

  if args.mode == 'watch':
    last_procs = long_procs(args.ppid, min_age)
    while True:
      procs = long_procs(args.ppid, min_age)
      ended_procs = last_procs - procs
      if ended_procs:
        for proc in ended_procs:
          spawn_notify(notify, proc)
      last_procs = procs
      time.sleep(3)
  else:
    cmd = 'python %s --config_file %s --ppid %d watch' % (
        __file__, args.config_file, args.ppid)
    subprocess.Popen(cmd, shell=True)

if __name__ == '__main__':
  main()
