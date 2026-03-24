import customtkinter as ctk
from PIL import Image #Pillow library for image handling
from game_window import GameWindow


class StartMenuWindow(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.setup_config()
        self.create_widgets()
    
    #Function that will use GUI

    def on_diapason_entry(self, event):
        diapason = self.diapason_entry.get()
        # Validate the input and start the game with the given diapason
        # You can add your game logic here to handle the diapason input

    def player_start_first(self):
        pass
    
    def update_entry(self, value):
        self.slider_var.set(str(int(float(value)))) # Update the entry field with the slider value, converting it to an integer and then to a string

    def validate_entry(self, event):
        check_value = self.diapason_entry.get()

        if not check_value:
            return
        
        try:
            num_value=int(check_value)
            if 15<=num_value<=25:
                self.slider_var.set(num_value)
            else:
                self.diapason_entry.delete(0, ctk.END)
                self.diapason_entry.insert(0, str(self.slider_var.get()))

        except ValueError:
            self.diapason_entry.delete(0, ctk.END)
            self.diapason_entry.insert(0, str(self.slider_var.get()))

    def start(self):

        self.withdraw()

        self.game_view=GameWindow(master=self)
        self.game_view.lift()#in first layer      

    #Game window setup

    def setup_config(self):
        
        self.title("mip-game")
        self.geometry("300x300")
        self.resizable(False, False)  #Disable window resizing
    
        self.slider_var = ctk.IntVar(value="20")
        self.check_var=ctk.StringVar(value="off")

    def create_widgets(self):

        self.logo=ctk.CTkImage(Image.open("game-control.png"), size=(40, 40))
        self.logo_label = ctk.CTkLabel(master=self, image=self.logo, text="")
        self.logo_label.grid(row=0, column=0)

        self.start_new_game = ctk.CTkButton(self, text="Start New Game", command=self.start, width=150, height=40, font=('Arial', 15))
        self.start_new_game.grid(row=1, column=0, padx=(20, 20), pady=(15, 20), sticky="ns")

        self.diapason_label = ctk.CTkLabel(self, text="Enter a number from 15 to 25:")
        self.diapason_label.grid(row=3, column=0, padx=(20, 20), sticky="nsew")

        self.diapason_entry = ctk.CTkEntry(self, width=60, justify="center")
        self.diapason_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ns")
        self.diapason_entry.insert(0, "20")

        # self.slider_var=ctk.IntVar(value=20)
        self.slider = ctk.CTkSlider(self, 
                                    from_=15, 
                                    to=25,
                                    number_of_steps=10, #How many discrete steps the slider should have
                                    variable=self.slider_var,
                                    height=20,)
        self.slider.grid(row=5, column=0, padx=80, pady=5, sticky="ew")

        self.diapason_entry.bind("<Return>", self.validate_entry)  # Bind the Enter key to validate the entry

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


        

if __name__ == "__main__":
    app = StartMenuWindow()
    app.mainloop()