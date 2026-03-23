import customtkinter as ctk

class GameWindow(ctk.CTkToplevel):
    def __init__(self, master, ):
        super().__init__(*master)

        self.title("My new window")
        self.geometry("300x300")

        # def close():
        #     new_window.destroy()
        #     new_window.update()        

        self.new_button=ctk.CTkButton(new_window, text="Close window", command=close, fg_color="pink")
        self.new_button.pack(pady= 20)