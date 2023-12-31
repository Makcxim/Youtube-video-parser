# Youtube video parser

Parse some video and channel data from youtube playlist.  
Save this data to text files or to google sheet.
Find needed video data from videos after some date.

# Usage
Use .env file to set your google credentials, needed date, YT playlist link.  
Download your service file from google cloud console.  
Guide: https://pygsheets.readthedocs.io/en/stable/authorization.html

```python
from video_parser import write_to_gsheet, write_to_text

# Save to google sheet
await write_to_gsheet(google_sheet_id="h&RCvQ7d-gpQfmeradLT6kjK5Vt3SUynwsA4M2x8ZRhE",
                      url="https://www.youtube.com/@LinusTechTips/videos",
                      date="20231015",
                      start_row=1,
                      list_id=0)

# Save to text files in data folder
await write_to_text(url="https://www.youtube.com/@LinusTechTips/videos",
                    date="20231015")
```

# Example 
Watch the example in example.py  
Watch the app example with Tkinter in app-example.py
For app example you can use .env file for default values insertion.

# Preview
![img.png](pictures/img.png)

## TODO
- [ ] Fix freeze while updating google sheet values (pysheets)
- [ ] Refactor some trash...
- [ ] Normal design?

