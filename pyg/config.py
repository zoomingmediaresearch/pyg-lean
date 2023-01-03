"""
Initializes and loads project yaml files:

- config.yml: project directory, youtube api key
- channels.yml: list of youtube channels to fetch
- videos.yml: list of youtube channels to fetch
"""

import yaml
import os
import json
import socks
import socket

__VERSION__ = "1.0.0"

PROV_AGENT = "pyg_{}".format(__VERSION__)


#YAML TEMPLATES
FETCH_TEMPLATE = """
# channels:
# - 'user/pythonselkanHD'
# - 'channel/UCT6iAerLNE-0J1S_E97UAuQ'
"""

FETCH_CHANNELS_TEMPLATE = """
# main:
# - 'user/pythonselkanHD'
# - 'channel/UCT6iAerLNE-0J1S_E97UAuQ'
"""

FETCH_VIDEOS_TEMPLATE = """
# video_list:
# - '5IsSpAOD6K8'
"""


#DATA DIRECTORIES
DATA_DIR = "data"
ADDON_DIR = "addon"

#ARCHIVE DIRECTORIES
VIDEO_CAPTIONS_DIR = "video_captions"
VIDEO_COMMENTS_DIR = "video_comments"
VIDEO_METADATA_DIR = "video_meta"
PLAYLISTS_DIR = "playlists"


def init_project():
    """
    Creates templates for config.yml, channels.yml, videos.yml
    """

    config = {
        "project": {
            "name": "pyg_project",
            "dir": "data"
        },
        "network": {
            "proxy": ""
        },
        "youtube": {
            "api-key": ""
        },
    }
    if not os.path.exists("config.yml"):
        with open("config.yml", "w") as f:
            yaml.dump(config, f, default_flow_style=False)

    if not os.path.exists("channels.yml"):
        with open("channels.yml", "w") as f:
            f.write(FETCH_CHANNELS_TEMPLATE)

    if not os.path.exists("videos.yml"):
        with open("videos.yml", "w") as f:
            f.write(FETCH_VIDEOS_TEMPLATE)

def load_config():
    """
    load config yml project directory and youtube api key information
    """
    try:
        with open("config.yml") as f:
            config = yaml.safe_load(f)
        PROJECT = config["project"]
        PROJECT["dir"]
        YOUTUBE_API_KEY = config["youtube"]["api-key"]
        PROXY = config["network"]["proxy"]
    except:
        PROJECT = {}
        PROJECT["dir"] = ""
        YOUTUBE_API_KEY = ""

    if YOUTUBE_API_KEY == "" or PROJECT["dir"] == "":
        raise IOError("config.yml not configured correctly")

    config = {
        "PROJECT_DIR": PROJECT["dir"],
        "YOUTUBE_API_KEY": YOUTUBE_API_KEY,
        "ADDON_DIR": os.path.join(PROJECT["dir"], ADDON_DIR),
        "PROJECT_NAME": PROJECT["name"],
        "PROXY": PROXY
    }
    return config


def channel_config():
    """
    yields all channel in channels.yml
    """
    try:
        with open("channels.yml") as f:
            fetch = yaml.safe_load(f)
    except:
        raise IOError("No valid channels.yml available")
    
    for group, channels in fetch.items():
        yield (group, channels)


def video_config():
    try:
        with open("videos.yml") as f:
            fetch = yaml.safe_load(f)
    except:
        raise IOError("No valid videos.yml available")
    print(fetch)
    for group, video_ids in fetch.items():
        yield (group, video_ids)


def set_proxy(proxy):
    """
    sets up proxy connection
    """
    addr, port = proxy.split(":")
    socks.setdefaultproxy(proxy_type=socks.PROXY_TYPE_SOCKS5, addr=addr, port=int(port))
    socket.socket = socks.socksocket
