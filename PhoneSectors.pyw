import tkinter as tk
from tkinter import scrolledtext as sText
import sys

import lib.queryMaker as qm
import lib.miner as miner

class GUI(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master.title("Phone Sectors")
        self.master.iconbitmap("./lib/icon.ico")
        width = 650
        height = 200
        screenX = self.master.winfo_screenwidth()
        screenY = self.master.winfo_screenheight()
        x = int(screenX/2 - width/2)
        y = int(screenY/2 - height/2)
        self.master.geometry("{}x{}+{}+{}".format(width, height, x, y))
        self.master.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):

        controlFrame = tk.LabelFrame(self.master, text=" Search 11888.gr ")

        # Name Field
        name_label = tk.Label(controlFrame, text="Name")
        name_label.grid(row=0, column=0, sticky="E")
        self.name = tk.StringVar()
        self.name_entry = tk.Entry(controlFrame, textvariable=self.name)
        self.name_entry.bind("<Return>", self.go)
        self.name_entry.grid(row=0, column=1)

        # Location Field
        location_label = tk.Label(controlFrame, text="Location")
        location_label.grid(row=1, column=0, sticky="E")
        self.location = tk.StringVar()
        self.location_entry = tk.Entry(controlFrame, textvariable=self.location)
        self.location_entry.bind("<Return>", self.go)
        self.location_entry.grid(row=1, column=1)

        # Address Field
        address_label = tk.Label(controlFrame, text="Address")
        address_label.grid(row=2, column=0, sticky="E")
        self.address = tk.StringVar()
        self.address_entry = tk.Entry(controlFrame, textvariable=self.address)
        self.address_entry.bind("<Return>", self.go)
        self.address_entry.grid(row=2, column=1)

        buttonsFrame = tk.Frame(controlFrame)
        

        # Help Button
        self.help_button = tk.Button(buttonsFrame, text="Help")
        self.help_button.configure(width=10)
        self.help_button.bind("<Button-1>", self.help)
        self.help_button.pack(side="left", padx=3)

        # GO! Button
        self.go_button = tk.Button(buttonsFrame, text="Go!")
        self.go_button.configure(width=10)
        self.go_button.bind("<Button-1>", self.go)
        self.go_button.pack(side="right", padx=3)
        #self.go_button.grid(row=3, column=1, sticky="E", pady=5)

        buttonsFrame.grid(row=3, column=0, columnspan=2, pady=10)

        controlFrame.pack(side="left", expand=1,  ipadx=5, padx=10)


        logFrame = tk.LabelFrame(self.master, text="Log")

        # Logger
        self.logger = sText.ScrolledText(logFrame)
        self.logger.tag_config("success", foreground="green")
        self.logger.tag_config("warning", foreground="orange")
        self.logger.tag_config("info", foreground="grey")
        self.logger.tag_config("error", foreground="red")
        self.logger.configure(state="disabled", wrap="word")
        self.logger.pack(expand=1, fill="both")

        logFrame.pack(side="right", expand=1, fill="both", pady=10, padx=10)

    def help(self, event):
        help_msg = "Phone Sectors is used to extract records based on specific \
parameters.\n\nBoth \"Name\" and \"Location\" fields should be at least 3 \
characters long. \"Address\" field may be left out blank, if address road is not \
necessary. However, if it's filled in, it can not contain specific numbers."
        self.log(help_msg, "info")

    def go(self, event):
        name = self.name.get()
        location = self.location.get()
        address = self.address.get()

        if not len(name)>=3:
            self.log("Name should be at least 3 characters long!", "error")
            print("Name should be at least 3 characters long!")
            return
        if not len(location)>=3:
            self.log("Location should be at least 3 characters long!", "error")
            print("Location should be at least 3 characters long!")
            return
        if address:
            if not address.isalpha():
                self.log("Address can't contain numbers!", "error")
                print("Address can not contain numbers!")
                return

        self.name_entry.delete(0, "end")
        self.location_entry.delete(0, "end")
        self.address_entry.delete(0, "end")
        extract(name, location, address, self)

    def log(self, message, fatality="info"):
        self.logger.configure(state="normal")
        self.logger.insert("end", message, fatality)
        self.logger.insert("end", "\n---\n")
        self.logger.configure(state="disabled")
        self.logger.see("end")

def CLI():
    while True:
        ans = input("Copy from your browser the NAME KEY and paste it here: ")
        if len(ans) >= 3:
            name = ans
            break
        else: print("Please insert a NAME KEY longer than 3 characters")

    while True:
        ans = input("Copy from your browser the LOCATION KEY and paste it here: ")
        if ans != "":
            location = ans
            break
        else: print("Make sure you copy the LOCATION KEY")

    extract(name, location)

def extract(name, location, address="", logger=None):
    filename = name + "_" + location
    if address: filename += "_" + address
    data = qm.query(name, location, logger)
    miner.mineToExcel(data, filename, address, logger)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if "--cli" in sys.argv:
            CLI()
            input("Press <enter> to exit...")
            exit()
    else:
        app = GUI()
        app.mainloop()
