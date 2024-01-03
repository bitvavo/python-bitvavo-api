import re
import sys
from os import path

if len(sys.argv) < 2:
    raise Exception("Please provide a new version number:\n\tbump.py <VERSION>")

new_version = sys.argv[1]
setup_file = path.realpath(path.join(path.dirname(__file__), "..", "setup.py"))

with open(setup_file, "r") as file:
    lines = file.readlines()

changed = False
for i, line in enumerate(lines):
    if "version=" in line:
        line = re.sub(r'"[^"]+"', '"' + new_version + '"', line)
        if line != lines[i]:
            lines[i] = line
            changed = True

if changed:
    with open(setup_file, "w") as file:
        file.writelines(lines)
        print("setup.py changed to version: " + new_version)
else:
    print("setup.py did not change")
    sys.exit(1)
