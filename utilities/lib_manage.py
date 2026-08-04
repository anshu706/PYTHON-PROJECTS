import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import font as tkFont


class LibraryManager:
    def __init__(self, root):
        self.root = root
        self.root.title("📚 NEO LIBRARY MANAGER")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)

        # Color scheme - Green/Teal library theme
        self.BG_COLOR = "#0d2818"
        self.SIDEBAR_COLOR = "#1a3a2a"
        self.CARD_COLOR = "#1f4d38"
        self.PRIMARY_COLOR = "#00d084"
        self.SECONDARY_COLOR = "#00b8a9"
        self.ACCENT_COLOR = "#f4d35e"
        self.SUCCESS_COLOR = "#06ffa5"
        self.DANGER_COLOR = "#ff4757"
        self.TEXT_COLOR = "#ffffff"
        self.MUTED_TEXT = "#7a9e8f"

        self.root.configure(bg=self.BG_COLOR)

        # Books database
        self.books = [
            {
                "title": "Introduction to C",
                "author": "Dennis Ritchie",
                "pages": 280,
                "price": 350,
                "code": 123,
                "stock": 2,
            },
            {
                "title": "Introduction to Python",
                "author": "Guido Rossum",
                "pages": 320,
                "price": 420,
                "code": 456,
                "stock": 3,
            },
            {
                "title": "Fundamentals of Thermodynamics",
                "author": "Moran",
                "pages": 510,
                "price": 670,
                "code": 153,
                "stock": 13,
            },
        ]

        self.current_view = "catalog"
        self.setup_ui()

    def setup_ui(self):
        """Setup the main UI"""
        # Header
        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR)
        header.pack(fill=tk.X)

        title_font = tkFont.Font(family="Arial", size=24, weight="bold")
        tk.Label(
            header,
            text="📚 NEO LIBRARY MANAGER",
            font=title_font,
            bg=self.PRIMARY_COLOR,
            fg=self.BG_COLOR
        ).pack(pady=12, padx=20, anchor=tk.W)

        # Main container
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.sidebar = tk.Frame(main_frame, bg=self.SIDEBAR_COLOR, width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        self.create_sidebar()

        # Content area
        self.content_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        self.content_frame.pack(
            side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.show_catalog_view()

    def create_sidebar(self):
        """Create sidebar buttons"""
        btn_font = tkFont.Font(family="Arial", size=10, weight="bold")

        # Catalog button
        self.catalog_btn = tk.Button(
            self.sidebar,
            text="📖 VIEW CATALOG",
            command=self.show_catalog_view,
            font=btn_font,
            bg=self.PRIMARY_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            pady=12,
            cursor="hand2"
        )
        self.catalog_btn.pack(fill=tk.X, pady=8)

        # Search button
        self.search_btn = tk.Button(
            self.sidebar,
            text="🔍 SEARCH BY CODE",
            command=self.show_search_view,
            font=btn_font,
            bg=self.SECONDARY_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            pady=12,
            cursor="hand2"
        )
        self.search_btn.pack(fill=tk.X, pady=8)

        # Add book button
        self.add_btn = tk.Button(
            self.sidebar,
            text="➕ ADD BOOK",
            command=self.show_add_view,
            font=btn_font,
            bg=self.SUCCESS_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            pady=12,
            cursor="hand2"
        )
        self.add_btn.pack(fill=tk.X, pady=8)

        # Statistics button
        self.stats_btn = tk.Button(
            self.sidebar,
            text="📊 STATISTICS",
            command=self.show_stats_view,
            font=btn_font,
            bg=self.ACCENT_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            pady=12,
            cursor="hand2"
        )
        self.stats_btn.pack(fill=tk.X, pady=8)

    def clear_content(self):
        """Clear content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def update_sidebar_highlight(self, active_btn):
        """Highlight the active sidebar button"""
        buttons = [self.catalog_btn, self.search_btn,
                   self.add_btn, self.stats_btn]
        for btn in buttons:
            if btn == active_btn:
                btn.config(relief=tk.SUNKEN, bd=2)
            else:
                btn.config(relief=tk.FLAT, bd=0)

    def show_catalog_view(self):
        """Display catalog with table view"""
        self.clear_content()
        self.update_sidebar_highlight(self.catalog_btn)

        # Title
        title_font = tkFont.Font(family="Arial", size=14, weight="bold")
        tk.Label(
            self.content_frame,
            text="📚 LIBRARY CATALOG",
            font=title_font,
            bg=self.BG_COLOR,
            fg=self.PRIMARY_COLOR
        ).pack(pady=15, anchor=tk.W)

        # Create Treeview
        tree_frame = tk.Frame(self.content_frame, bg=self.CARD_COLOR)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Define columns
        columns = ("Code", "Title", "Author", "Pages", "Price", "Stock")

        # Create Treeview with custom style
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview',
                        background=self.CARD_COLOR,
                        foreground=self.TEXT_COLOR,
                        fieldbackground=self.CARD_COLOR,
                        borderwidth=0)
        style.configure('Treeview.Heading',
                        background=self.SECONDARY_COLOR,
                        foreground=self.BG_COLOR,
                        borderwidth=0)
        style.map('Treeview', background=[('selected', self.PRIMARY_COLOR)])

        tree = ttk.Treeview(tree_frame, columns=columns,
                            height=12, show='headings')

        # Define column headings and widths
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140, anchor=tk.CENTER)

        # Add data
        for i, book in enumerate(self.books, 1):
            stock_indicator = f"✓ {book['stock']}" if book['stock'] > 0 else "✗ 0"
            tree.insert("", "end", values=(
                book['code'],
                book['title'],
                book['author'],
                book['pages'],
                f"Rs {book['price']}",
                stock_indicator
            ))

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Summary
        summary_font = tkFont.Font(family="Arial", size=10)
        summary_text = f"Total Books: {len(self.books)} | Total Stock: {sum(b['stock'] for b in self.books)} units"
        tk.Label(
            self.content_frame,
            text=summary_text,
            font=summary_font,
            bg=self.BG_COLOR,
            fg=self.MUTED_TEXT
        ).pack(pady=10, anchor=tk.W)

    def show_search_view(self):
        """Display search by code view"""
        self.clear_content()
        self.update_sidebar_highlight(self.search_btn)

        # Title
        title_font = tkFont.Font(family="Arial", size=14, weight="bold")
        tk.Label(
            self.content_frame,
            text="🔍 SEARCH BY CODE",
            font=title_font,
            bg=self.BG_COLOR,
            fg=self.PRIMARY_COLOR
        ).pack(pady=15, anchor=tk.W)

        # Search input
        input_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        input_frame.pack(fill=tk.X, pady=15)

        tk.Label(
            input_frame,
            text="Enter Book Code:",
            font=tkFont.Font(family="Arial", size=11),
            bg=self.BG_COLOR,
            fg=self.TEXT_COLOR
        ).pack(anchor=tk.W, pady=5)

        search_entry = tk.Entry(
            input_frame,
            font=tkFont.Font(family="Arial", size=12, weight="bold"),
            bg=self.CARD_COLOR,
            fg=self.PRIMARY_COLOR,
            insertbackground=self.PRIMARY_COLOR,
            relief=tk.FLAT,
            borderwidth=0
        )
        search_entry.pack(fill=tk.X, ipady=10)

        # Result display area
        result_frame = tk.Frame(self.content_frame, bg=self.CARD_COLOR)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=15, padx=5, ipady=15)

        result_label = tk.Label(
            result_frame,
            text="",
            font=tkFont.Font(family="Arial", size=10),
            bg=self.CARD_COLOR,
            fg=self.TEXT_COLOR,
            justify=tk.LEFT,
            wraplength=500
        )
        result_label.pack(anchor=tk.NW, padx=15, pady=15)

        def search():
            try:
                code = int(search_entry.get().strip())
                found = None
                for book in self.books:
                    if book['code'] == code:
                        found = book
                        break

                if found:
                    result_text = f"""
📖 BOOK FOUND!

Title:    {found['title']}
Author:   {found['author']}
Pages:    {found['pages']}
Price:    Rs {found['price']}
Code:     {found['code']}
Stock:    {found['stock']} copies available

{'✓ In Stock' if found['stock'] > 0 else '✗ Out of Stock'}
                    """
                    result_label.config(
                        text=result_text, fg=self.SUCCESS_COLOR)
                else:
                    result_label.config(
                        text=f"❌ No book found with code {code}",
                        fg=self.DANGER_COLOR
                    )
            except ValueError:
                result_label.config(
                    text="❌ Please enter a valid code number",
                    fg=self.DANGER_COLOR
                )

        # Search button
        search_btn = tk.Button(
            input_frame,
            text="🔎 FIND BOOK",
            command=search,
            font=tkFont.Font(family="Arial", size=10, weight="bold"),
            bg=self.SECONDARY_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            pady=8,
            cursor="hand2"
        )
        search_btn.pack(fill=tk.X, pady=10)

    def show_add_view(self):
        """Display add book view"""
        self.clear_content()
        self.update_sidebar_highlight(self.add_btn)

        # Title
        title_font = tkFont.Font(family="Arial", size=14, weight="bold")
        tk.Label(
            self.content_frame,
            text="➕ ADD NEW BOOK",
            font=title_font,
            bg=self.BG_COLOR,
            fg=self.PRIMARY_COLOR
        ).pack(pady=15, anchor=tk.W)

        # Form frame
        form_frame = tk.Frame(self.content_frame, bg=self.CARD_COLOR)
        form_frame.pack(fill=tk.X, pady=10, padx=5, ipady=15)

        entries = {}
        label_font = tkFont.Font(family="Arial", size=10, weight="bold")

        fields = ["Title", "Author", "Pages", "Price", "Code", "Stock"]

        for field in fields:
            label_frame = tk.Frame(form_frame, bg=self.CARD_COLOR)
            label_frame.pack(fill=tk.X, pady=8, padx=15)

            tk.Label(
                label_frame,
                text=f"{field}:",
                font=label_font,
                bg=self.CARD_COLOR,
                fg=self.TEXT_COLOR
            ).pack(anchor=tk.W, pady=3)

            entry = tk.Entry(
                label_frame,
                font=tkFont.Font(family="Arial", size=10),
                bg="#0d2818",
                fg=self.PRIMARY_COLOR,
                insertbackground=self.PRIMARY_COLOR,
                relief=tk.FLAT,
                borderwidth=0
            )
            entry.pack(fill=tk.X, ipady=8)
            entries[field.lower()] = entry

        def add_book():
            try:
                new_book = {
                    "title": entries['title'].get().strip(),
                    "author": entries['author'].get().strip(),
                    "pages": int(entries['pages'].get()),
                    "price": int(entries['price'].get()),
                    "code": int(entries['code'].get()),
                    "stock": int(entries['stock'].get()),
                }

                if not new_book['title'] or not new_book['author']:
                    messagebox.showwarning(
                        "Input Error", "Title and Author cannot be empty!")
                    return

                self.books.append(new_book)
                messagebox.showinfo("Success", "✓ Book added successfully!")

                # Clear form
                for entry in entries.values():
                    entry.delete(0, tk.END)

            except ValueError:
                messagebox.showerror(
                    "Input Error", "Please enter valid numbers for Pages, Price, Code, and Stock!")

        # Add button
        add_btn = tk.Button(
            form_frame,
            text="✅ ADD TO LIBRARY",
            command=add_book,
            font=tkFont.Font(family="Arial", size=11, weight="bold"),
            bg=self.SUCCESS_COLOR,
            fg=self.BG_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            pady=10,
            cursor="hand2"
        )
        add_btn.pack(fill=tk.X, padx=15, pady=15)

    def show_stats_view(self):
        """Display statistics view"""
        self.clear_content()
        self.update_sidebar_highlight(self.stats_btn)

        # Title
        title_font = tkFont.Font(family="Arial", size=14, weight="bold")
        tk.Label(
            self.content_frame,
            text="📊 LIBRARY STATISTICS",
            font=title_font,
            bg=self.BG_COLOR,
            fg=self.PRIMARY_COLOR
        ).pack(pady=15, anchor=tk.W)

        # Statistics cards
        stats_frame = tk.Frame(self.content_frame, bg=self.BG_COLOR)
        stats_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Calculate stats
        total_books = len(self.books)
        total_stock = sum(b['stock'] for b in self.books)
        total_value = sum(b['price'] * b['stock'] for b in self.books)
        avg_price = sum(b['price'] for b in self.books) / \
            len(self.books) if self.books else 0

        cards_data = [
            ("📚", "Total Books", str(total_books), self.PRIMARY_COLOR),
            ("📦", "Total Stock", str(total_stock), self.SECONDARY_COLOR),
            ("💰", "Library Value", f"Rs {total_value}", self.ACCENT_COLOR),
            ("💵", "Avg Price", f"Rs {int(avg_price)}", self.SUCCESS_COLOR),
        ]

        for emoji, label, value, color in cards_data:
            card = tk.Frame(stats_frame, bg=color)
            card.pack(fill=tk.X, pady=10, padx=5, ipady=15)

            left_frame = tk.Frame(card, bg=color)
            left_frame.pack(side=tk.LEFT, padx=20)

            tk.Label(
                left_frame,
                text=emoji,
                font=tkFont.Font(family="Arial", size=32),
                bg=color
            ).pack()

            right_frame = tk.Frame(card, bg=color)
            right_frame.pack(side=tk.LEFT, padx=20)

            tk.Label(
                right_frame,
                text=label,
                font=tkFont.Font(family="Arial", size=11, weight="bold"),
                bg=color,
                fg=self.BG_COLOR
            ).pack(anchor=tk.W)

            tk.Label(
                right_frame,
                text=value,
                font=tkFont.Font(family="Arial", size=18, weight="bold"),
                bg=color,
                fg=self.BG_COLOR
            ).pack(anchor=tk.W)

        # Book frequency
        freq_label = tk.Label(
            stats_frame,
            text="📈 BOOKS BY STOCK LEVEL",
            font=tkFont.Font(family="Arial", size=11, weight="bold"),
            bg=self.BG_COLOR,
            fg=self.PRIMARY_COLOR
        )
        freq_label.pack(pady=(20, 10), anchor=tk.W)

        for book in self.books:
            bar_frame = tk.Frame(stats_frame, bg=self.BG_COLOR)
            bar_frame.pack(fill=tk.X, pady=5, padx=5)

            tk.Label(
                bar_frame,
                text=f"{book['title'][:30]:30}",
                font=tkFont.Font(family="Arial", size=9),
                bg=self.BG_COLOR,
                fg=self.TEXT_COLOR,
                width=30
            ).pack(side=tk.LEFT)

            # Bar
            bar = tk.Canvas(
                bar_frame,
                height=20,
                bg=self.CARD_COLOR,
                highlightthickness=0
            )
            bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)

            bar_width = min(book['stock'] * 15, 300)
            bar.create_rectangle(0, 0, bar_width, 20,
                                 fill=self.SECONDARY_COLOR, outline="none")
            bar.create_text(
                bar_width/2, 10, text=str(book['stock']), fill=self.BG_COLOR, font=("Arial", 9, "bold"))


def main():
    root = tk.Tk()
    app = LibraryManager(root)
    root.mainloop()


if __name__ == "__main__":
    main()
