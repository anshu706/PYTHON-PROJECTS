import tkinter as tk

PRICES = {
    "Cosmetics": {
        "Body Soap": 10,
        "Hair Cream": 25,
        "Hair Spray": 50,
        "Body Spray": 50,
    },
    "Grocery": {
        "Sugar": 100,
        "Tea": 15,
        "Coffee": 50,
        "Rice": 150,
        "Wheat": 160,
    },
    "Beverages": {
        "Pepsi": 30,
        "Sprite": 35,
        "Coke": 30,
        "Mojitos": 25,
        "Thumbs Up": 35,
    },
}


class BillingDeskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ANTEIKU Smart Billing Desk")
        self.root.geometry("1120x680")
        self.root.minsize(980, 620)
        self.root.configure(bg="#f6efe4")

        self.quantity_vars = {}
        self.total_vars = {
            "Cosmetics": tk.StringVar(value="Rs 0"),
            "Grocery": tk.StringVar(value="Rs 0"),
            "Beverages": tk.StringVar(value="Rs 0"),
            "Grand": tk.StringVar(value="Rs 0"),
        }

        self.customer_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.customer_id_var = tk.StringVar()
        self.status_var = tk.StringVar(
            value="Fill details, set quantities, then generate invoice.")

        self._build_ui()

    def _build_ui(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0, bg="#f6efe4")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._paint_background)

        self.shell = tk.Frame(self.canvas, bg="#fff9f0")
        self.shell_window = self.canvas.create_window(
            0, 0, anchor="nw", window=self.shell)
        self.canvas.bind("<Configure>", self._resize_shell, add="+")

        self._build_header()
        self._build_main()

    def _build_header(self):
        header = tk.Frame(self.shell, bg="#362c2a", padx=24, pady=16)
        header.pack(fill="x", padx=18, pady=(18, 10))

        tk.Label(
            header,
            text="ANTEIKU SMART BILLING DESK",
            font=("Georgia", 20, "bold"),
            fg="#ffe9c8",
            bg="#362c2a",
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Boutique Checkout Interface",
            font=("Trebuchet MS", 11),
            fg="#e5cfa7",
            bg="#362c2a",
        ).pack(anchor="w", pady=(2, 0))

    def _build_main(self):
        body = tk.Frame(self.shell, bg="#fff9f0")
        body.pack(fill="both", expand=True, padx=18, pady=(0, 18))

        left = tk.Frame(body, bg="#fff9f0")
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = tk.Frame(body, bg="#f1e6d6", padx=14, pady=14)
        right.pack(side="right", fill="y", padx=(10, 0))

        self._build_customer_card(left)
        self._build_products_card(left)
        self._build_actions_card(left)

        self._build_totals_card(right)
        self._build_invoice_card(right)

    def _build_customer_card(self, parent):
        frame = tk.Frame(parent, bg="#f7efdf", padx=14, pady=12)
        frame.pack(fill="x")

        tk.Label(
            frame,
            text="Customer Details",
            font=("Georgia", 14, "bold"),
            fg="#463533",
            bg="#f7efdf",
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        tk.Label(frame, text="Name", font=("Trebuchet MS", 10), fg="#5b4a45", bg="#f7efdf").grid(
            row=1, column=0, sticky="w", pady=4
        )
        tk.Entry(frame, textvariable=self.customer_name_var, font=("Trebuchet MS", 11), width=26).grid(
            row=1, column=1, padx=(8, 20), pady=4
        )

        tk.Label(frame, text="Phone", font=("Trebuchet MS", 10), fg="#5b4a45", bg="#f7efdf").grid(
            row=1, column=2, sticky="w", pady=4
        )
        tk.Entry(frame, textvariable=self.phone_var, font=("Trebuchet MS", 11), width=18).grid(
            row=1, column=3, padx=(8, 0), pady=4
        )

        tk.Label(frame, text="Customer ID", font=("Trebuchet MS", 10), fg="#5b4a45", bg="#f7efdf").grid(
            row=2, column=0, sticky="w", pady=4
        )
        tk.Entry(frame, textvariable=self.customer_id_var, font=("Trebuchet MS", 11), width=14).grid(
            row=2, column=1, sticky="w", padx=(8, 0), pady=4
        )

    def _build_products_card(self, parent):
        frame = tk.Frame(parent, bg="#fff6ea", padx=14, pady=12)
        frame.pack(fill="both", expand=True, pady=(12, 0))

        tk.Label(
            frame,
            text="Product Quantities",
            font=("Georgia", 14, "bold"),
            fg="#463533",
            bg="#fff6ea",
        ).pack(anchor="w", pady=(0, 8))

        categories = tk.Frame(frame, bg="#fff6ea")
        categories.pack(fill="both", expand=True)

        for col, (category, items) in enumerate(PRICES.items()):
            card = tk.Frame(categories, bg="#fff1db", padx=10, pady=10)
            card.grid(row=0, column=col, sticky="nsew", padx=5)
            categories.grid_columnconfigure(col, weight=1)

            tk.Label(
                card,
                text=category,
                font=("Trebuchet MS", 12, "bold"),
                fg="#6c4e3f",
                bg="#fff1db",
            ).pack(anchor="w", pady=(0, 8))

            for item, price in items.items():
                row = tk.Frame(card, bg="#fff1db")
                row.pack(fill="x", pady=2)

                tk.Label(
                    row,
                    text=f"{item} (Rs {price})",
                    font=("Trebuchet MS", 10),
                    fg="#5f4a43",
                    bg="#fff1db",
                    width=19,
                    anchor="w",
                ).pack(side="left")

                qty = tk.IntVar(value=0)
                spin = tk.Spinbox(
                    row,
                    from_=0,
                    to=99,
                    textvariable=qty,
                    width=5,
                    command=self.update_totals,
                    font=("Trebuchet MS", 10),
                )
                spin.pack(side="right")
                spin.bind("<KeyRelease>", lambda _event: self.update_totals())

                self.quantity_vars[(category, item)] = qty

    def _build_actions_card(self, parent):
        frame = tk.Frame(parent, bg="#f7efdf", padx=14, pady=12)
        frame.pack(fill="x", pady=(12, 0))

        tk.Button(
            frame,
            text="Generate Invoice",
            font=("Trebuchet MS", 11, "bold"),
            bg="#6f3f2e",
            fg="#fff2de",
            activebackground="#8b543f",
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.generate_invoice,
        ).pack(side="left")

        tk.Button(
            frame,
            text="Clear All",
            font=("Trebuchet MS", 11),
            bg="#d7c4a6",
            fg="#463533",
            activebackground="#e8d7bd",
            relief="flat",
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.clear_all,
        ).pack(side="left", padx=(10, 0))

        tk.Label(
            frame,
            textvariable=self.status_var,
            font=("Trebuchet MS", 10),
            fg="#5e4e48",
            bg="#f7efdf",
            wraplength=520,
            justify="left",
        ).pack(side="left", padx=(14, 0))

    def _build_totals_card(self, parent):
        frame = tk.Frame(parent, bg="#fff3df", padx=12, pady=12)
        frame.pack(fill="x")

        tk.Label(
            frame,
            text="Totals",
            font=("Georgia", 14, "bold"),
            fg="#4a362e",
            bg="#fff3df",
        ).pack(anchor="w", pady=(0, 10))

        for label, key in [
            ("Cosmetics", "Cosmetics"),
            ("Grocery", "Grocery"),
            ("Beverages", "Beverages"),
            ("Grand Total", "Grand"),
        ]:
            row = tk.Frame(frame, bg="#fff3df")
            row.pack(fill="x", pady=2)
            tk.Label(
                row,
                text=label,
                font=("Trebuchet MS", 10),
                fg="#604841",
                bg="#fff3df",
            ).pack(side="left")
            tk.Label(
                row,
                textvariable=self.total_vars[key],
                font=("Trebuchet MS", 10, "bold"),
                fg="#6f3f2e",
                bg="#fff3df",
            ).pack(side="right")

    def _build_invoice_card(self, parent):
        frame = tk.Frame(parent, bg="#fff7e9", padx=12, pady=12)
        frame.pack(fill="both", expand=True, pady=(12, 0))

        tk.Label(
            frame,
            text="Invoice Preview",
            font=("Georgia", 13, "bold"),
            fg="#4a362e",
            bg="#fff7e9",
        ).pack(anchor="w", pady=(0, 8))

        self.invoice_box = tk.Text(
            frame,
            width=38,
            height=24,
            bg="#fffef9",
            fg="#4f423d",
            relief="flat",
            font=("Consolas", 10),
        )
        self.invoice_box.pack(fill="both", expand=True)
        self.invoice_box.insert(
            "end",
            "ANTEIKU Billing\n"
            "------------------------------\n"
            "Invoice will appear here.\n",
        )
        self.invoice_box.configure(state="disabled")

    def _paint_background(self, event):
        self.canvas.delete("bg")
        width = event.width
        height = event.height

        for i in range(height):
            ratio = i / max(height, 1)
            red = int(246 + (229 - 246) * ratio)
            green = int(239 + (215 - 239) * ratio)
            blue = int(228 + (195 - 228) * ratio)
            color = f"#{red:02x}{green:02x}{blue:02x}"
            self.canvas.create_line(0, i, width, i, fill=color, tags="bg")

        self.canvas.create_oval(-180, -150, 260, 230,
                                fill="#efe0c7", outline="", tags="bg")
        self.canvas.create_oval(
            width - 280, height - 220, width + 140, height + 140, fill="#e4d3b3", outline="", tags="bg"
        )

    def _resize_shell(self, event):
        margin_x = 20
        margin_y = 20
        self.canvas.coords(self.shell_window, margin_x, margin_y)
        self.canvas.itemconfig(
            self.shell_window,
            width=max(event.width - (margin_x * 2), 940),
            height=max(event.height - (margin_y * 2), 560),
        )

    def update_totals(self):
        cosmetics_total = 0
        grocery_total = 0
        beverages_total = 0

        for (category, item), qty_var in self.quantity_vars.items():
            try:
                qty = max(0, int(qty_var.get()))
            except (ValueError, tk.TclError):
                qty = 0
            line_total = PRICES[category][item] * qty

            if category == "Cosmetics":
                cosmetics_total += line_total
            elif category == "Grocery":
                grocery_total += line_total
            else:
                beverages_total += line_total

        grand_total = cosmetics_total + grocery_total + beverages_total

        self.total_vars["Cosmetics"].set(f"Rs {cosmetics_total}")
        self.total_vars["Grocery"].set(f"Rs {grocery_total}")
        self.total_vars["Beverages"].set(f"Rs {beverages_total}")
        self.total_vars["Grand"].set(f"Rs {grand_total}")

        return cosmetics_total, grocery_total, beverages_total, grand_total

    def generate_invoice(self):
        name = self.customer_name_var.get().strip() or "Walk-in Customer"
        phone = self.phone_var.get().strip() or "N/A"
        customer_id = self.customer_id_var.get().strip() or "N/A"

        cosmetics_total, grocery_total, beverages_total, grand_total = self.update_totals()

        lines = [
            "ANTEIKU SMART BILLING DESK",
            "--------------------------------",
            f"Customer : {name}",
            f"Phone    : {phone}",
            f"ID       : {customer_id}",
            "--------------------------------",
            "ITEMS",
        ]

        any_items = False
        for category, items in PRICES.items():
            lines.append(f"[{category}]")
            for item, price in items.items():
                qty = max(0, int(self.quantity_vars[(category, item)].get()))
                if qty > 0:
                    any_items = True
                    lines.append(f"{item[:14]:14} x{qty:2}  Rs {price * qty}")

        if not any_items:
            lines.append("No products selected")

        lines.extend(
            [
                "--------------------------------",
                f"Cosmetics : Rs {cosmetics_total}",
                f"Grocery   : Rs {grocery_total}",
                f"Beverages : Rs {beverages_total}",
                f"Grand     : Rs {grand_total}",
                "--------------------------------",
                "Thank you for shopping with us.",
            ]
        )

        self.invoice_box.configure(state="normal")
        self.invoice_box.delete("1.0", "end")
        self.invoice_box.insert("end", "\n".join(lines))
        self.invoice_box.configure(state="disabled")
        self.status_var.set("Invoice generated successfully.")

    def clear_all(self):
        self.customer_name_var.set("")
        self.phone_var.set("")
        self.customer_id_var.set("")

        for qty in self.quantity_vars.values():
            qty.set(0)

        self.update_totals()

        self.invoice_box.configure(state="normal")
        self.invoice_box.delete("1.0", "end")
        self.invoice_box.insert(
            "end",
            "ANTEIKU Billing\n"
            "------------------------------\n"
            "Invoice cleared.\n",
        )
        self.invoice_box.configure(state="disabled")
        self.status_var.set("Reset complete.")


def main():
    root = tk.Tk()
    BillingDeskApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
