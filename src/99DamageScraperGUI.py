import sys
from tkinter import *
from tkinter import ttk, messagebox
import scraper
import threading
import os
import logging

import time
# TODO add ttk.Separator(master, orient=HORIZONTAL).grid(row=1, sticky='EW')


class DamageScraperGUI:
    def __init__(self, master):
        # TODO add entry for league link
        self.master = master
        master.title("99Damage Scraper")
        master.configure(background='#353c47')
        master.grid_rowconfigure(0, pad=3)
        master.grid_rowconfigure(1, pad=3)
        master.grid_rowconfigure(2, pad=3)
        master.grid_rowconfigure(3, pad=3)

        # select seasonlink row
        self.label = Label(
            master, text='99League-Link', background='#353c47', fg="white")
        self.label.grid(row=0, column=0)

        self.leaguelink_entry = Entry(background='#7b8189')
        self.leaguelink_entry.grid(row=0, column=1, columnspan=3, sticky=E + W)
        # default is saison10
        self.leaguelink_entry.insert(
            0, 'https://csgo.99damage.de/de/leagues/99dmg/989-saison-10')

        # explain row
        self.label = Label(master, text="Save to",
                           background='#353c47', fg="white")
        self.label.grid(row=1, column=0)

        self.label = Label(master, text="Set delay",
                           background='#353c47', fg="white")
        self.label.grid(row=1, column=1)

        self.label = Label(master, text="Startbutton",
                           background='#353c47', fg="white")
        self.label.grid(row=1, column=2, sticky=N+S+E+W)

        self.label = Label(master, text="est. Runtime",
                           background='#353c47', fg="white")
        self.label.grid(row=1, column=3)

        # first row (button input saveselcetor label with time)

        self.label = Label(master, text="teamdata.json")
        self.label.grid(row=2, column=0)

        self.delay_league_entry = Entry(
            master, width=3, bd=2, background='#7b8189')
        self.delay_league_entry.insert(0, 0)
        self.delay_league_entry.grid(row=2, column=1)

        self.scrap_league_button = Button(
            text='Scrap League', command=self.start_leaguescraper, background='#7b8189')
        self.scrap_league_button.grid(
            row=2, column=2, sticky=W+E)

        self.runtime_label = Label(master, text="8 Min",background='#353c47',fg="white")
        self.runtime_label.grid(row=2, column=3)

        # second row (button input saveselcetor label with time)

        self.label = Label(master, text="teamdata_players.json")
        self.label.grid(row=3, column=0)

        self.delay_team_entry = Entry(
            master, width=3, bd=3, background='#7b8189')
        self.delay_team_entry.insert(0, 0)
        self.delay_team_entry.grid(row=3, column=1)

        self.scrap_league_button = Button(
            text='Add Players', command=self.start_add_players, background='#7b8189')
        self.scrap_league_button.grid(
            row=3, column=2, sticky=W+E)

        self.runtime_label = Label(master, text="38 Min",background='#353c47',fg="white")
        self.runtime_label.grid(row=3, column=3)
        # second row (button input saveselcetor label with time)

        # third row console log

        self.log = Text(width=45, height=8, wrap="word",
                        background='#7b8189')  # TODO SCROLLBAR
        self.log.grid(row=4, columnspan=4, rowspan=4)
        # todo add func
        self.stop_button = Button(
            text='Stop', background='#472222', fg='white', command=self.stop)
        # TODO make kill window with os and spawn it again so it dead
        self.stop_button.grid(row=4, column=3, sticky=N+E)

        # used to redirect stdout to text
        sys.stdout = TextRedirector(self.log, "stdout")

    def start_leaguescraper(self):
        logging.info(threading.enumerate())
        print(
            "_________________________\nLeague Scraper started\n_________________________")
        # TODO IF value error print error
        # 'https://csgo.99damage.de/de/leagues/99dmg/989-saison-10'
        league_scrap_thread = threading.Thread(target=scraper.scrap_league_and_div_data, args=[
            str(self.leaguelink_entry.get()),], name='League Scrap',daemon=True)


        league_scrap_thread.start()


    def start_add_players(self):
        print(
            "_________________________\nAdd Teamdata Scraper started\n_________________________")
        # TODO IF value error print error
        add_team_thread = threading.Thread(target=scraper.add_teamdata_to_data,daemon=True)
        add_team_thread.start()

    def stop(self):
        # TODO did it really stop?
        root.destroy()
        for thread in threading.enumerate():
            logging.info(thread)
        os.system("python " + os.path.basename(sys.argv[0]))
        os.kill(os.getpid(), 9)
        print("Stopped")


class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")
        self.widget.see(END)


def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        os.kill(os.getpid(), 9)
        root.destroy()

if __name__ == '__main__':

    root = Tk()
    my_gui = DamageScraperGUI(root)





    root.protocol("WM_DELETE_WINDOW", on_closing)
    # root.geometry('400x270')
    root.mainloop()
