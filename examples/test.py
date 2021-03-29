import sys
sys.path.append("../")

from pyhmy import cli
import os

env = cli.download("./bin/test", replace=False)
cli.environment.update(env)
new_path = os.getcwd() + "/bin/test"

print(new_path)
