"""
Initializes and loads project yaml files:

- config.yml: project directory, youtube api key, elasticsearch credentials
- fetch.yml: list of youtube channels to fetch
- network.yml: specifies related channel/recommended video channels
"""

import yaml
import os

__VERSION__ = 0.1

PROV_AGENT = "pyg_{}".format(__VERSION__)

NETWORK_TEMPLATE = """
# videos:
#   mgs:
#     q: 'metal gear solid'
#     depth: 1
#   yy_thegift:
#     seeds:
#     - 'Fg1EvKUhZw4'
#     depth: 3
#
# channels:
#   yongyea:
#     seeds:
#     - 'channel/UCT6iAerLNE-0J1S_E97UAuQ'
#     - 'user/pythonselkanHD'
#     featured: false
#     depth: 5    
"""

FETCH_TEMPLATE = """
# channels:
# - 'user/pythonselkanHD'
# - 'channel/UCT6iAerLNE-0J1S_E97UAuQ'
"""



def init():
    """
    Creates templates for config.yml, fetch.yml, network.yml
    """
    # if not os.path.exists(PROJECT["dir"]):
    #     os.makedirs(PROJECT["dir"])

    config = {
        "project": {
            "name": "pyg_project",
            "dir": "data"
        },
        "youtube": {
            "api-key": ""
        },
        "elasticsearch" : {
            "url": "",
            "user": "",
            "password": "",
            "prefix": "pyg_"
        }
    }
    if not os.path.exists("config.yml"):
        with open("config.yml", "w") as f:
            yaml.dump(config, f, default_flow_style=False)

    if not os.path.exists("fetch.yml"):
        with open("fetch.yml", "w") as f:
            f.write(FETCH_TEMPLATE)

    if not os.path.exists("network.yml"):
        with open("network.yml", "w") as f:
            f.write(NETWORK_TEMPLATE)

def load_config():
    """
    load config yml project directory and youtube api key information
    """
    try:
        with open("config.yml") as f:
            config = yaml.load(f)
        PROJECT = config["project"]
        PROJECT["dir"]
        YOUTUBE_API_KEY = config["youtube"]["api-key"]
    except:
        PROJECT = {}
        PROJECT["dir"] = ""
        YOUTUBE_API_KEY = ""

    if YOUTUBE_API_KEY == "" or PROJECT["dir"] == "":
        raise IOError("config.yml not configured correctly")

    config = {
        "PROJECT_DIR": PROJECT["dir"],
        "YOUTUBE_API_KEY": YOUTUBE_API_KEY,
    }
    return config

def load_elasticsearch_config():
    """
    load elasticsearch credentials and index prefix from config.yml
    """
    try:
        with open("config.yml") as f:
            config = yaml.load(f)
    except:
        raise IOError("config.yml not there ...")

    try:
        es_config = config["elasticsearch"]
        user = es_config["user"]
        url = es_config["url"]
        password = es_config["password"]
        prefix = es_config["prefix"]

        if user == "" and password == "":
            ES_SERVER = url
        
        if prefix == "":
            raise IOError("es index prefix needed in config.yml")

        return ES_SERVER, prefix

    except:
        raise IOError("config.yml not valid")

    pass

def fetch_queue():
    """
    yields all channel in fetch.yml
    """
    try:
        with open("fetch.yml") as f:
            fetch = yaml.load(f)
    except:
        raise IOError("No valid fetch.yml available")
    
    if "channels" not in fetch:
        raise IOError("fetch.yml not configured correclty")

    if fetch["channels"]:
        for channel in fetch["channels"]:
            yield channel

def network_queue(network_type):
    """
    yields all network graph specifications in network.yml
    """
    try:
        with open("network.yml") as f:
            network = yaml.load(f)
    except:
        raise IOError("network.yml does not exist")

    if network_type in network:
        if network[network_type]:
            for name, config in network[network_type].items(): 
                yield name, config