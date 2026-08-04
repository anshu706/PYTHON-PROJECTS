import tkinter as tk
from tkinter import messagebox
from tkinter import font as tkFont
import random


class GuessGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎯 Mystery Number")
        self.root.geometry("500x650")
        self.root.resizable(False, False)

        # Color scheme - Modern blue & gradient
        self.BG_COLOR = "#0a0e27"
        self.CARD_COLOR = "#1a1f3a"
        self.PRIMARY_COLOR = "#00d4ff"
        self.SUCCESS_COLOR = "#00ff88"
        self.WARNING_COLOR = "#ffaa00"
        self.DANGER_COLOR = "#ff3366"
        self.TEXT_COLOR = "#ffffff"

        self.root.configure(bg=self.BG_COLOR)

        # Game state
        self.secret_number = random.randint(1, 10)
        self.attempts_left = 3
        self.attempt_count = 0
        self.game_over = False
        self.guess_history = []

        self.setup_ui()

    def setup_ui(self):
        """Setup the game UI"""
        # Main container
        main_container = tk.Frame(self.root, bg=self.BG_COLOR)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Title section
        title_font = tkFont.Font(family="Helvetica", size=28, weight="bold")
        title = tk.Label(
            main_container,
            text="🎯 MYSTERY NUMBER",
            font=title_font,
            bg=self.BG_COLOR,
            fg=self.PRIMARY_COLOR
        )
        title.pack(pady=20)

        subtitle_font = tkFont.Font(family="Helvetica", size=10)
        subtitle = tk.Label(
            main_container,
            text="Can you guess the secret number?",
            font=subtitle_font,
            bg=self.BG_COLOR,
            fg="#88a0ff"
        )
        subtitle.pack(pady=5)

        # Card container
        card = tk.Frame(main_container, bg=self.CARD_COLOR, relief=tk.FLAT)
        card.pack(fill=tk.BOTH, expand=True, pady=20, padx=5, ipady=20)

        # Range hint
        hint_font = tkFont.Font(family="Helvetica", size=11, weight="bold")
        tk.Label(
            card,
            text="Pick a number between 1 and 10",
            font=hint_font,
            bg=self.CARD_COLOR,
            fg=self.PRIMARY_COLOR
        ).pack(pady=15)

        # Attempts remaining
        self.attempts_frame = tk.Frame(card, bg=self.CARD_COLOR)
        self.attempts_frame.pack(pady=15)

        self.update_attempts_display()

        # Input section
        input_label = tk.Label(
            card,
            text="Your Guess:",
            font=tkFont.Font(family="Helvetica", size=11, weight="bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_COLOR
        )
        input_label.pack(pady=(20, 5))

        # Input field
        self.guess_entry = tk.Entry(
            card,
            font=tkFont.Font(family="Helvetica", size=14, weight="bold"),
            bg="#2a2f4a",
            fg=self.PRIMARY_COLOR,
            insertbackground=self.PRIMARY_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            justify=tk.CENTER
        )
        self.guess_entry.pack(fill=tk.X, padx=30, pady=10, ipady=12)
        self.guess_entry.bind("<Return>", lambda e: self.make_guess())

        # Submit button
        btn_font = tkFont.Font(family="Helvetica", size=11, weight="bold")
        self.submit_btn = tk.Button(
            card,
            text="🔮 CHECK GUESS",
            command=self.make_guess,
            font=btn_font,
            bg=self.PRIMARY_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            pady=10,
            cursor="hand2"
        )
        self.submit_btn.pack(fill=tk.X, padx=30, pady=15)

        # Feedback section
        self.feedback_label = tk.Label(
            card,
            text="",
            font=tkFont.Font(family="Helvetica", size=11, weight="bold"),
            bg=self.CARD_COLOR,
            fg=self.WARNING_COLOR,
            wraplength=400,
            height=2
        )
        self.feedback_label.pack(pady=15)

        # Guess history section
        history_label = tk.Label(
            card,
            text="📊 Your Guesses:",
            font=tkFont.Font(family="Helvetica", size=10, weight="bold"),
            bg=self.CARD_COLOR,
            fg=self.TEXT_COLOR
        )
        history_label.pack(pady=(20, 10))

        self.history_label = tk.Label(
            card,
            text="No guesses yet",
            font=tkFont.Font(family="Helvetica", size=10),
            bg=self.CARD_COLOR,
            fg="#6a7aaa"
        )
        self.history_label.pack()

        # Reset button
        reset_font = tkFont.Font(family="Helvetica", size=10, weight="bold")
        reset_btn = tk.Button(
            main_container,
            text="🔄 NEW GAME",
            command=self.reset_game,
            font=reset_font,
            bg=self.CARD_COLOR,
            fg=self.SUCCESS_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            pady=8
        )
        reset_btn.pack(fill=tk.X, pady=10)

    def update_attempts_display(self):
        """Update the attempts remaining display"""
        for widget in self.attempts_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(
            self.attempts_frame,
            text="Attempts Remaining:",
            font=tkFont.Font(family="Helvetica", size=9),
            bg=self.CARD_COLOR,
            fg="#88a0ff"
        ).pack()

        # Visual hearts/dots
        hearts_frame = tk.Frame(self.attempts_frame, bg=self.CARD_COLOR)
        hearts_frame.pack(pady=8)

        for i in range(self.attempts_left):
            tk.Label(
                hearts_frame,
                text="❤️",
                font=tkFont.Font(family="Helvetica", size=16),
                bg=self.CARD_COLOR
            ).pack(side=tk.LEFT, padx=5)

        # Remaining count
        tk.Label(
            self.attempts_frame,
            text=f"{self.attempt_count} / 3 guesses made",
            font=tkFont.Font(family="Helvetica", size=9),
            bg=self.CARD_COLOR,
            fg=self.TIP_COLOR if self.attempts_left > 1 else self.DANGER_COLOR
        ).pack()

    def make_guess(self):
        """Process the player's guess"""
        if self.game_over:
            messagebox.showinfo("Game Over", "Please start a new game!")
            return

        try:
            guess = int(self.guess_entry.get().strip())

            if guess < 1 or guess > 10:
                messagebox.showwarning(
                    "Invalid Input", "Please guess between 1 and 10!")
                return

            self.guess_entry.delete(0, tk.END)
            self.attempt_count += 1
            self.attempts_left -= 1
            self.guess_history.append(guess)

            # Check guess
            if guess == self.secret_number:
                self.feedback_label.config(
                    text=f"🎉 PERFECT! You found it!\nThe secret number was {self.secret_number}",
                    fg=self.SUCCESS_COLOR
                )
                self.game_over = True
                self.submit_btn.config(state=tk.DISABLED)
                messagebox.showinfo("Victory!",
                                    f"🎯 Congratulations! 🎯\n\nYou guessed correctly in {self.attempt_count} attempt(s)!")
            else:
                # Provide hint
                if guess < self.secret_number:
                    hint = "⬆️  Too low! Try higher."
                    color = self.WARNING_COLOR
                else:
                    hint = "⬇️  Too high! Try lower."
                    color = self.WARNING_COLOR

                self.feedback_label.config(text=hint, fg=color)

                if self.attempts_left <= 0:
                    self.feedback_label.config(
                        text=f"💔 Game Over!\nThe secret number was {self.secret_number}",
                        fg=self.DANGER_COLOR
                    )
                    self.game_over = True
                    self.submit_btn.config(state=tk.DISABLED)
                    messagebox.showinfo("Game Over",
                                        f"😔 You lost!\n\nThe secret number was {self.secret_number}\n\nYour guesses: {', '.join(map(str, self.guess_history))}")

            # Update UI
            self.update_attempts_display()
            self.update_history()

        except ValueError:
            messagebox.showerror(
                "Invalid Input", "Please enter a valid number!")

    def update_history(self):
        """Update the guess history display"""
        if self.guess_history:
            history_text = " → ".join(map(str, self.guess_history))
            self.history_label.config(text=history_text)
        else:
            self.history_label.config(text="No guesses yet")

    def reset_game(self):
        """Reset the game"""
        self.secret_number = random.randint(1, 10)
        self.attempts_left = 3
        self.attempt_count = 0
        self.game_over = False
        self.guess_history = []

        self.guess_entry.delete(0, tk.END)
        self.guess_entry.config(state=tk.NORMAL)
        self.submit_btn.config(state=tk.NORMAL)

        self.feedback_label.config(text="")
        self.update_attempts_display()
        self.update_history()

        self.guess_entry.focus()

    @property
    def TIP_COLOR(self):
        return self.SUCCESS_COLOR if self.attempts_left > 1 else self.DANGER_COLOR


def main():
    root = tk.Tk()
    app = GuessGameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
