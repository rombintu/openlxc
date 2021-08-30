from .models import Hypervisor
import json

def getHypervisor():
    try:
        with open('hypinfo.json', 'r') as f:
            uname = json.loads(f.read())
    except:
        uname = {
            "system": "None",
            "node": "None",
            "release": "None",
            "version": "None",
            "machine": "None",
            # "processor": "None"
        }

    hypervisor = Hypervisor(
        uname['system'],
        uname['node'],
        uname['release'],
        uname['version'],
        uname['machine'],
        # uname['processor']
        )
    return hypervisor