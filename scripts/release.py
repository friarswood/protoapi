#!/usr/bin/env python3

import pytest
import json
import os
# git-python seems buggy (repo got corrupted) and hard to use

version_file = "./static/swagger.json"

# dont actually execute shell commands if True
DRY_RUN=False

# wrap os.system 
def shell(cmd):
  print(cmd)
  if DRY_RUN: return
  ret = os.system(cmd)
  if ret != 0:
    raise SystemError("'%s' returned %d" % (cmd, ret))


# 0. warn if local modifications
shell("[[ -z $(git status -s) ]] || echo 'WARNING: found modified/untracked files'")

# 1. ensure tests run ok
assert pytest.main() == pytest.ExitCode.OK

# 2. get current version from swagger
with open(version_file) as fp:
  swagger = json.load(fp)
  old_version_string = swagger["info"]["version"]

# bump patch version 
version_numbers = [int(s) for s in old_version_string.split(".")]
version_numbers[2] = version_numbers[2] + 1
version_string = ".".join([str(n) for n in version_numbers])
print("Bumping version to %s" % version_string)
swagger["info"]["version"] = version_string
with open(version_file, "w") as fp:
  json.dump(swagger, fp, indent=2)
# commit changed version
print("Committing version update")
shell("git add %s" % version_file)
shell("git commit -m\"[autorelease]\" tag %s\"" % version_string)

# 4. tag and push
print("Tagging %s" % version_string)
shell("git tag -a -m \"[autorelease]\" %s" % version_string)
print("Pushing bumped version and tag to origin")
shell("git push origin --follow-tags")

