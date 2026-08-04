import tkinter as tk

ACCOUNTS = [
    {
        "card_code": "k",
        "name": "Ken Kaneki",
        "title": "Midnight Account",
        "pin": 1234,
        "balance": 50000,
    },
    {
        "card_code": "s",
        "name": "Sasuke Uchiha",
        "title": "Storm Account",
        "pin": 5678,
        "balance": 100000,
    },
    {
        "card_code": "i",
        "name": "Itachi Uchiha",
        "title": "Shadow Account",
        "pin": 9123,
        "balance": 60000,
    },
    {
        "card_code": "l",
        "name": "Light Yagami",
        "title": "Nova Account",
        "pin": 8123,
        "balance": 40000,
    },
]


class AnteikuATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ATM")
        self.root.geometry("980x620")
        self.root.minsize(900, 560)
        self.root.configure(bg="#090f1c")

        self.selected_account = None
        self.pin_attempts = 0
        self.session_unlocked = False

        self._build_ui()

    def _build_ui(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="#090f1c")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._paint_background)

        self.shell = tk.Frame(self.canvas, bg="#10192f", bd=0)
        self.shell_window = self.canvas.create_window(
            0, 0, anchor="nw", window=self.shell, width=940, height=560
        )

        self.canvas.bind("<Configure>", self._resize_shell, add="+")

        self._build_header()
        self._build_body()

    def _build_header(self):
        header = tk.Frame(self.shell, bg="#111b33", padx=26, pady=14)
        header.pack(fill="x", pady=(18, 12), padx=18)

        tk.Label(
            header,
            text="ANTEIKU ATM v3",
            font=("Bahnschrift SemiBold", 22),
            fg="#7cf7ff",
            bg="#111b33",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Aesthetic Neon Banking Interface",
            font=("Consolas", 11),
            fg="#9fb9ff",
            bg="#111b33",
        ).pack(anchor="w", pady=(2, 0))

    def _build_body(self):
        body = tk.Frame(self.shell, bg="#10192f")
        body.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        self.left_panel = tk.Frame(body, bg="#0f1c36", padx=16, pady=16)
        self.left_panel.pack(side="left", fill="both",
                             expand=True, padx=(0, 10))

        self.right_panel = tk.Frame(body, bg="#0b162b", padx=16, pady=16)
        self.right_panel.pack(side="right", fill="y", padx=(10, 0))

        self._build_account_grid()
        self._build_pin_block()
        self._build_action_block()
        self._build_status_block()

    def _build_account_grid(self):
        tk.Label(
            self.left_panel,
            text="Select Card",
            font=("Bahnschrift SemiBold", 16),
            fg="#d6ebff",
            bg="#0f1c36",
        ).pack(anchor="w")

        tk.Label(
            self.left_panel,
            text="Tap a profile to insert a card",
            font=("Consolas", 10),
            fg="#8ea8d8",
            bg="#0f1c36",
        ).pack(anchor="w", pady=(2, 12))

        cards_wrap = tk.Frame(self.left_panel, bg="#0f1c36")
        cards_wrap.pack(fill="x")

        self.account_buttons = {}
        for index, account in enumerate(ACCOUNTS):
            card = tk.Frame(cards_wrap, bg="#15284f", padx=12, pady=10)
            row = index // 2
            col = index % 2
            card.grid(row=row, column=col, sticky="nsew", padx=6, pady=6)
            cards_wrap.grid_columnconfigure(col, weight=1)

            tk.Label(
                card,
                text=account["name"],
                font=("Bahnschrift", 12),
                fg="#f0f7ff",
                bg="#15284f",
            ).pack(anchor="w")
            tk.Label(
                card,
                text=f"{account['title']}  |  Code: {account['card_code'].upper()}",
                font=("Consolas", 9),
                fg="#9fc3ff",
                bg="#15284f",
            ).pack(anchor="w", pady=(2, 8))

            select_btn = tk.Button(
                card,
                text="Insert Card",
                font=("Bahnschrift", 10),
                bg="#2ec8ff",
                fg="#081324",
                activebackground="#7be7ff",
                activeforeground="#04101d",
                relief="flat",
                cursor="hand2",
                command=lambda acc=account: self.select_account(acc),
            )
            select_btn.pack(anchor="w")
            self.account_buttons[account["card_code"]] = (card, select_btn)

    def _build_pin_block(self):
        pin_frame = tk.Frame(self.left_panel, bg="#102245", padx=12, pady=12)
        pin_frame.pack(fill="x", pady=(14, 0))

        tk.Label(
            pin_frame,
            text="PIN Verification",
            font=("Bahnschrift", 13),
            fg="#e6f1ff",
            bg="#102245",
        ).pack(anchor="w")

        self.pin_hint = tk.Label(
            pin_frame,
            text="Enter your 4-digit PIN",
            font=("Consolas", 10),
            fg="#89a9de",
            bg="#102245",
        )
        self.pin_hint.pack(anchor="w", pady=(2, 8))

        entry_wrap = tk.Frame(pin_frame, bg="#102245")
        entry_wrap.pack(fill="x")

        self.pin_entry = tk.Entry(
            entry_wrap,
            show="*",
            font=("Consolas", 16),
            bg="#08152e",
            fg="#9cf9ff",
            insertbackground="#9cf9ff",
            relief="flat",
            width=14,
        )
        self.pin_entry.pack(side="left")

        tk.Button(
            entry_wrap,
            text="Unlock",
            font=("Bahnschrift", 11),
            bg="#48f0b8",
            fg="#04241c",
            activebackground="#83ffd6",
            relief="flat",
            padx=14,
            cursor="hand2",
            command=self.verify_pin,
        ).pack(side="left", padx=(10, 0))

    def _build_action_block(self):
        action_frame = tk.Frame(self.right_panel, bg="#0b162b")
        action_frame.pack(fill="x")

        tk.Label(
            action_frame,
            text="Session Actions",
            font=("Bahnschrift SemiBold", 16),
            fg="#d9ebff",
            bg="#0b162b",
        ).pack(anchor="w")

        self.account_name_label = tk.Label(
            action_frame,
            text="No card inserted",
            font=("Consolas", 10),
            fg="#89a0c7",
            bg="#0b162b",
        )
        self.account_name_label.pack(anchor="w", pady=(2, 12))

        tk.Label(
            action_frame,
            text="Withdraw Amount",
            font=("Consolas", 10),
            fg="#9fb9ea",
            bg="#0b162b",
        ).pack(anchor="w")

        self.withdraw_entry = tk.Entry(
            action_frame,
            font=("Consolas", 14),
            bg="#091125",
            fg="#d8f7ff",
            insertbackground="#d8f7ff",
            relief="flat",
            width=18,
        )
        self.withdraw_entry.pack(anchor="w", pady=(4, 12))

        self.balance_button = tk.Button(
            action_frame,
            text="Check Balance",
            font=("Bahnschrift", 11),
            bg="#37a5ff",
            fg="#041428",
            activebackground="#74c4ff",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            state="disabled",
            command=self.check_balance,
        )
        self.balance_button.pack(fill="x", pady=(0, 8))

        self.withdraw_button = tk.Button(
            action_frame,
            text="Withdraw Cash",
            font=("Bahnschrift", 11),
            bg="#ffbf4f",
            fg="#2a1a00",
            activebackground="#ffd891",
            relief="flat",
            padx=12,
            pady=6,
            cursor="hand2",
            state="disabled",
            command=self.withdraw_cash,
        )
        self.withdraw_button.pack(fill="x")

    def _build_status_block(self):
        panel = tk.Frame(self.right_panel, bg="#101d38", padx=12, pady=12)
        panel.pack(fill="both", expand=True, pady=(16, 0))

        tk.Label(
            panel,
            text="Live Status",
            font=("Bahnschrift", 13),
            fg="#e9f2ff",
            bg="#101d38",
        ).pack(anchor="w")

        self.status_label = tk.Label(
            panel,
            text="Insert a card to begin.",
            font=("Consolas", 10),
            fg="#9cb7e7",
            bg="#101d38",
            justify="left",
            wraplength=260,
        )
        self.status_label.pack(anchor="w", pady=(8, 0))

        self.receipt_box = tk.Text(
            panel,
            height=12,
            width=34,
            bg="#0a1428",
            fg="#b9fff4",
            insertbackground="#b9fff4",
            relief="flat",
            font=("Consolas", 10),
        )
        self.receipt_box.pack(fill="both", expand=True, pady=(12, 0))
        self.receipt_box.configure(state="disabled")

    def _paint_background(self, event):
        self.canvas.delete("bg")
        width = event.width
        height = event.height

        for i in range(height):
            ratio = i / max(height, 1)
            red = int(9 + (28 - 9) * ratio)
            green = int(15 + (9 - 15) * ratio)
            blue = int(28 + (63 - 28) * ratio)
            color = f"#{red:02x}{green:02x}{blue:02x}"
            self.canvas.create_line(0, i, width, i, fill=color, tags="bg")

        self.canvas.create_oval(
            width - 260,
            -120,
            width + 180,
            300,
            outline="",
            fill="#102857",
            tags="bg",
        )
        self.canvas.create_oval(
            -180,
            height - 280,
            320,
            height + 180,
            outline="",
            fill="#0f2d4f",
            tags="bg",
        )

    def _resize_shell(self, event):
        margin_x = 20
        margin_y = 20
        shell_width = max(event.width - (margin_x * 2), 860)
        shell_height = max(event.height - (margin_y * 2), 500)
        self.canvas.coords(self.shell_window, margin_x, margin_y)
        self.canvas.itemconfig(
            self.shell_window, width=shell_width, height=shell_height)

    def _write_receipt(self, lines):
        self.receipt_box.configure(state="normal")
        self.receipt_box.delete("1.0", "end")
        self.receipt_box.insert("end", "\n".join(lines))
        self.receipt_box.configure(state="disabled")

    def _enable_actions(self, enabled):
        state = "normal" if enabled else "disabled"
        self.balance_button.configure(state=state)
        self.withdraw_button.configure(state=state)

    def select_account(self, account):
        self.selected_account = account
        self.pin_attempts = 0
        self.session_unlocked = False
        self.pin_entry.delete(0, "end")
        self.withdraw_entry.delete(0, "end")
        self._enable_actions(False)

        for code, (card, _) in self.account_buttons.items():
            card.configure(bg="#15284f" if code !=
                           account["card_code"] else "#1d3f75")

        self.account_name_label.configure(text=f"Active: {account['name']}")
        self.pin_hint.configure(text="Enter PIN and press Unlock")
        self.status_label.configure(
            text=f"Card inserted for {account['name']}.\nPIN attempts left: 3"
        )

        self._write_receipt(
            [
                "---- ANTEIKU ATM ----",
                f"USER      : {account['name']}",
                f"PROFILE   : {account['title']}",
                "STATUS    : Card inserted",
                "",
                "Authenticate to continue.",
            ]
        )

    def verify_pin(self):
        if self.selected_account is None:
            self.status_label.configure(text="Select an account card first.")
            return

        pin_text = self.pin_entry.get().strip()
        if not pin_text.isdigit() or len(pin_text) != 4:
            self.status_label.configure(text="PIN must be exactly 4 digits.")
            return

        if int(pin_text) == self.selected_account["pin"]:
            self.session_unlocked = True
            self._enable_actions(True)
            self.status_label.configure(
                text=(
                    f"Access granted for {self.selected_account['name']}.\n"
                    "You can now check balance or withdraw cash."
                )
            )
            self.pin_hint.configure(text="Session unlocked")
            return

        self.pin_attempts += 1
        attempts_left = 3 - self.pin_attempts
        self.pin_entry.delete(0, "end")

        if attempts_left <= 0:
            self.selected_account = None
            self.session_unlocked = False
            self._enable_actions(False)
            self.account_name_label.configure(text="No card inserted")
            self.pin_hint.configure(text="Session blocked. Re-insert card")
            self.status_label.configure(
                text="PIN mismatch x3. Session blocked for safety.")
            self._write_receipt(
                [
                    "---- SECURITY NOTICE ----",
                    "AUTH FAILED",
                    "Reason: 3 incorrect PIN attempts",
                    "Action: Re-insert card to restart",
                ]
            )
            return

        self.status_label.configure(
            text=f"PIN mismatch. Attempts left: {attempts_left}"
        )

    def check_balance(self):
        if not self._session_ready():
            return

        balance = self.selected_account["balance"]
        self.status_label.configure(text=f"Current Balance: {balance}")
        self._write_receipt(
            [
                "---- BALANCE ENQUIRY ----",
                f"USER      : {self.selected_account['name']}",
                f"ACCOUNT   : {self.selected_account['title']}",
                f"BALANCE   : {balance}",
                "",
                "Thank you for banking with ANTEIKU.",
            ]
        )

    def withdraw_cash(self):
        if not self._session_ready():
            return

        amount_text = self.withdraw_entry.get().strip()
        if not amount_text.isdigit():
            self.status_label.configure(
                text="Enter a valid numeric withdraw amount.")
            return

        amount = int(amount_text)
        if amount <= 0:
            self.status_label.configure(
                text="Amount must be greater than zero.")
            return

        if amount > self.selected_account["balance"]:
            self.status_label.configure(
                text="Insufficient funds for this withdrawal.")
            return

        self.selected_account["balance"] -= amount
        remaining = self.selected_account["balance"]
        self.withdraw_entry.delete(0, "end")

        self.status_label.configure(
            text=f"Cash ready: {amount}\nRemaining Balance: {remaining}"
        )
        self._write_receipt(
            [
                "---- TRANSACTION RECEIPT ----",
                f"USER      : {self.selected_account['name']}",
                f"PROFILE   : {self.selected_account['title']}",
                f"WITHDRAWN : {amount}",
                f"REMAINING : {remaining}",
                "",
                "Please collect your cash safely.",
            ]
        )

    def _session_ready(self):
        if self.selected_account is None:
            self.status_label.configure(text="Insert a card to begin.")
            return False

        if not self.session_unlocked:
            self.status_label.configure(text="Unlock session with PIN first.")
            return False

        return True


def main():
    root = tk.Tk()
    AnteikuATMApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
