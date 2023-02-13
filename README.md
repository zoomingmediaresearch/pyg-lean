# pyg-lean - passable youtube grabber, the lean version

![Python 3]( https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-blue.svg)

*pyg* is a wrapper around the Youtube-API, and allows easy retrieval and analysis
of specific data. *pyg-lean* is a lean version of the original *pyg*. 

> You need a working Youtube-API key in order to use this program. See the [Google Developers Portal](https://developers.google.com/youtube/v3/getting-started) for more information on how to create one. 

![pyg logo](assets/pyg_logo.png?raw=true "pyg")

## Features
 
- Fetch Youtube data (metadata for videos, playlists, comments and captions) for channels as well as for collections of videos

## Requirements

- tested on Python 3.7, 3.8, 3.9, 3.10 
- a Youtube API v3 key

## Installation

Clone this repository and install it (preferably into a virtualenv):

```zsh
$ git clone https://github.com/zoomingmediaresearch/pyg-lean
$ cd pyg-lean
$ pip install .
```

## Quickstart

Create a project folder and initialize project there:

```zsh
$ mkdir pygproject
$ cd pygproject
$ pyg init

```

The last command creates template files for the project configuration (config.yml) and fetch items (channels.yml, videos.yml). 

### Configuration

Before you can start, you will need to add some information to the config.yml. Enter your Youtube API key into the *config.yml* in order to proceed.

```yaml
network:
  proxy: ''           # if you use a proxy server, add it here
project:         
  dir: data           # you might change the data directory (or not)
  name: pygproject    # change to your project name
  source: nosource    # you can provide extra metadata here that will be included in the created zip archive filenames
youtube:
  api-key: ''         # add your YouTube API key here, otherwise nothing will work
```

### Fetching Channels

The main configuration file (contentwise) is the *channels.yml* file in the root directory.
It contains a list of all channel identifiers to be fetched. 

Note: The channels can be grouped, to allow for a granular retrieval and update process.

```yaml
main_group:
  - channel/UCdQHEqTxcFzjFCrq0o4V7dg
  - channel/UCI06ztiuPl-F9cSXsejMV8A
other_group:
  - channel/UCZzPA6tCoQAZNiddpE-xA_Q
```

After filling in your preferred chanels, run the fetch command to fetch the data using
the Youtube API:

```zsh
$ pyg fetch channels
```

If you are interested in only a specific group, you can give it a argument:

```
$ pyg fetch channels other_group
```

The channels will be fetched and saved into the projects data folder (which is specified in the previously configured *config.yml*) Each groups contents will be stored in a separate folder, and each channel in a separate zip archive (See e.g. [olf42/zip_archive](https://github.com/olf42/zip_archive) for a small zip file wrapper in Python). 

### Fetching Videos

It is also possible to just get single videos in a similar way. Add the videos IDs to your *videos.yml*:

```yaml
my_video_list:
  - 5IsSpAOD6K8
  - qFLw26BjDZs
```

and use the fetch videos command:

```zsh
$ pyg fetch videos 
```

or for a specific group:

```zsh
$ pyg fetch videos my_video_list
```

### Fetching Updates 

You can use the integrated update function to fetch new comments, videos and channels:

```zsh
$ pyg update channels
```

The update script checks for each video in the channel if the comment count changed. If so, the current video data will be fetched from the Youtube API.
New videos will also be fetched.

An update-file for each channel in the form of <channel_name>\_<source>\_updated\_<timestamp>.zip will be created in the data folder.


### Usage behind a proxy Server

List proxy in config.yml

```yaml
network:
  proxy: 123.4.5.6:7890
```

You are required to give the *--proxy* option in order to use the given proxy.

```
$ pyg --proxy fetch channels 
```

## Command line interface

```zsh
pyg

    --proxy/--no-proxy (default: no-proxy)

    init

    fetch
        channels
            <group name>
            --comments/--no-comments (default: comments)
            --captions/--no-captions (default: captions)
        videos
            <group name>
            --comments/--no-comments (default: comments)
            --captions/--no-captions (default: captions)

    update
        channels
            <group name>

    analysis
        user-stats
        channel-stats

```

## Copyright
- 2019, Universitätsbibliothek Leipzig <info@ub.uni-leipzig.de>

## Authors of the original *pyg*
- P. Mühleder <muehleder@ub.uni-leipzig.de>
- F. Rämisch <raemisch@ub.uni-leipzig.de>

## Licence
- GNU General Public License v3 (Software)
- CC-BY (Assets)
