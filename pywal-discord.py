import os, argparse
from sys import argv
from platform import system
from inspect import cleandoc
from pathlib import Path

class Parser(argparse.ArgumentParser):
    def error(self, message):
        print('error: %s\n' % message)
        self.print_help()
        exit(2)
parser = Parser()
home = os.path.expanduser('~')
cat = lambda *files: '\n'.join([Path(fn).read_text() for fn in files])

platform = system()
if platform == "Darwin":
    config = home+"/.config/pywal-discord"
    path = home+"/Library/Preferences/BetterDiscord/themes"
elif platform == "Windows":
    config = "config" # TODO: find standard config directory
    path = home+"\\Appdata\\Roaming\\BetterDiscord\\themes"
elif platform == "Linux":
    path = home+"/.config/BetterDiscord/themes"
    config="/usr/share/pywal-discord"

parser.add_argument("-t", "--theme", help="Available: [default,abou]", choices=["default", "abou"], metavar="THEME", default="default")
parser.add_argument("-p", "--path", help="Path where pywal-discord will generate theme. Default: "+path)
parser.add_argument("-d", "--directory", help="Make path directory where theme will be generated if it doesn't already exist", action="store_true")
#parser.add_argument("-tt", "--transition-time", help="Time in seconds for color transition animation. Default: 1", type=int, default=1, dest="transition")

args = parser.parse_args()
if args.directory:
    os.makedirs(path, exists_ok=True)
if args.path:
    path = args.path

newfile = os.path.join(path, "pywal-discord-%s.theme.css" % args.theme)
with open(newfile, "w") as w:
    w.write(cat(os.path.join(config, "meta.css"),
                os.path.join(home, ".cache", "wal", "colors.css"),
                os.path.join(config, "pywal-discord-%s.css" % args.theme)))
#                "\n* {transition: background-color %ss;}" % args.transition)
