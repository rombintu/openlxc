DATABASE = 'sqlite:///db.sqlite'
import platform
import json

def createconf():
    uname = platform.uname()
    with open('hypinfo.json', 'w') as f:
        content = json.dumps(
            {
                "system": uname.system,
                "node": uname.node,
                "release": uname.release,
                "version": uname.version,
                "machine": uname.machine,
                "processor": uname.processor
            })

        f.write(content)

if __name__ == '__main__':
    createconf()