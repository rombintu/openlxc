from pylxd import Client

client = Client()

config = {
    'name': 'bionic-test', 
    'source': {
        'type': 'image', 
        "mode": "pull", 
        "server": "https://cloud-images.ubuntu.com/daily", 
        "protocol": "simplestreams", 
        'alias': 'bionic/amd64'},
    'profiles': ['default'] 
    }

instance = client.instances.create(config, wait=True)