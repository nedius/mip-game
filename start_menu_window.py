import customtkinter as ctk
from PIL import Image
from game_window import GameWindow
from utils import num_array
from game import ALGO_MINIMAX, ALGO_ALPHABETA


class StartMenuWindow(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.setup_config()
        self.create_widgets()

    # ── Event handlers ─────────────────────────────────────────────────────────

    def update_entry(self, value):
        self.diapason_entry.delete(0, ctk.END)
        self.diapason_entry.insert(0, str(int(value)))

    def validate_entry(self, event):
        check_value = self.diapason_entry.get()
        if not check_value:
            return
        try:
            num_value = int(check_value)
            if 15 <= num_value <= 25:
                self.slider_var.set(num_value)
            else:
                self.diapason_entry.delete(0, ctk.END)
                self.diapason_entry.insert(0, str(self.slider_var.get()))
        except ValueError:
            self.diapason_entry.delete(0, ctk.END)
            self.diapason_entry.insert(0, str(self.slider_var.get()))

    def select_algorithm(self, algorithm):
        """Called when the user clicks one of the algorithm buttons."""
        self.__selected_algorithm = algorithm
        if algorithm == ALGO_MINIMAX:
            self.btn_minimax.configure(fg_color="#1f6aa5")    # highlighted
            self.btn_alfa_beta.configure(fg_color="#3a3a3a")  # normal
        else:
            self.btn_alfa_beta.configure(fg_color="#1f6aa5")
            self.btn_minimax.configure(fg_color="#3a3a3a")

    def start(self):
        diapason = int(self.diapason_entry.get())
        player_starts = self.check_var.get() == "on"
        game_number_array = num_array(diapason)

        self.withdraw()
        self.game_view = GameWindow(
            master=self,
            game_number_array=game_number_array,
            player_starts=player_starts,
            algorithm=self.__selected_algorithm,
        )
        self.game_view.lift()

    # ── Window setup ───────────────────────────────────────────────────────────

    def setup_config(self):
        self.title("mip-game")
        self.geometry("300x400")
        self.resizable(False, False)

        self.slider_var = ctk.IntVar(value=20)
        self.check_var  = ctk.StringVar(value="off")
        self.__selected_algorithm = ALGO_MINIMAX   # default

    def create_widgets(self):
        try:
            self.logo = ctk.CTkImage(Image.open("game-control.png"), size=(40, 40))
            self.logo_label = ctk.CTkLabel(master=self, image=self.logo, text="")
        except Exception:
            self.logo_label = ctk.CTkLabel(master=self, text="🎮", font=("Arial", 30))
        self.logo_label.grid(row=0, column=0, pady=(10, 0))

        self.start_new_game = ctk.CTkButton(
            self, text="Start New Game", command=self.start,
            width=150, height=40, font=("Arial", 15))
        self.start_new_game.grid(row=1, column=0, padx=20, pady=(15, 20), sticky="ns")

        self.diapason_label = ctk.CTkLabel(self, text="Enter a number from 15 to 25:")
        self.diapason_label.grid(row=3, column=0, padx=20, sticky="nsew")

        self.diapason_entry = ctk.CTkEntry(self, width=60, justify="center")
        self.diapason_entry.grid(row=4, column=0, padx=20, pady=10, sticky="ns")
        self.diapason_entry.insert(0, "20")

        self.slider = ctk.CTkSlider(
            self, from_=15, to=25, number_of_steps=10,
            variable=self.slider_var, command=self.update_entry, height=20)
        self.slider.grid(row=5, column=0, padx=80, pady=5, sticky="ew")

        self.diapason_entry.bind("<Return>", self.validate_entry)

        self.check_box = ctk.CTkCheckBox(
            master=self, text="Player starts first",
            font=("Arial", 14), variable=self.check_var,
            onvalue="on", offvalue="off")
        self.check_box.grid(row=6, column=0, pady=15)

        # ── Algorithm selection ────────────────────────────────────────────────
        algo_label = ctk.CTkLabel(self, text="Algorithm:", font=("Arial", 13))
        algo_label.grid(row=7, column=0, pady=(5, 2))

        self.btn_minimax = ctk.CTkButton(
            self, text="Minimax",
            fg_color="#1f6aa5",          # starts highlighted (default)
            command=lambda: self.select_algorithm(ALGO_MINIMAX))
        self.btn_minimax.grid(row=8, column=0, padx=80, pady=3, sticky="ew")

        self.btn_alfa_beta = ctk.CTkButton(
            self, text="Alpha-Beta",
            fg_color="#3a3a3a",          # not selected
            command=lambda: self.select_algorithm(ALGO_ALPHABETA))
        self.btn_alfa_beta.grid(row=9, column=0, padx=80, pady=3, sticky="ew")

        self.grid_columnconfigure(0, weight=1)


if __name__ == "__main__":
    app = StartMenuWindow()
    app.mainloop()
