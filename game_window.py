import customtkinter as ctk

class GameWindow(ctk.CTkToplevel):


    def __init__(self, master):
        super().__init__(master)

        self.title("My new window")
        self.geometry("300x300")

        def on_close(self):
            self.master.deiconify()
            self.destroy()      

        self.new_button=ctk.CTkButton(
                                    self, 
                                    text="Close window", 
                                    fg_color="pink", 
                                    text_color="purple")
                                    # command=self.on_close)
        self.new_button.pack(pady= 20)

        