#!/usr/bin/python
import sys
import IPython


SDK_PATH = '/Applications/GoogleAppEngineLauncher.app/Contents/Resources/GoogleAppEngine-default.bundle/Contents/Resources/google_appengine'

def main():
  sys.path.insert(0, SDK_PATH)
  import dev_appserver
  dev_appserver.fix_sys_path()
  embedshell = IPython.Shell.IPShellEmbed(argv=[])
  embedshell()


if __name__ == '__main__':
  main()