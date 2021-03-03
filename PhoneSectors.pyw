import tkinter as tk
from tkinter import scrolledtext

import lib.PhoneSectorsController as PSC

class GUI(tk.Frame):
    """
    This class provides a simple graphical interface for user to interact with
    PhoneSectors' controller.
    """

    def __init__(self):
        super().__init__()
        self.setupWindow()
        self.setupControls()
        self.setupLogger()

    def setupWindow(self):
        """
        This method initializes window related settings.
        """

        # Set dimensions and position
        width = 650
        height = 200
        screenX = self.master.winfo_screenwidth()
        screenY = self.master.winfo_screenheight()
        x = int(screenX/2 - width/2)
        y = int(screenY/2 - height/2)
        self.master.geometry("{}x{}+{}+{}".format(width, height, x, y))

        # Other settings
        self.master.title("Phone Sectors")
        self.master.iconbitmap("./lib/res/icon.ico")
        self.master.resizable(False, False)

    def setupControls(self):
        """
        This method initializes the controller section of main window.
        """

        # Root frame
        controlFrame = tk.LabelFrame(self.master, text=" Search 11888.gr ")

        # Name Field
        name_label = tk.Label(controlFrame, text="Name")
        name_label.grid(row=0, column=0, sticky="E")
        self.name = tk.StringVar()
        self.name_entry = tk.Entry(controlFrame, textvariable=self.name)
        self.name_entry.focus_set()
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

        # Buttons sub-frame
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

        # Packing up
        buttonsFrame.grid(row=3, column=0, columnspan=2, pady=10)
        controlFrame.pack(side="left", expand=1,  ipadx=5, padx=10)

    def setupLogger(self):
        """
        This method initializes the logger window, which is used to display
        feedback messages to user.
        """

        # Root frame
        logFrame = tk.LabelFrame(self.master, text="Log")

        # Logger
        self.logger = scrolledtext.ScrolledText(logFrame)
        self.logger.tag_config("success", foreground="green")
        self.logger.tag_config("warning", foreground="orange")
        self.logger.tag_config("info", foreground="grey")
        self.logger.tag_config("error", foreground="red")
        self.logger.configure(state="disabled", wrap="word")
        self.logger.pack(expand=1, fill="both")

        # Packing up
        logFrame.pack(side="right", expand=1, fill="both", pady=10, padx=10)

    def help(self, event):
        """
        This method is used to display the help message in logger. The help
        message can be found and/ or altered in "./lib/res/help_msg.txt".
        """

        try:
            with open("./lib/res/help_msg.txt", "r", encoding="utf-8") as f_in:
                help_msg = f_in.read().strip()
            self.log(help_msg, "info")
        except:
            self.log("Help Message couldn't be loaded due to some error!", "error")

    def go(self, event):
        """
        This method is used to initialize the go button, which triggers the
        main search and export routine. In that stage the input is being checked
        whether they comply to certain validity rules.
        """

        name = self.name.get()
        location = self.location.get()
        address = self.address.get()

        # Validity rules
        if not len(name)>=3:
            self.log("Name should be at least 3 characters long!", "error")
            return
        if not len(location)>=3:
            self.log("Location should be at least 3 characters long!", "error")
            return
        if address:
            if not address.isalpha():
                self.log("Address can't contain numbers!", "error")
                return

        # Clear entries only if the query is about to begin
        self.name_entry.delete(0, "end")
        self.location_entry.delete(0, "end")
        self.address_entry.delete(0, "end")

        session = PSC.PhoneSectorsController(self, name, location, address)
        session.start()

    def log(self, message, fatality="info"):
        """
        This method displays given message to logger screen, in appropriate color.
        - message: The message to be displayed.
        - fatality: The importance of the message. It can be one of
            {"success", "info", "warning", "error"}.
        """

        # Enable editing
        self.logger.configure(state="normal")

        # Insert message to logger and place viewport at very end of logger.
        self.logger.insert("end", message, fatality)
        self.logger.insert("end", "\n---\n")
        self.logger.see("end")

        # Disable editing
        self.logger.configure(state="disabled")

if __name__ == "__main__":
    GUI().mainloop()
