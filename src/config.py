import platform
import json
import os

from pathlib import Path

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
                # "processor": uname.processor
            })

        f.write(content)

def createUploadFolder():
    folder = os.getenv("UPLOAD_FOLDER")
    Path(folder or "uploads").mkdir(parents=True, exist_ok=True)

if __name__ == '__main__':
    createconf()
    createUploadFolder()