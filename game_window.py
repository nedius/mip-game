import customtkinter as ctk
import aiLogic
import moves
from state import game_state
from game import ALGO_MINIMAX, ALGO_ALPHABETA


class GameWindow(ctk.CTkToplevel):

    def __init__(self, master, game_number_array, player_starts=True, algorithm=ALGO_MINIMAX):
        super().__init__(master)

        self.__algorithm = algorithm
        self.__state     = game_state()
        self.__state.set_num_array(list(game_number_array))
        self.__state.is_player_move = player_starts

        # Selection state
        self.__selected_pair = None   # 1-based pair number chosen by player
        self.__sq_widgets    = {}     # index -> (frame, label) for current row

        # History (for the "previous row" display)
        self.__prev_array  = None     # num_array before the last move
        self.__prev_move   = None     # (move_type, value) of the last move
        self.__prev_actor  = None     # "Player" | "Computer"

        self.protocol("WM_DELETE_WINDOW", self.quit)
        self._build_static_widgets()
        self.refresh_grid()

        if not player_starts:
            self.after(400, self._computer_move)

    # ─────────────────────────── navigation ───────────────────────────────────

    def on_go_to_menu(self):
        self.master.deiconify()
        self.destroy()

    def on_exit(self):
        self.master.destroy()

    # ─────────────────────────── square click ─────────────────────────────────

    def on_square_click(self, index):
        if not self.__state.is_player_move:
            return

        num_arr  = self.__state.get_num_array()
        pair_idx = index // 2
        pair_num = pair_idx + 1

        # Lone last element
        is_lone = (index == len(num_arr) - 1) and (len(num_arr) % 2 != 0)
        if is_lone:
            self.status_label.configure(
                text="This is the last unpaired number. Use «Remove last».")
            return

        prev_pair = self.__selected_pair

        # Toggle
        if self.__selected_pair == pair_num:
            self.__selected_pair = None
            self.status_label.configure(
                text="Your turn — click a pair, then press «Sum pair».")
        else:
            self.__selected_pair = pair_num
            li = pair_idx * 2
            ri = li + 1
            self.status_label.configure(
                text=f"Pair {pair_num} selected  ({num_arr[li]}, {num_arr[ri]}) — press «Sum pair» to confirm.")

        # Repaint only changed pairs instead of full grid rebuild
        pairs_to_repaint = set()
        if prev_pair is not None:
            pairs_to_repaint.add(prev_pair)
        if self.__selected_pair is not None:
            pairs_to_repaint.add(self.__selected_pair)

        if pairs_to_repaint and self.__sq_widgets:
            self._repaint_pairs(pairs_to_repaint, num_arr)
        else:
            self.refresh_grid()

    # ─────────────────────────── button actions ────────────────────────────────

    def on_sum_click(self):
        if not self.__state.is_player_move:
            return
        if self.__selected_pair is None:
            self.status_label.configure(
                text="Click a pair first, then press «Sum pair».")
            return
        self._apply_move((moves.SUM_PAIR, self.__selected_pair), actor="Player")

    def on_remove_click(self):
        if not self.__state.is_player_move:
            return
        num_arr = self.__state.get_num_array()
        if len(num_arr) % 2 == 0:
            self.status_label.configure(
                text="Remove is only allowed when the last pair is incomplete.")
            return
        self._apply_move((moves.REMOVE_LAST, None), actor="Player")

    # ─────────────────────────── move logic ───────────────────────────────────

    def _apply_move(self, move, actor):
        if not moves.is_allowed_move(self.__state, move):
            self.status_label.configure(text="Illegal move.")
            return

        self.__prev_array = list(self.__state.get_num_array())
        self.__prev_move  = move
        self.__prev_actor = actor

        self.__state = moves.apply_move(self.__state, move)
        self.__selected_pair = None
        self.refresh_grid()
        self.update_scores()

        if moves.is_terminal(self.__state):
            self.show_result()
            return

        if actor == "Player":
            self.status_label.configure(text="Computer is thinking…")
            self.after(350, self._computer_move)

    def _computer_move(self):
        if self.__algorithm == ALGO_ALPHABETA:
            best_move = aiLogic.get_best_move_alphabeta(self.__state, depth=3)
        else:
            best_move = aiLogic.get_best_move(self.__state, depth=3)

        if best_move is None:
            self.show_result()
            return

        algo_label = "Alpha-Beta" if self.__algorithm == ALGO_ALPHABETA else "Minimax"
        move_type, val = best_move

        # Build description before applying (array changes after)
        arr = self.__state.get_num_array()
        if move_type == moves.SUM_PAIR:
            li, ri = (val - 1) * 2, (val - 1) * 2 + 1
            desc = f"summed pair {val}  ({arr[li]}, {arr[ri]})"
        else:
            desc = f"removed last  ({arr[-1]})"

        self._apply_move(best_move, actor="Computer")
        self.status_label.configure(text=f"Computer ({algo_label}): {desc}")

        if moves.is_terminal(self.__state):
            self.show_result()

    def _repaint_pairs(self, pair_nums, num_arr):
        """Recolour only the squares belonging to the given 1-based pair numbers."""
        for pair_num in pair_nums:
            for offset in (0, 1):
                index = (pair_num - 1) * 2 + offset
                if index >= len(num_arr):
                    continue
                if index not in self.__sq_widgets:
                    continue
                sq, lbl = self.__sq_widgets[index]
                pair_idx = index // 2
                is_lone  = (index == len(num_arr) - 1) and (len(num_arr) % 2 != 0)

                if is_lone:
                    color = self._LONE_COLOR
                elif self.__selected_pair is not None and pair_num == self.__selected_pair:
                    color = self._SEL_COLOR
                else:
                    color = self._PAIR_COLORS[pair_idx % 2]

                txt_color = "#222222" if color == self._SEL_COLOR else "white"
                sq.configure(fg_color=color)
                lbl.configure(text_color=txt_color)

    # ─────────────────────────── grid rendering ───────────────────────────────

    _PAIR_COLORS     = ["#9252AB", "#C23659"]
    _PAIR_COLORS_DIM = ["#4a2060", "#6b1f32"]
    _SEL_COLOR       = "#F0C040"
    _ACTED_COLOR     = "#E07020"
    _LONE_COLOR      = "#2a6496"

    def refresh_grid(self):
        self.__sq_widgets = {}

        # Build new frame fully before swapping to minimize flash
        new_frame = ctk.CTkFrame(self, fg_color="transparent")

        row_offset = 0

        # ── Previous row ──────────────────────────────────────────────────────
        if self.__prev_array is not None:
            ctk.CTkLabel(
                new_frame,
                text=f"↑  {self.__prev_actor}'s last move  (highlighted in orange)",
                font=("Arial", 11),
                text_color="#888888"
            ).grid(row=row_offset, column=0,
                   columnspan=len(self.__prev_array) + 1,
                   sticky="w", padx=4, pady=(0, 2))
            row_offset += 1

            self._draw_row(
                row_offset, self.__prev_array,
                dim=True, acted_move=self.__prev_move,
                parent=new_frame)
            row_offset += 2

            ctk.CTkLabel(
                new_frame,
                text="─" * 60,
                font=("Arial", 8),
                text_color="#555555"
            ).grid(row=row_offset, column=0,
                   columnspan=len(self.__prev_array) + 1,
                   pady=(0, 4))
            row_offset += 1

        # ── Current row ───────────────────────────────────────────────────────
        ctk.CTkLabel(
            new_frame,
            text="Current  ↓",
            font=("Arial", 11),
            text_color="#cccccc"
        ).grid(row=row_offset, column=0,
               columnspan=len(self.__state.get_num_array()) + 1,
               sticky="w", padx=4, pady=(0, 2))
        row_offset += 1

        self._draw_row(
            row_offset, self.__state.get_num_array(),
            dim=False, acted_move=None, interactive=True,
            parent=new_frame)
        row_offset += 1

        num_arr = self.__state.get_num_array()
        for pair_idx in range((len(num_arr) + 1) // 2):
            li = pair_idx * 2
            ri = li + 1
            if ri < len(num_arr):
                ctk.CTkLabel(
                    new_frame,
                    text=f" {pair_idx + 1} ",
                    font=("Arial", 10),
                    text_color="#777777"
                ).grid(row=row_offset, column=li, columnspan=2)

        # Atomic swap: destroy old, show new
        if hasattr(self, "_grid_frame"):
            self._grid_frame.destroy()
        self._grid_frame = new_frame
        self._grid_frame.pack(pady=(8, 4))

    def _draw_row(self, grid_row, num_arr, dim, acted_move, interactive=False, parent=None):
        acted_pair = acted_move[1] if (acted_move and acted_move[0] == moves.SUM_PAIR) else None
        acted_remove = acted_move is not None and acted_move[0] == moves.REMOVE_LAST

        for index, value in enumerate(num_arr):
            pair_idx = index // 2
            pair_num = pair_idx + 1
            is_lone  = (index == len(num_arr) - 1) and (len(num_arr) % 2 != 0)

            if dim:
                if (acted_pair is not None and pair_num == acted_pair) or \
                   (acted_remove and is_lone):
                    color     = self._ACTED_COLOR
                    txt_color = "white"
                else:
                    color     = self._PAIR_COLORS_DIM[pair_idx % 2]
                    txt_color = "#999999"
                size = 36
                font_size = 14
            else:
                if is_lone:
                    color = self._LONE_COLOR
                elif self.__selected_pair is not None and pair_num == self.__selected_pair:
                    color = self._SEL_COLOR
                else:
                    color = self._PAIR_COLORS[pair_idx % 2]
                txt_color = "#222222" if color == self._SEL_COLOR else "white"
                size = 42
                font_size = 17

            sq = ctk.CTkFrame(
                master=parent if parent is not None else self._grid_frame,
                width=size, height=size,
                corner_radius=7,
                fg_color=color)
            sq.grid(row=grid_row, column=index, padx=2, pady=2)
            sq.grid_propagate(False)

            lbl = ctk.CTkLabel(
                master=sq, text=str(value),
                text_color=txt_color,
                font=("Arial", font_size))
            lbl.place(relx=0.5, rely=0.5, anchor="center")

            if interactive:
                sq.bind("<Button-1>",  lambda e, i=index: self.on_square_click(i))
                lbl.bind("<Button-1>", lambda e, i=index: self.on_square_click(i))
                self.__sq_widgets[index] = (sq, lbl)

    # ─────────────────────────── other helpers ─────────────────────────────────

    def update_scores(self):
        self.score_label.configure(
            text=f"Player: {self.__state.first_player_score}   "
                 f"Computer: {self.__state.second_player_score}")

    def show_result(self):
        p = self.__state.first_player_score
        c = self.__state.second_player_score
        result = ("🎉 Player wins!" if p > c else
                  "🤖 Computer wins!" if c > p else
                  "🤝 It's a tie!")
        self.status_label.configure(
            text=f"Game over!  Player {p} – Computer {c}.  {result}")
        self.sum_btn.configure(state="disabled")
        self.remove_btn.configure(state="disabled")

    # ─────────────────────────── static layout ────────────────────────────────

    def _build_static_widgets(self):
        self.title("Game Window")
        self.geometry("1050x540")
        self.resizable(False, False)

        algo_name = "Alpha-Beta" if self.__algorithm == ALGO_ALPHABETA else "Minimax"

        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=20, pady=(12, 0))

        self.score_label = ctk.CTkLabel(
            top_bar, text="Player: 0   Computer: 0",
            font=("Arial", 15, "bold"))
        self.score_label.pack(side="left")

        ctk.CTkLabel(top_bar,
                     text=f"Algorithm: {algo_name}",
                     font=("Arial", 13), text_color="gray"
                     ).pack(side="right")

        self.status_label = ctk.CTkLabel(
            self,
            text="Your turn — click a pair, then press «Sum pair».",
            font=("Arial", 13))
        self.status_label.pack(pady=(6, 0))

        action_row = ctk.CTkFrame(self, fg_color="transparent")
        action_row.pack(pady=(8, 4))

        self.sum_btn = ctk.CTkButton(
            action_row, text="Sum pair  (+)",
            fg_color="#239618",
            command=self.on_sum_click,
            corner_radius=8, width=130, height=36,
            font=("Arial", 15), text_color="white")
        self.sum_btn.pack(side="left", padx=20)

        self.remove_btn = ctk.CTkButton(
            action_row, text="Remove last",
            fg_color="#BD7114",
            command=self.on_remove_click,
            corner_radius=8, width=130, height=36,
            font=("Arial", 15), text_color="white")
        self.remove_btn.pack(side="left", padx=20)

        # Nav buttons pinned to the bottom
        nav_row = ctk.CTkFrame(self, fg_color="transparent")
        nav_row.pack(side="bottom", pady=(4, 10))

        ctk.CTkButton(nav_row, text="Go To Main Menu",
                      fg_color="pink", text_color="purple",
                      command=self.on_go_to_menu, width=150
                      ).pack(side="left", padx=10)

        ctk.CTkButton(nav_row, text="Exit",
                      fg_color="red", text_color="white",
                      command=self.on_exit, width=80
                      ).pack(side="left", padx=10)