import customtkinter as ctk

class GameWindow(ctk.CTkToplevel):

    def __init__(self, master, game_number_array):
        super().__init__(master)
        self.game_data=game_number_array
        self.game_window_setup()
        self.game_gird()        
        self.game_window_widgets()
        self.selected_numbers = []
        self.protocol("WM_DELETE_WINDOW", self.quit)

    def on_go_to_menu(self):
        self.master.deiconify()
        self.destroy()

    def on_exit(self):
        self.master.destroy()

    def button_sum_action(self):
        pass

    def button_remove_action(self):
        pass
    

    # TODO: izdarit lauka izveli un parbaudi, lai varetu nospiest tikai 1 un 2, 3 un 4,...    
    def game_gird(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(pady=20)

        for index, value in enumerate(self.game_data): #enumerate give index and value

            if (index//2)%2==0:
                color = "#9252AB"
            else:
                color = "#C23659"
            square = ctk.CTkFrame(master=self.container, 
                                    width=30, 
                                    height=30, 
                                    corner_radius=8,
                                    fg_color=color)
            
            square.grid(row=0, column=index, padx=3, pady=5)
            square.grid_propagate(False) 

            label = ctk.CTkLabel(master=square, text=str(value), text_color="white", font=('Arial', 17))
            label.place(relx=0.5, rely=0.5, anchor="center")

            square.bind("<Button-1>", lambda event, s=square, i=index, v=value: self.on_square_click(s, i, v))

            label.bind("<Button-1>", lambda event, s=square, i=index, v=value: self.on_square_click(s, i, v))

    def game_window_setup(self):

        self.title("Game window")
        self.geometry("1000x300")  

    def game_window_widgets(self):

        self.action_container = ctk.CTkFrame(self, fg_color="transparent")
        self.action_container.pack(fill="x", pady=40, padx=300) 

        self.sum_action=ctk.CTkButton(
                                    master=self.action_container,
                                    text="sum(+)",
                                    fg_color="#239618",
                                    command=self.button_sum_action,
                                    corner_radius=8,
                                    width=30,
                                    height=30,
                                    font=('Arial', 17),
                                    text_color="white")
        self.sum_action.pack(side= "left")

        self.remove_action=ctk.CTkButton(
                                    master=self.action_container,
                                    text="remove",
                                    fg_color="#BD7114",
                                    command=self.button_remove_action,
                                    corner_radius=8,
                                    width=30,
                                    height=30,
                                    font=('Arial', 17),
                                    text_color="white")
        self.remove_action.pack(side= "right")

        self.go_to_menu=ctk.CTkButton(
                                    self, 
                                    text="Go To Main Menu", 
                                    fg_color="pink", 
                                    text_color="purple",
                                    command=self.on_go_to_menu)
        self.go_to_menu.pack(pady= 10)

        self.exit=ctk.CTkButton(self, text="Exit", command=self.on_exit, fg_color="red", text_color="white")
        self.exit.pack(pady=7)
