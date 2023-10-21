import asyncio
from video_parser import write_to_gsheet, write_to_text
from settings import settings


async def main():
    # Save to google sheet
    # await write_to_gsheet(settings.GOOGLE_SHEET_ID,
    #                       settings.YT_PLAYLIST_URL,
    #                       settings.DATE_AFTER,
    #                       settings.START_ROW,
    #                       settings.LIST_ID)

    # Save to text files
    await write_to_text(settings.YT_PLAYLIST_URL,
                        settings.DATE_AFTER)


asyncio.run(main())
