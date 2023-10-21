import asyncio
from video_parser import write_to_gsheet, write_to_text


async def main():
    # Save to google sheet
    await write_to_gsheet(google_sheet_id="h&RCvQ7d-gpQfmeradLT6kjK5Vt3SUynwsA4M2x8ZRhE",
                          url="https://www.youtube.com/@LinusTechTips/videos",
                          date="20231015",
                          start_row=1,
                          list_id=0)

    # Save to text files
    await write_to_text(url="https://www.youtube.com/@LinusTechTips/videos",
                        date="20231015")


asyncio.run(main())
