import click


@click.command()
@click.option("--video_file", required=True, help="Video file for colour analysis.")
def click_video_colour_analysis(**kwargs):
    from video_analysis.colour_analysis import colour_analysis

    colour_analysis(**kwargs)


@click.command()
@click.option("--video_file", required=True, help="Video file to be split into frames.")
def click_video_splitter(**kwargs):
    from video_analysis.split_video import video_splitter

    video_splitter(**kwargs)
