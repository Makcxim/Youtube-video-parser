import asyncio
from pathlib import Path
import pygsheets
import sys
import shlex


data_folder = Path("data")
data_folder.mkdir(parents=True, exist_ok=True)


async def run_command(command, stdin=None, quiet=True, log_stdout=False, env=None):
    if sys.platform == 'win32':
        command_string = ' '.join(command)
    else:
        command_string = shlex.join(command)
    proc = await asyncio.create_subprocess_shell(
        command_string,
        stdin=asyncio.subprocess.PIPE if stdin else None,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        **({'env': env} if env else {}))

    stdout, stderr = await proc.communicate(stdin)

    if not quiet:
        print(f'[{command_string!r} exited with {proc.returncode}]')
        if stderr:
            print(f'[stderr]\n{stderr.decode(errors="ignore")}')
        if stdout and log_stdout:
            print(f'[stdout]\n{stdout.decode(errors="ignore")}')
    return stdout


async def get_channel_info(output_filename, link):
    command = f'yt-dlp --skip-download ' \
              f'--print-to-file "%(uploader)s /gay/ %(channel_follower_count)s /gay/ %(uploader_url)s" ' \
              f'{output_filename} {link}'
    await run_command(command.split(), quiet=True)


async def get_all_videos(date_after, output_filename, yt_playlist_url):
    command = f'yt-dlp --skip-download --lazy-playlist --break-on-reject --dateafter {date_after} ' \
              f'--print-to-file "%(title)s /gay/ %(view_count)s /gay/ %(like_count)s /gay/ %(comment_count)s ' \
              f'/gay/ %(upload_date)s /gay/ %(duration)s /gay/ %(webpage_url)s" ' \
              f'{output_filename} {yt_playlist_url}'
    await run_command(command.split(), quiet=True)


async def write_to_text(url, date):
    """
    Save some video data to text files.
    :param url: YouTube playlist url
    :param date: date after which videos will be retrieved
    :return: On success, needed video and channel data, writes data to text files.
    """

    videos_info = data_folder / "videos.txt"
    channel_info = data_folder / "channel.txt"
    with open(videos_info, "w", encoding="utf-8"): pass
    with open(channel_info, "w", encoding="utf-8"): pass

    await get_all_videos(date, videos_info, url)
    f1 = open(videos_info, "r", encoding="utf-8").readlines()
    await get_channel_info(channel_info, f1[0].strip().split(" /gay/ ")[-1])
    f2 = open(channel_info, "r", encoding="utf-8").readlines()
    video_data = [i.strip().split(" /gay/ ") for i in f1]
    channel_data = [i.strip().split(" /gay/ ") for i in f2]
    return video_data, channel_data


async def write_to_gsheet(google_sheet_id, url, date, start_row, list_id):
    """
    Writes data to google sheet and save it to text files.
    :param google_sheet_id: specified google sheet id
    :param url: YouTube playlist url
    :param date: date after which videos will be retrieved
    :param start_row: start row in google sheet
    :param list_id: list id in google sheet
    :return: On success, writes data to google sheet and save it to text files.
    """
    video_data, channel_data = await write_to_text(url, date)

    # how to get service_file: https://pygsheets.readthedocs.io/en/stable/authorization.html
    gc = pygsheets.authorize(service_file='service_file.json')
    sht1 = gc.open_by_key(google_sheet_id)
    wks = sht1.worksheets()[list_id]

    wks.update_value(f"A{start_row}", "Channel Name")
    wks.update_value(f"B{start_row}", channel_data[0][0])
    wks.update_value(f"A{start_row + 1}", "Channel Followers")
    wks.update_value(f"B{start_row + 1}", channel_data[0][1])
    wks.update_value(f"A{start_row + 2}", "Channel URL")
    wks.update_value(f"B{start_row + 2}", channel_data[0][2])
    wks.update_value(f"A{start_row + 4}", "Video Name")
    wks.update_value(f"B{start_row + 4}", "Views")
    wks.update_value(f"C{start_row + 4}", "Likes")
    wks.update_value(f"D{start_row + 4}", "Comments")
    wks.update_value(f"E{start_row + 4}", "Upload Date")
    wks.update_value(f"F{start_row + 4}", "Duration")
    wks.update_value(f"G{start_row + 4}", "Video URL")

    for _, i in enumerate(video_data):
        wks.update_value(f"A{5 + start_row + _}", i[0])
        wks.update_value(f"B{5 + start_row + _}", i[1])
        wks.update_value(f"C{5 + start_row + _}", i[2])
        wks.update_value(f"D{5 + start_row + _}", i[3])
        wks.update_value(f"E{5 + start_row + _}", i[4])
        wks.update_value(f"F{5 + start_row + _}", i[5])
        wks.update_value(f"G{5 + start_row + _}", i[6])
