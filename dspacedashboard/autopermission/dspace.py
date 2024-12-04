import os
import subprocess

from decouple import config

def update_dspace_user(netid, extra_params=[]):
    dspace_cli = os.path.join(config('DSPACE_PATH'), 'bin/dspace')
    res = subprocess.check_output([dspace_cli, "user", "--modify", "-n", netid] + extra_params)
    return res