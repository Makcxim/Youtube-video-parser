from tkinter import Tk, Button, Label, Entry
from video_parser import write_to_gsheet, data_folder
from settings import settings
import asyncio


class App:
    async def exec(self):
        self.window = MainGUI(asyncio.get_event_loop())
        await self.window.show()


class MainGUI(Tk):
    def __init__(self, loop):
        self.done = False
        self.current_length = 0
        self.loop = loop
        self.root = Tk()
        self.root.geometry("500x300")
        self.root.title("YouTube Parser")

        self.sheet_id_label = Label(self.root, text="Google Sheet ID:")
        self.sheet_id_label.pack()
        self.sheet_id_entry = Entry(self.root)
        self.sheet_id_entry.pack()

        self.list_id_label = Label(self.root, text="List ID:")
        self.list_id_label.pack()
        self.list_id_entry = Entry(self.root)
        self.list_id_entry.pack()

        self.url_label = Label(self.root, text="URL:")
        self.url_label.pack()
        self.url_entry = Entry(self.root)
        self.url_entry.pack()

        self.date_label = Label(self.root, text="Date:")
        self.date_label.pack()
        self.date_entry = Entry(self.root)
        self.date_entry.pack()

        self.start_row_label = Label(self.root, text="Start Row:")
        self.start_row_label.pack()
        self.start_row = Entry(self.root)
        self.start_row.pack()

        self.progress_label = Label(self.root, text=f"Progress: 0")
        self.progress_label.pack()

        self.sheet_id_entry.insert(0, settings.GOOGLE_SHEET_ID)
        self.list_id_entry.insert(0, settings.LIST_ID)
        self.url_entry.insert(0, settings.YT_PLAYLIST_URL)
        self.date_entry.insert(0, settings.DATE_AFTER)
        self.start_row.insert(0, settings.START_ROW)

        self.start_button = Button(self.root, text="Start", command=lambda: self.loop.create_task(self.start_parser()))
        self.start_button.pack()

    async def show(self):
        while True:
            try:
                self.current_length = len(open(data_folder / 'videos.txt').readlines())
            except FileNotFoundError:
                self.current_length = 0
            self.progress_label.config(text=f"Progress: {self.current_length}")
            if self.done:
                self.progress_label.config(text=f"Progress: {self.current_length} - END")
            self.root.update()
            await asyncio.sleep(.1)

    async def start_parser(self):
        self.done = False
        await write_to_gsheet(self.sheet_id_entry.get(),
                              self.url_entry.get(),
                              self.date_entry.get(),
                              int(self.start_row.get()),
                              int(self.list_id_entry.get()))
        self.done = True


asyncio.run(App().exec())
