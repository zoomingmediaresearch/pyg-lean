import click
import os
from .config import init_project, load_config, channel_config, video_config, set_proxy
from .fetcher import ChannelFetcher, VideoFetcher, ChannelUpdateFetcher
from .analysis import UserStatsBuilder, channel_stats
from .utils import get_channel_files

"""
Pyg command line tool

pyg

    --proxy/--no-proxy (default: no-proxy)

    init

    fetch
        <group name>
        --comments/--no-comments (fetch comments; default: comments)
        --captions/--no-captions (fetch captoins; default: captoins)
        --skip/--no-skip (skip already fetched channels: default: skip)

    update
        <group name>

    analysis
        <analysis type>

"""

@click.group()
@click.option("--proxy/--no-proxy", default=False)
@click.pass_context
def cli(ctx, proxy):
    """
    pyg command line tool
    """
    if proxy:
        c = load_config()
        url = c["PROXY"]
        ctx.obj = { "PROXY": url}


# INIT COMMAND

@cli.command()
def init():
    print("init pyg project")
    init_project()


# FETCH COMMANDS

@cli.group()
def fetch():
    pass

@fetch.command()
@click.argument("group", default="all")
@click.option("--comments/--no-comments", default=True)
@click.option("--captions/--no-captions", default=True)
@click.option("--skip/--no-skip", default=True)
def channels(group, comments, captions, skip):
    for group_name, channels in channel_config():
        print(group_name, channels)
        if group == "all" or group_name == group:
            for channel in channels:
                ChannelFetcher(channel=channel, captions=captions, comments=comments, skip=skip, group=group_name)

@fetch.command()
@click.argument("group", default="all")
@click.option("--comments/--no-comments", default=True)
@click.option("--captions/--no-captions", default=True)
@click.option("--skip/--no-skip", default=True)
def videos(group, comments, captions, skip):
    for group_name, video_ids in video_config():
        if group == "all" or group_name == group:
            VideoFetcher(video_ids, group_name)


# UPDATE COMMAND

@cli.group()
def update():
    pass

@update.command()
@click.argument("group", default="all")
def channels(group):
    CF = load_config()
    for channel_cf  in get_channel_files(CF):
        archive_name = channel_cf["archive_name"].replace(".zip", "")
        archive_filepath = channel_cf["archive"]
        print(archive_name, archive_filepath)
        ChannelUpdateFetcher(archive_name, archive_filepath)
    # for group_name, channels in channel_config():
    #     print(group_name, channels)
    #     if group == "all" or group_name == group:
    #         for channel in channels:
    #             ChannelUpdateFetcher(channel=channel)


# ANALYSIS COMMAND

@cli.command()
@click.argument("analysis_type", default="channels")
def analysis(analysis_type):
    if analysis_type == "user-stats":
        stats = UserStatsBuilder()
    elif analysis_type == "channel-stats":
        channel_stats()

