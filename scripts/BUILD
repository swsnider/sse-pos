#!/usr/bin/env python
# A small python script to package up the app
import os
import os.path
import shutil
import subprocess
import sys


def main():
  if len(sys.argv) != 2:
    sys.exit(1)
  project = sys.argv[1]

  if subprocess.call('type sass', shell=True, stdin=subprocess.PIPE,
                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT) != 0:
    print '[BUILD] Installing sass'
    r = subprocess.call('sudo gem install haml', shell=True)
    if r != 0:
      print '[BUILD] Sass gem installation failed -- exiting...'
      sys.exit(1)

  if os.path.isdir('build_out'):
    if os.path.isdir('build_out/%s' % project):
      shutil.rmtree('build_out/%s' % project)
  else:
    try:
      shutil.rmtree('build_out')
    except OSError:
      pass
    os.mkdir('build_out')

  shutil.copytree(project, 'build_out/%s' % project)

  print '[BUILD] Copying complete. Running Sass...'
  r = subprocess.call('sass --update --style expanded "build_out/%s"'
                      ' "build_out/%s"' % (project, project), shell=True)
  r = subprocess.call('find "build_out/%s" -iname "*.scss" -delete' % project,
                      shell=True)
  print '[BUILD] Build complete. Results in build_out/%s' % project


if __name__ == '__main__':
  main()