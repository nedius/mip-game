import customtkinter as ctk

class GameWindow(ctk.CTkToplevel):

    def __init__(self, master, game_number_array):
        super().__init__(master)
        self.game_data=game_number_array
        self.game_window_setup()
        self.game_window_widgets()
        self.game_gird()
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def on_close(self):
        self.master.deiconify()
        self.destroy()

    def on_exit(self):
        self.master.destroy()
    
    def game_window_setup(self):

        self.title("My new window")
        self.geometry("300x300")  

    def game_window_widgets(self):     

        self.new_button=ctk.CTkButton(
                                    self, 
                                    text="Close window", 
                                    fg_color="pink", 
                                    text_color="purple",
                                    command=self.on_close)
        self.new_button.pack(pady= 20)

        self.exit=ctk.CTkButton(self, text="EXIT", command=self.on_exit, fg_color="red", text_color="white")
        self.exit.pack(pady=20)

    def game_gird(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20, padx=20)

        for index, value in enumerate(self.game_data): #enumerate give index and value
            square = ctk.CTkFrame(master=self.container, 
                                    width=20, 
                                    height=20, 
                                    corner_radius=8,
                                    fg_color="purple")
            
            square.grid(row=0, column=index, padx=5, pady=5)
            square.grid_propagate(False) 

            label = ctk.CTkLabel(master=square, text=str(value), text_color="white")
            label.place(relx=0.5, rely=0.5, anchor="center")

        