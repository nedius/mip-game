import customtkinter as ctk
from PIL import Image #Pillow library for image handling
from game_window import GameWindow


class Frontend(ctk.CTk):

    def on_diapason_entry(self, event):
        diapason = self.diapason_entry.get()
        # Validate the input and start the game with the given diapason
        # You can add your game logic here to handle the diapason input

    def player_start_first(self):
        pass
    
    def update_entry(self, value):
        self.silder_var.set(str(int(float(value)))) # Update the entry field with the slider value, converting it to an integer and then to a string

    def validate_entry(self, event):
        value = self.diapason_entry.get()
        if value.isdigit() and 15 <= int(value) <= 25:
            self.silder_var.set(int(value))  # Update the slider with the entry value
        else:
            self.diapason_entry.delete(0, ctk.END)  # Clear the entry if it's invalid
            self.diapason_entry.insert(0, str(self.silder_var.get()))  # Reset to the current slider value    

    def __init__(self):
        super().__init__()

        self.title("mip-game")
        self.geometry("300x300")
        self.resizable(False, False)  #Disable window resizing

        

        self.silder_var = ctk.IntVar(value=20)

        self.logo=ctk.CTkImage(Image.open("game-control.png"), size=(40, 40))
        self.logo_label = ctk.CTkLabel(master=self, image=self.logo, text="")
        self.logo_label.grid(row=0, column=0)

        self.start_new_game = ctk.CTkButton(self, text="Start New Game", command=self.start, width=150, height=40, font=('Arial', 15))
        self.start_new_game.grid(row=1, column=0, padx=(20, 20), pady=(15, 20), sticky="ns")

        self.diapason_label = ctk.CTkLabel(self, text="Enter a number from 15 to 25:")
        self.diapason_label.grid(row=3, column=0, padx=(20, 20), sticky="nsew")

        self.diapason_entry = ctk.CTkEntry(self, textvariable=self.silder_var, width=60, justify="center")
        self.diapason_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ns")

        # self.silder_var=ctk.IntVar(value=20)
        self.slider = ctk.CTkSlider(self, 
                                    from_=15, 
                                    to=25,
                                    number_of_steps=10, #How many discrete steps the slider should have
                                    variable=self.silder_var,
                                    height=20,)
        self.slider.grid(row=5, column=0, padx=80, pady=5, sticky="ew")

        self.check_var=ctk.StringVar(value="off")
        self.check_box=ctk.CTkCheckBox(
                                master=self,
                                text="Start first",
                                font=("Arial", 14),
                                command=self.player_start_first,
                                variable=self.check_var,
                                onvalue="on",
                                offvalue="off")
        self.check_box.grid(row=6, column=0, pady=15)

        self.grid_columnconfigure(0, weight=1)  # Make the column expand to fill the window

        self.diapason_entry.bind("<Return>", self.validate_entry)  # Bind the Enter key to validate the entry
        
    def start(self):

        self.withdraw()

        self.game_view=GameWindow(master=self)
        self.game_view.lift()#in first layer


if __name__ == "__main__":
    app = Frontend()
    app.mainloop()