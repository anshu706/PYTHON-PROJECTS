import tkinter as tk
from tkinter import ttk

QUIZ = [
    {
        "question": "Which one is the first search engine on the internet?",
        "o1": "Google",
        "o2": "Archie",
        "o3": "Wais",
        "o4": "Altavista",
        "answer": 2,
    },
    {
        "question": "Which browser was invented in 1990?",
        "o1": "Internet Explorer",
        "o2": "Mosaic",
        "o3": "Mozilla",
        "o4": "Sinter",
        "answer": 4,
    },
    {
        "question": "First computer virus is known as?",
        "o1": "Rabbit",
        "o2": "Creeper virus",
        "o3": "Elk Cloner",
        "o4": "SCA virus",
        "answer": 2,
    },
    {
        "question": "Firewall in computer is used for?",
        "o1": "Security",
        "o2": "Data Transmission",
        "o3": "Monitoring",
        "o4": "Authentication",
        "answer": 1,
    },
    {
        "question": "Which one is not a database software?",
        "o1": "MySQL",
        "o2": "Oracle",
        "o3": "COBOL",
        "o4": "Sybase",
        "answer": 3,
    },
]


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Arcade Knowledge Arena")
        self.geometry("1120x720")
        self.minsize(960, 640)
        self.configure(bg="#151827")

        self.score = 0
        self.current_index = 0
        self.selected_answer = tk.IntVar(value=0)
        self.answer_vars = []

        self.colors = {
            "bg": "#151827",
            "surface": "#1D2133",
            "panel": "#242A40",
            "panel_soft": "#2D3450",
            "accent": "#86E1FC",
            "accent_2": "#CBA6F7",
            "accent_3": "#8BD5CA",
            "fg": "#EEF2FF",
            "muted": "#A3ACD6",
            "muted_2": "#7E87B3",
            "danger": "#F38BA8",
            "success": "#A6E3A1",
            "warning": "#F9E2AF",
            "button": "#7DC4E4",
            "button_hover": "#99D6F7",
            "button_alt": "#323A58",
        }

        self.fonts = {
            "hero": ("Segoe UI", 28, "bold"),
            "title": ("Segoe UI", 20, "bold"),
            "section": ("Segoe UI", 14, "bold"),
            "body": ("Segoe UI", 12),
            "body_bold": ("Segoe UI", 12, "bold"),
            "small": ("Segoe UI", 10),
            "score": ("Segoe UI", 26, "bold"),
        }

        self._build_background()
        self._build_shell()
        self._show_intro()

        self.bind("<Return>", self._handle_enter)
        self.bind("<Left>", lambda e: self._nudge_choice(-1))
        self.bind("<Right>", lambda e: self._nudge_choice(1))
        self.bind("<Escape>", lambda e: self._confirm_exit())

    def _build_background(self):
        self.bg_canvas = tk.Canvas(
            self, bg=self.colors["bg"], highlightthickness=0, bd=0)
        self.bg_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.bg_canvas.bind("<Configure>", self._draw_background)

    def _draw_background(self, event=None):
        self.bg_canvas.delete("all")
        width = max(self.bg_canvas.winfo_width(), 1)
        height = max(self.bg_canvas.winfo_height(), 1)
        self.bg_canvas.create_oval(
            width - 480, -160, width + 120, 420, fill="#20243B", outline="")
        self.bg_canvas.create_oval(-220, height - 280,
                                   260, height + 120, fill="#1B2035", outline="")
        self.bg_canvas.create_oval(
            width * 0.62, height * 0.52, width * 0.97, height * 0.96, fill="#1D243C", outline="")
        self.bg_canvas.create_line(0, 0, width, 0, fill="#2B3350", width=1)

    def _build_shell(self):
        self.shell = tk.Frame(self, bg=self.colors["bg"], padx=26, pady=22)
        self.shell.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.sidebar = tk.Frame(
            self.shell, bg=self.colors["surface"], width=320)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main = tk.Frame(self.shell, bg=self.colors["bg"])
        self.main.pack(side="left", fill="both", expand=True)

        self._build_sidebar()
        self.content = tk.Frame(self.main, bg=self.colors["bg"])
        self.content.pack(fill="both", expand=True, padx=(22, 0))

    def _build_sidebar(self):
        header = tk.Frame(
            self.sidebar, bg=self.colors["surface"], padx=22, pady=24)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Arcade Knowledge Arena",
            font=self.fonts["title"],
            bg=self.colors["surface"],
            fg=self.colors["accent"],
            justify="left",
            wraplength=260,
        ).pack(anchor="w")
        tk.Label(
            header,
            text="A cleaner quiz experience with stronger rhythm, clarity, and visual feedback.",
            font=self.fonts["small"],
            bg=self.colors["surface"],
            fg=self.colors["muted"],
            justify="left",
            wraplength=260,
        ).pack(anchor="w", pady=(10, 0))

        stats = tk.Frame(self.sidebar, bg=self.colors["surface"], padx=22)
        stats.pack(fill="x", pady=(0, 8))

        self.score_var = tk.StringVar(value="0")
        self.question_var = tk.StringVar(value="0 / 0")
        self.progress_label_var = tk.StringVar(value="Ready to begin")

        self._stat_tile(stats, "Score", self.score_var,
                        self.colors["accent_2"])
        self._stat_tile(stats, "Question", self.question_var,
                        self.colors["accent_3"])

        status = tk.Frame(
            self.sidebar, bg=self.colors["panel"], padx=18, pady=18)
        status.pack(fill="x", padx=18, pady=(10, 18))

        tk.Label(
            status,
            text="Session Status",
            font=self.fonts["small"],
            bg=self.colors["panel"],
            fg=self.colors["muted"],
        ).pack(anchor="w")
        tk.Label(
            status,
            textvariable=self.progress_label_var,
            font=self.fonts["body_bold"],
            bg=self.colors["panel"],
            fg=self.colors["fg"],
            wraplength=260,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

        controls = tk.Frame(self.sidebar, bg=self.colors["surface"], padx=18)
        controls.pack(fill="x", pady=(0, 18))

        self.start_btn = self._button(
            controls, "Start Quiz", self._start_quiz, fill=True, accent=True)
        self.start_btn.pack(fill="x", pady=(0, 12), ipady=12)

        self.rules_btn = self._button(
            controls, "View Rules", self._show_rules, fill=True, accent=False)
        self.rules_btn.pack(fill="x", pady=(0, 12), ipady=12)

        self.reset_btn = self._button(
            controls, "Reset Session", self._reset_session, fill=True, accent=False)
        self.reset_btn.pack(fill="x", ipady=12)

        footer = tk.Frame(
            self.sidebar, bg=self.colors["surface"], padx=22, pady=18)
        footer.pack(side="bottom", fill="x")
        tk.Label(
            footer,
            text="Tip: Use the buttons or press Enter to submit.",
            font=self.fonts["small"],
            bg=self.colors["surface"],
            fg=self.colors["muted_2"],
            wraplength=260,
            justify="left",
        ).pack(anchor="w")

    def _stat_tile(self, parent, label, value_var, accent):
        card = tk.Frame(parent, bg=self.colors["panel"], padx=16, pady=14)
        card.pack(fill="x", pady=(0, 12))
        tk.Label(card, text=label, font=self.fonts["small"],
                 bg=self.colors["panel"], fg=self.colors["muted"]).pack(anchor="w")
        tk.Label(card, textvariable=value_var, font=("Segoe UI", 18, "bold"),
                 bg=self.colors["panel"], fg=accent).pack(anchor="w", pady=(4, 0))

    def _button(self, parent, text, command, fill=False, accent=False):
        bg = self.colors["button"] if accent else self.colors["button_alt"]
        fg = "#10131E" if accent else self.colors["fg"]
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=self.fonts["body_bold"],
            bg=bg,
            fg=fg,
            bd=0,
            relief="flat",
            cursor="hand2",
            activebackground=self.colors["button_hover"] if accent else self.colors["panel_soft"],
            activeforeground="#10131E" if accent else self.colors["fg"],
        )
        self._hover(button, bg, self.colors["button_hover"]
                    if accent else self.colors["panel_soft"], fg, fg)
        return button

    def _hover(self, widget, bg_normal, bg_hover, fg_normal, fg_hover):
        widget.bind("<Enter>", lambda e: widget.config(
            bg=bg_hover, fg=fg_hover))
        widget.bind("<Leave>", lambda e: widget.config(
            bg=bg_normal, fg=fg_normal))

    def _clear_content(self):
        for child in self.content.winfo_children():
            child.destroy()

    def _card(self, parent, padx=24, pady=24):
        return tk.Frame(parent, bg=self.colors["panel"], padx=padx, pady=pady)

    def _show_intro(self):
        self._clear_content()
        self.progress_label_var.set("Ready to begin")
        self.question_var.set(f"0 / {len(QUIZ)}")
        self.score_var.set("0")
        self.selected_answer.set(0)
        self.current_index = 0
        self.score = 0
        self.answer_vars = []

        hero = self._card(self.content, padx=30, pady=30)
        hero.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.92)

        top = tk.Frame(hero, bg=self.colors["panel"])
        top.pack(fill="x")

        badge = tk.Frame(top, bg=self.colors["panel_soft"], padx=14, pady=10)
        badge.pack(anchor="w")
        tk.Label(
            badge,
            text="ARCADE MODE",
            font=self.fonts["small"],
            bg=self.colors["panel_soft"],
            fg=self.colors["accent"],
        ).pack()

        tk.Label(
            hero,
            text="A sharper quiz interface with better pacing and clearer feedback.",
            font=self.fonts["hero"],
            bg=self.colors["panel"],
            fg=self.colors["fg"],
            justify="left",
            wraplength=700,
        ).pack(anchor="w", pady=(18, 10))

        tk.Label(
            hero,
            text="Select an answer, submit it, and watch the scoreboard update live.",
            font=self.fonts["body"],
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify="left",
            wraplength=720,
        ).pack(anchor="w")

        preview = tk.Frame(hero, bg=self.colors["panel"], pady=24)
        preview.pack(fill="x")

        self._preview_chip(preview, f"Questions: {len(QUIZ)}")
        self._preview_chip(preview, f"Points per correct: 5")
        self._preview_chip(preview, f"Max score: {len(QUIZ) * 5}")

        actions = tk.Frame(hero, bg=self.colors["panel"], pady=8)
        actions.pack(fill="x")

        start_btn = self._button(
            actions, "Start Quiz", self._start_quiz, accent=True)
        start_btn.pack(side="left", ipady=12, ipadx=10)
        self._hover(start_btn, self.colors["button"],
                    self.colors["button_hover"], "#10131E", "#10131E")

        rules_btn = self._button(actions, "See Rules",
                                 self._show_rules, accent=False)
        rules_btn.pack(side="left", padx=(12, 0), ipady=12, ipadx=10)
        self._hover(rules_btn, self.colors["button_alt"],
                    self.colors["panel_soft"], self.colors["fg"], self.colors["fg"])

    def _preview_chip(self, parent, text):
        chip = tk.Frame(parent, bg=self.colors["panel_soft"], padx=14, pady=10)
        chip.pack(side="left", padx=(0, 12))
        tk.Label(chip, text=text, font=self.fonts["small"],
                 bg=self.colors["panel_soft"], fg=self.colors["fg"]).pack()

    def _show_rules(self):
        self._clear_content()
        rules = self._card(self.content, padx=30, pady=28)
        rules.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88)

        tk.Label(rules, text="Rules Briefing",
                 font=self.fonts["title"], bg=self.colors["panel"], fg=self.colors["accent_2"]).pack(anchor="w")
        tk.Label(
            rules,
            text="1. Correct answer: +5 points\n2. Wrong answer: +0 points\n3. Input is selected with the buttons\n4. You can replay as often as you want",
            font=self.fonts["body"],
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify="left",
            anchor="w",
        ).pack(anchor="w", pady=(14, 0))

        tip = tk.Frame(rules, bg=self.colors["panel_soft"], padx=18, pady=18)
        tip.pack(fill="x", pady=(22, 0))
        tk.Label(tip, text="UX note", font=self.fonts["small"],
                 bg=self.colors["panel_soft"], fg=self.colors["accent"]).pack(anchor="w")
        tk.Label(
            tip,
            text="The interface is designed to keep one primary action visible at a time, reduce cognitive load, and provide immediate feedback after every answer.",
            font=self.fonts["body"],
            bg=self.colors["panel_soft"],
            fg=self.colors["fg"],
            wraplength=720,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        actions = tk.Frame(rules, bg=self.colors["panel"], pady=18)
        actions.pack(fill="x")
        back_btn = self._button(
            actions, "Back", self._show_intro, accent=False)
        back_btn.pack(side="left", ipady=12, ipadx=12)
        self._hover(back_btn, self.colors["button_alt"],
                    self.colors["panel_soft"], self.colors["fg"], self.colors["fg"])

    def _start_quiz(self):
        self.score = 0
        self.current_index = 0
        self.selected_answer.set(0)
        self.answer_vars = []
        self._show_question()

    def _show_question(self):
        self._clear_content()

        if self.current_index >= len(QUIZ):
            self._show_result()
            return

        question = QUIZ[self.current_index]
        self.question_var.set(f"{self.current_index + 1} / {len(QUIZ)}")
        self.score_var.set(str(self.score))
        self.progress_label_var.set(
            f"Question {self.current_index + 1}: choose the strongest answer.")

        wrapper = self._card(self.content, padx=28, pady=28)
        wrapper.place(relx=0.5, rely=0.5, anchor="center",
                      relwidth=0.92, relheight=0.88)

        header = tk.Frame(wrapper, bg=self.colors["panel"])
        header.pack(fill="x")

        tk.Label(
            header,
            text=f"Question {self.current_index + 1}",
            font=self.fonts["small"],
            bg=self.colors["panel"],
            fg=self.colors["accent"],
        ).pack(anchor="w")

        tk.Label(
            header,
            text=question["question"],
            font=self.fonts["title"],
            bg=self.colors["panel"],
            fg=self.colors["fg"],
            justify="left",
            wraplength=760,
        ).pack(anchor="w", pady=(10, 0))

        top_row = tk.Frame(wrapper, bg=self.colors["panel"], pady=16)
        top_row.pack(fill="x")
        self._question_chip(top_row, f"Score: {self.score}")
        self._question_chip(
            top_row, f"Question {self.current_index + 1} of {len(QUIZ)}")
        self._question_chip(top_row, f"Goal: clean accuracy")

        progress_outer = tk.Frame(wrapper, bg=self.colors["panel"], pady=6)
        progress_outer.pack(fill="x")
        tk.Label(
            progress_outer,
            text="Progress",
            font=self.fonts["small"],
            bg=self.colors["panel"],
            fg=self.colors["muted"],
        ).pack(anchor="w")

        progress_value = self.current_index / len(QUIZ)
        self.progress = ttk.Progressbar(
            wrapper, orient="horizontal", mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=(8, 18))
        self.progress["value"] = progress_value * 100

        options = tk.Frame(wrapper, bg=self.colors["panel"])
        options.pack(fill="both", expand=True)
        options.columnconfigure(0, weight=1)
        options.columnconfigure(1, weight=1)

        self.selected_answer.set(0)
        self.answer_vars = [
            (1, question["o1"]),
            (2, question["o2"]),
            (3, question["o3"]),
            (4, question["o4"]),
        ]

        for idx, (choice_value, choice_text) in enumerate(self.answer_vars):
            row = idx // 2
            col = idx % 2
            self._answer_card(options, row, col, choice_value, choice_text)

        bottom = tk.Frame(wrapper, bg=self.colors["panel"], pady=16)
        bottom.pack(fill="x")

        submit_btn = self._button(
            bottom, "Submit Answer", self._submit_answer, accent=True)
        submit_btn.pack(side="left", ipady=12, ipadx=14)
        self._hover(submit_btn, self.colors["button"],
                    self.colors["button_hover"], "#10131E", "#10131E")

        skip_btn = self._button(bottom, "Back to Menu",
                                self._show_intro, accent=False)
        skip_btn.pack(side="left", padx=(12, 0), ipady=12, ipadx=14)
        self._hover(skip_btn, self.colors["button_alt"],
                    self.colors["panel_soft"], self.colors["fg"], self.colors["fg"])

        hint = tk.Label(
            bottom,
            text="Press Enter to submit. Arrow keys can move through options.",
            font=self.fonts["small"],
            bg=self.colors["panel"],
            fg=self.colors["muted_2"],
        )
        hint.pack(side="right")

    def _question_chip(self, parent, text):
        chip = tk.Frame(parent, bg=self.colors["panel_soft"], padx=14, pady=8)
        chip.pack(side="left", padx=(0, 10))
        tk.Label(chip, text=text, font=self.fonts["small"],
                 bg=self.colors["panel_soft"], fg=self.colors["fg"]).pack()

    def _answer_card(self, parent, row, col, value, label):
        card = tk.Frame(
            parent, bg=self.colors["panel_soft"], padx=16, pady=16, cursor="hand2")
        card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)

        radio = tk.Radiobutton(
            card,
            text=label,
            variable=self.selected_answer,
            value=value,
            font=self.fonts["body_bold"],
            bg=self.colors["panel_soft"],
            fg=self.colors["fg"],
            selectcolor=self.colors["panel_soft"],
            activebackground=self.colors["panel_soft"],
            activeforeground=self.colors["fg"],
            bd=0,
            anchor="w",
            justify="left",
            wraplength=300,
            highlightthickness=0,
        )
        radio.pack(fill="both", expand=True)

        card.bind("<Button-1>", lambda e, v=value: self.selected_answer.set(v))
        radio.bind("<Button-1>", lambda e,
                   v=value: self.selected_answer.set(v))
        self._hover(card, self.colors["panel_soft"],
                    self.colors["button_alt"], self.colors["fg"], self.colors["fg"])

    def _submit_answer(self):
        answer = self.selected_answer.get()
        if answer == 0:
            self.progress_label_var.set("Pick an answer before continuing.")
            return

        correct = QUIZ[self.current_index]["answer"]
        if answer == correct:
            self.score += 5
            self.progress_label_var.set("Correct. +5 points locked in.")
        else:
            self.progress_label_var.set(
                f"Missed. The correct answer was option {correct}.")

        self.current_index += 1
        self.score_var.set(str(self.score))
        self.after(260, self._show_question)

    def _show_result(self):
        self._clear_content()
        max_score = len(QUIZ) * 5
        accuracy = (self.score / max_score) * 100 if max_score else 0

        self.question_var.set(f"{len(QUIZ)} / {len(QUIZ)}")
        self.score_var.set(str(self.score))
        self.progress_label_var.set("Session complete")

        wrapper = self._card(self.content, padx=32, pady=32)
        wrapper.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9)

        tk.Label(
            wrapper,
            text="Scoreboard",
            font=self.fonts["section"],
            bg=self.colors["panel"],
            fg=self.colors["accent_2"],
        ).pack(anchor="w")

        tk.Label(
            wrapper,
            text=f"{self.score} / {max_score}",
            font=self.fonts["score"],
            bg=self.colors["panel"],
            fg=self.colors["fg"],
        ).pack(anchor="w", pady=(10, 0))

        tk.Label(
            wrapper,
            text=f"Accuracy: {accuracy:.0f}%",
            font=self.fonts["body"],
            bg=self.colors["panel"],
            fg=self.colors["muted"],
        ).pack(anchor="w", pady=(8, 0))

        summary = tk.Frame(
            wrapper, bg=self.colors["panel_soft"], padx=18, pady=18)
        summary.pack(fill="x", pady=(22, 16))

        if self.score >= 20:
            verdict = "Elite run. You owned the arena today."
            accent = self.colors["success"]
        elif self.score >= 10:
            verdict = "Strong session. One more pass will sharpen the score."
            accent = self.colors["warning"]
        else:
            verdict = "Warm-up tier. Re-enter and tighten the timing."
            accent = self.colors["danger"]

        tk.Label(summary, text="Result",
                 font=self.fonts["small"], bg=self.colors["panel_soft"], fg=self.colors["muted"]).pack(anchor="w")
        tk.Label(
            summary,
            text=verdict,
            font=self.fonts["body_bold"],
            bg=self.colors["panel_soft"],
            fg=accent,
            wraplength=760,
            justify="left",
        ).pack(anchor="w", pady=(6, 0))

        progress = ttk.Progressbar(
            wrapper, orient="horizontal", mode="determinate", maximum=max_score)
        progress.pack(fill="x", pady=(10, 6))
        progress["value"] = self.score

        actions = tk.Frame(wrapper, bg=self.colors["panel"], pady=8)
        actions.pack(fill="x")

        replay_btn = self._button(
            actions, "Play Again", self._start_quiz, accent=True)
        replay_btn.pack(side="left", ipady=12, ipadx=14)
        self._hover(replay_btn, self.colors["button"],
                    self.colors["button_hover"], "#10131E", "#10131E")

        menu_btn = self._button(actions, "Main Menu",
                                self._show_intro, accent=False)
        menu_btn.pack(side="left", padx=(12, 0), ipady=12, ipadx=14)
        self._hover(menu_btn, self.colors["button_alt"],
                    self.colors["panel_soft"], self.colors["fg"], self.colors["fg"])

    def _reset_session(self):
        self.score = 0
        self.current_index = 0
        self.selected_answer.set(0)
        self.score_var.set("0")
        self.question_var.set(f"0 / {len(QUIZ)}")
        self.progress_label_var.set("Session reset. Ready when you are.")
        self._show_intro()

    def _handle_enter(self, event=None):
        if self.current_index < len(QUIZ):
            self._submit_answer()
        else:
            self._show_intro()

    def _nudge_choice(self, direction):
        if self.current_index >= len(QUIZ):
            return
        current = self.selected_answer.get()
        if current == 0:
            self.selected_answer.set(1 if direction > 0 else 4)
            return
        next_value = current + direction
        if next_value < 1:
            next_value = 4
        if next_value > 4:
            next_value = 1
        self.selected_answer.set(next_value)

    def _confirm_exit(self):
        popup = tk.Toplevel(self)
        popup.title("Exit Arena")
        popup.geometry("360x180")
        popup.configure(bg=self.colors["bg"])
        popup.transient(self)
        popup.grab_set()
        popup.resizable(False, False)

        tk.Label(
            popup,
            text="Leave the arena?",
            font=self.fonts["title"],
            bg=self.colors["bg"],
            fg=self.colors["fg"],
        ).pack(pady=(28, 8))
        tk.Label(
            popup,
            text="You can return and replay at any time.",
            font=self.fonts["body"],
            bg=self.colors["bg"],
            fg=self.colors["muted"],
        ).pack()

        actions = tk.Frame(popup, bg=self.colors["bg"])
        actions.pack(pady=26)

        yes = tk.Button(
            actions,
            text="Exit",
            command=self.destroy,
            font=self.fonts["body_bold"],
            bg=self.colors["danger"],
            fg="#10131E",
            bd=0,
            cursor="hand2",
        )
        yes.pack(side="left", padx=8, ipadx=16, ipady=10)

        no = tk.Button(
            actions,
            text="Cancel",
            command=popup.destroy,
            font=self.fonts["body_bold"],
            bg=self.colors["button_alt"],
            fg=self.colors["fg"],
            bd=0,
            cursor="hand2",
        )
        no.pack(side="left", padx=8, ipadx=16, ipady=10)


def main():
    app = QuizApp()
    app.mainloop()


if __name__ == "__main__":
    main()
