import random
import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkFont


class CasinoGame:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ LUCKY CASINO ✨")
        self.root.geometry("700x750")
        self.root.resizable(False, False)

        # Color scheme
        self.BG_COLOR = "#0f0f1e"
        self.PRIMARY_COLOR = "#ff006e"
        self.SECONDARY_COLOR = "#8338ec"
        self.SUCCESS_COLOR = "#06ffa5"
        self.DANGER_COLOR = "#ff006e"
        self.TEXT_COLOR = "#ffffff"
        self.ACCENT_COLOR = "#ffbe0b"

        self.root.configure(bg=self.BG_COLOR)

        # Game variables
        self.player_name = ""
        self.balance = 0
        self.current_bet = 0
        self.game_started = False

        self.setup_ui()

    def setup_ui(self):
        """Setup the main UI"""
        # Header
        header_frame = tk.Frame(self.root, bg=self.SECONDARY_COLOR)
        header_frame.pack(fill=tk.X, pady=0)

        title_font = tkFont.Font(family="Arial", size=32, weight="bold")
        title = tk.Label(
            header_frame,
            text="🎰 LUCKY CASINO 🎰",
            font=title_font,
            bg=self.SECONDARY_COLOR,
            fg=self.TEXT_COLOR
        )
        title.pack(pady=20)

        # Main content area
        self.content_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.show_login_screen()

    def show_login_screen(self):
        """Display login/initial setup screen"""
        self.clear_content()

        # Title
        title_font = tkFont.Font(family="Arial", size=20, weight="bold")
        tk.Label(
            self.content_frame,
            text="Welcome to Lucky Casino",
            font=title_font,
            bg=self.BG_COLOR,
            fg=self.ACCENT_COLOR
        ).pack(pady=20)

        # Rules section
        rules_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        rules_frame.pack(pady=20, padx=10, fill=tk.X)

        rules_font = tkFont.Font(family="Arial", size=11)
        rules_text = """
        📋 GAME RULES:
        
        🔹 Guess a number from 1 to 10
        🔹 Correct guess wins 10x your bet
        🔹 Wrong guess loses your bet
        🔹 Play until balance reaches $0
        """

        tk.Label(
            rules_frame,
            text=rules_text,
            font=rules_font,
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR,
            justify=tk.LEFT
        ).pack()

        # Player name input
        name_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        name_frame.pack(pady=15, fill=tk.X)

        tk.Label(
            name_frame,
            text="👤 Player Name:",
            font=tkFont.Font(family="Arial", size=12),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W)

        self.name_entry = self.create_entry(name_frame)
        self.name_entry.pack(fill=tk.X, pady=5)

        # Balance input
        balance_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        balance_frame.pack(pady=15, fill=tk.X)

        tk.Label(
            balance_frame,
            text="💰 Deposit Amount ($):",
            font=tkFont.Font(family="Arial", size=12),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W)

        self.balance_entry = self.create_entry(balance_frame)
        self.balance_entry.pack(fill=tk.X, pady=5)

        # Start button
        self.create_button(
            self.content_frame,
            "🚀 START PLAYING",
            self.start_game,
            self.PRIMARY_COLOR
        ).pack(pady=30)

    def create_entry(self, parent):
        """Create styled entry field"""
        entry = tk.Entry(
            parent,
            font=tkFont.Font(family="Arial", size=12),
            bg="#1a1a2e",
            fg=self.TEXT_COLOR,
            insertbackground=self.ACCENT_COLOR,
            relief=tk.FLAT,
            borderwidth=0
        )
        entry.pack(fill=tk.X, ipady=10)
        return entry

    def create_button(self, parent, text, command, color):
        """Create styled button"""
        button = tk.Button(
            parent,
            text=text,
            command=command,
            font=tkFont.Font(family="Arial", size=12, weight="bold"),
            bg=color,
            fg=self.TEXT_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            padx=20,
            pady=12,
            cursor="hand2"
        )
        button.pack(fill=tk.X)
        return button

    def start_game(self):
        """Start the game"""
        try:
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning(
                    "Input Error", "Please enter your name!")
                return

            balance = int(self.balance_entry.get())
            if balance <= 0:
                messagebox.showwarning(
                    "Input Error", "Deposit must be greater than $0!")
                return

            self.player_name = name
            self.balance = balance
            self.game_started = True
            self.show_game_screen()

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers!")

    def show_game_screen(self):
        """Display the main game screen"""
        self.clear_content()

        # Player info bar
        info_frame = tk.Frame(self.content_frame, bg=self.SECONDARY_COLOR)
        info_frame.pack(fill=tk.X, pady=10, padx=0, ipady=10)

        info_font = tkFont.Font(family="Arial", size=11, weight="bold")
        left_info = tk.Frame(info_frame, bg=self.SECONDARY_COLOR)
        left_info.pack(side=tk.LEFT, padx=10)

        tk.Label(
            left_info,
            text=f"👤 {self.player_name}",
            font=info_font,
            bg=self.SECONDARY_COLOR,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W)

        right_info = tk.Frame(info_frame, bg=self.SECONDARY_COLOR)
        right_info.pack(side=tk.RIGHT, padx=10)

        self.balance_label = tk.Label(
            right_info,
            text=f"💰 Balance: ${self.balance}",
            font=info_font,
            bg=self.SECONDARY_COLOR,
            fg=self.SUCCESS_COLOR
        )
        self.balance_label.pack(anchor=tk.E)

        # Bet input section
        bet_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        bet_frame.pack(pady=20, fill=tk.X)

        tk.Label(
            bet_frame,
            text="💵 Enter Bet Amount ($):",
            font=tkFont.Font(family="Arial", size=12),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W, pady=5)

        self.bet_entry = self.create_entry(bet_frame)
        self.bet_entry.pack(fill=tk.X, pady=5)
        self.bet_entry.insert(0, "10")

        # Number guess section
        guess_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        guess_frame.pack(pady=20, fill=tk.X)

        tk.Label(
            guess_frame,
            text="🎲 Guess a Number (1-10):",
            font=tkFont.Font(family="Arial", size=12),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W, pady=5)

        # Number buttons (grid)
        buttons_frame = tk.Frame(guess_frame, bg=self.BG_COLOR)
        buttons_frame.pack(pady=10)

        self.selected_number = tk.IntVar(value=1)

        for i in range(1, 11):
            btn = tk.Radiobutton(
                buttons_frame,
                text=str(i),
                variable=self.selected_number,
                value=i,
                font=tkFont.Font(family="Arial", size=11, weight="bold"),
                bg=self.BG_COLOR,
                fg=self.TEXT_COLOR,
                selectcolor=self.PRIMARY_COLOR,
                activebackground=self.SECONDARY_COLOR,
                activeforeground=self.TEXT_COLOR,
                borderwidth=2,
                relief=tk.RAISED
            )
            btn.grid(row=(i-1)//5, column=(i-1) % 5, padx=5, pady=5)

        # Play button
        self.create_button(
            self.content_frame,
            "🎯 SPIN & CLAIM",
            self.play_round,
            self.PRIMARY_COLOR
        ).pack(pady=20)

        # Result display
        self.result_label = tk.Label(
            self.content_frame,
            text="",
            font=tkFont.Font(family="Arial", size=13, weight="bold"),
            bg=self.BG_COLOR,
            fg=self.SUCCESS_COLOR,
            wraplength=600
        )
        self.result_label.pack(pady=10)

        # Exit button
        self.create_button(
            self.content_frame,
            "❌ QUIT",
            self.quit_game,
            "#ff006e"
        ).pack(pady=10)

    def play_round(self):
        """Play a single round"""
        try:
            bet = int(self.bet_entry.get())

            if bet <= 0 or bet > self.balance:
                messagebox.showwarning("Invalid Bet",
                                       f"Bet must be between $1 and ${self.balance}!")
                return

            guess = self.selected_number.get()
            lucky_number = random.randint(1, 10)

            if guess == lucky_number:
                win = bet * 10
                self.balance += win
                self.result_label.config(
                    text=f"🎉 FANTASTIC! 🎉\nYou guessed {guess} and won ${win}!\nLucky number was {lucky_number}",
                    fg=self.SUCCESS_COLOR
                )
            else:
                self.balance -= bet
                self.result_label.config(
                    text=f"😢 UNLUCKY 😢\nYou guessed {guess} but it was {lucky_number}.\nYou lost ${bet}",
                    fg=self.DANGER_COLOR
                )

            self.balance_label.config(text=f"💰 Balance: ${self.balance}")

            if self.balance <= 0:
                messagebox.showinfo("Game Over",
                                    f"Balance reached $0!\n\nGood game, {self.player_name}!")
                self.show_login_screen()
                return

        except ValueError:
            messagebox.showerror(
                "Input Error", "Please enter a valid bet amount!")

    def quit_game(self):
        """Quit the game"""
        final_balance = self.balance if self.game_started else 0
        messagebox.showinfo("Thank You!",
                            f"Thanks for playing, {self.player_name}!\nFinal Balance: ${final_balance}")
        self.root.destroy()

    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


def main():
    root = tk.Tk()
    game = CasinoGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
