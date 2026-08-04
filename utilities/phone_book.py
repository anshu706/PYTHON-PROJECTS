import os
import tkinter as tk

# Catppuccin-inspired palette with stronger contrast for a modern dashboard feel.
BG = "#1B1D2B"
BG_ALT = "#232638"
PANEL = "#181A26"
CARD = "#2A2D41"
CARD_SOFT = "#32364D"
FG = "#EEF2FF"
SECONDARY = "#A8B0D6"
MUTED = "#7F88B4"
ACCENT = "#86E1FC"
ACCENT_2 = "#CBA6F7"
BTN_BG = "#7DC4E4"
BTN_HOVER = "#99D6F7"
BTN_FG = "#10131E"
SUCCESS_BG = "#8BD5CA"
ERROR_BG = "#F28FAD"
WARNING_BG = "#F5C2E7"


class ModernPhoneBook(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Aesthetic Phonebook")
        self.geometry("1080x720")
        self.minsize(920, 620)
        self.configure(bg=BG)

        self.contacts = []
        self.filtered_indices = []
        self.current_index = None
        self.entries = {}
        self.search_var = tk.StringVar()
        self.total_var = tk.StringVar(value="0")
        self.visible_var = tk.StringVar(value="0")
        self.selected_var = tk.StringVar(value="No contact selected")
        self.empty_title_var = tk.StringVar(
            value="Your phone book feels lighter now")
        self.empty_body_var = tk.StringVar(
            value="Add a first contact or search through saved people from the sidebar."
        )

        self._setup_ui()
        self._refresh_list()
        self._show_empty_state()

    def _setup_ui(self):
        self.f_hero = ("Segoe UI", 30, "bold")
        self.f_title = ("Segoe UI", 22, "bold")
        self.f_section = ("Segoe UI", 14, "bold")
        self.f_normal = ("Segoe UI", 12)
        self.f_small = ("Segoe UI", 10)
        self.f_bold = ("Segoe UI", 12, "bold")

        self.canvas_bg = tk.Canvas(self, bg=BG, highlightthickness=0, bd=0)
        self.canvas_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.canvas_bg.bind("<Configure>", self._draw_backdrop)

        shell = tk.Frame(self, bg=BG)
        shell.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.sidebar = tk.Frame(shell, bg=PANEL, width=320)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main = tk.Frame(shell, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self._build_sidebar()
        self._build_main()

        self.search_var.trace_add("write", lambda *_: self._refresh_list())

    def _build_sidebar(self):
        hero = tk.Frame(self.sidebar, bg=PANEL, padx=22, pady=24)
        hero.pack(fill="x")

        tk.Label(
            hero,
            text="Contacts",
            font=("Segoe UI", 24, "bold"),
            bg=PANEL,
            fg=ACCENT,
        ).pack(anchor="w")
        tk.Label(
            hero,
            text="Fast search, clean selection, and a more premium workflow.",
            font=self.f_small,
            bg=PANEL,
            fg=SECONDARY,
            wraplength=270,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        stats_row = tk.Frame(hero, bg=PANEL)
        stats_row.pack(fill="x", pady=(20, 0))

        self._stat_chip(stats_row, "Total", self.total_var, ACCENT)
        self._stat_chip(stats_row, "Visible", self.visible_var, ACCENT_2)

        search_card = tk.Frame(self.sidebar, bg=BG_ALT, padx=16, pady=16)
        search_card.pack(fill="x", padx=18, pady=(4, 12))

        tk.Label(
            search_card,
            text="Search",
            font=self.f_small,
            bg=BG_ALT,
            fg=SECONDARY,
        ).pack(anchor="w")

        search_row = tk.Frame(search_card, bg=BG_ALT)
        search_row.pack(fill="x", pady=(10, 0))

        self.search_entry = tk.Entry(
            search_row,
            textvariable=self.search_var,
            font=self.f_normal,
            bg=CARD,
            fg=FG,
            insertbackground=FG,
            bd=0,
            highlightthickness=1,
            highlightbackground=CARD,
            highlightcolor=ACCENT,
        )
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.search_entry.insert(0, "Search by name or phone")
        self.search_entry.config(fg=MUTED)
        self.search_entry.bind("<FocusIn>", lambda e: self._clear_placeholder(
            self.search_entry, "Search by name or phone"))
        self.search_entry.bind("<FocusOut>", lambda e: self._restore_placeholder(
            self.search_entry, "Search by name or phone"))

        clear_btn = tk.Button(
            search_row,
            text="Clear",
            font=self.f_small,
            bg=CARD_SOFT,
            fg=FG,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self._clear_search,
        )
        clear_btn.pack(side="left", padx=(10, 0), ipadx=12, ipady=8)
        self._hover(clear_btn, CARD_SOFT, CARD)

        list_header = tk.Frame(self.sidebar, bg=PANEL, padx=20)
        list_header.pack(fill="x", pady=(10, 0))
        tk.Label(
            list_header,
            text="Saved contacts",
            font=self.f_section,
            bg=PANEL,
            fg=FG,
        ).pack(anchor="w")
        tk.Label(
            list_header,
            text="Select a name to see the profile card.",
            font=self.f_small,
            bg=PANEL,
            fg=MUTED,
        ).pack(anchor="w", pady=(4, 0))

        list_wrap = tk.Frame(self.sidebar, bg=BG_ALT, padx=10, pady=10)
        list_wrap.pack(fill="both", expand=True, padx=18, pady=(12, 14))

        self.listbox = tk.Listbox(
            list_wrap,
            bg=BG_ALT,
            fg=FG,
            selectbackground=CARD_SOFT,
            selectforeground=ACCENT,
            bd=0,
            highlightthickness=0,
            font=self.f_normal,
            activestyle="none",
            relief="flat",
            height=12,
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self._on_select)

        scroll = tk.Scrollbar(list_wrap, command=self.listbox.yview)
        scroll.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scroll.set)

        add_btn = tk.Button(
            self.sidebar,
            text="+ Add Contact",
            font=self.f_bold,
            bg=BTN_BG,
            fg=BTN_FG,
            bd=0,
            activebackground=BTN_HOVER,
            activeforeground=BTN_FG,
            cursor="hand2",
            command=self._show_add,
        )
        add_btn.pack(fill="x", padx=18, pady=(0, 18), ipady=12)
        self._hover(add_btn, BTN_BG, BTN_HOVER)

    def _build_main(self):
        top = tk.Frame(self.main, bg=BG, padx=28, pady=24)
        top.pack(fill="x")

        header_row = tk.Frame(top, bg=BG)
        header_row.pack(fill="x")

        title_block = tk.Frame(header_row, bg=BG)
        title_block.pack(side="left", fill="x", expand=True)

        tk.Label(
            title_block,
            text="Modern Phonebook",
            font=self.f_hero,
            bg=BG,
            fg=FG,
        ).pack(anchor="w")
        tk.Label(
            title_block,
            text="A focused contact manager with smoother hierarchy and a calmer layout.",
            font=self.f_normal,
            bg=BG,
            fg=SECONDARY,
        ).pack(anchor="w", pady=(6, 0))

        self.action_button = tk.Button(
            header_row,
            text="New Contact",
            font=self.f_bold,
            bg=CARD,
            fg=FG,
            bd=0,
            cursor="hand2",
            command=self._show_add,
        )
        self.action_button.pack(side="right", padx=(18, 0), ipadx=18, ipady=10)
        self._hover(self.action_button, CARD, CARD_SOFT)

        self.main_stats = tk.Frame(top, bg=BG)
        self.main_stats.pack(fill="x", pady=(20, 0))

        self._info_card(self.main_stats, "Selected", self.selected_var)
        self._info_card(self.main_stats, "Saved", self.total_var)

        self.content_host = tk.Frame(self.main, bg=BG, padx=28, pady=6)
        self.content_host.pack(fill="both", expand=True)

    def _draw_backdrop(self, event=None):
        self.canvas_bg.delete("all")
        width = max(self.canvas_bg.winfo_width(), 1)
        height = max(self.canvas_bg.winfo_height(), 1)

        self.canvas_bg.create_oval(
            width - 420, -120, width + 120, 420, fill="#20253A", outline="")
        self.canvas_bg.create_oval(-180, height - 260,
                                   260, height + 160, fill="#20233A", outline="")
        self.canvas_bg.create_oval(
            width * 0.58, height * 0.44, width * 0.95, height * 0.92, fill="#1F2338", outline="")
        self.canvas_bg.create_line(0, 0, width, 0, fill="#31364D", width=1)

    def _clear_main(self):
        for widget in self.content_host.winfo_children():
            widget.destroy()

    def _stat_chip(self, parent, label, value_var, accent):
        chip = tk.Frame(parent, bg=CARD, padx=14, pady=10)
        chip.pack(side="left", padx=(0, 10), fill="x", expand=True)
        tk.Label(chip, text=label, font=self.f_small,
                 bg=CARD, fg=SECONDARY).pack(anchor="w")
        tk.Label(chip, textvariable=value_var, font=("Segoe UI", 18,
                 "bold"), bg=CARD, fg=accent).pack(anchor="w", pady=(3, 0))

    def _info_card(self, parent, label, value_var):
        card = tk.Frame(parent, bg=CARD, padx=16, pady=12)
        card.pack(side="left", padx=(0, 12), fill="x", expand=True)
        tk.Label(card, text=label, font=self.f_small,
                 bg=CARD, fg=SECONDARY).pack(anchor="w")
        tk.Label(card, textvariable=value_var, font=self.f_bold, bg=CARD,
                 fg=FG, wraplength=260, justify="left").pack(anchor="w", pady=(4, 0))

    def _make_field(self, parent, row, column, label, placeholder, colspan=1):
        wrap = tk.Frame(parent, bg=CARD)
        wrap.grid(row=row, column=column, columnspan=colspan,
                  sticky="nsew", padx=8, pady=8)

        tk.Label(wrap, text=label, font=self.f_small, bg=CARD,
                 fg=SECONDARY).pack(anchor="w", pady=(0, 6))

        entry = tk.Entry(
            wrap,
            font=self.f_normal,
            bg=BG_ALT,
            fg=FG,
            insertbackground=FG,
            bd=0,
            highlightthickness=1,
            highlightbackground=BG_ALT,
            highlightcolor=ACCENT,
            relief="flat",
        )
        entry.pack(fill="x", ipady=9)
        entry.insert(0, placeholder)
        entry.config(fg=MUTED)
        entry.bind("<FocusIn>", lambda e, ent=entry,
                   p=placeholder: self._clear_placeholder(ent, p))
        entry.bind("<FocusOut>", lambda e, ent=entry,
                   p=placeholder: self._restore_placeholder(ent, p))

        self.entries[label] = (entry, placeholder)

    def _clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=FG)

    def _restore_placeholder(self, entry, placeholder):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=MUTED)

    def _clear_search(self):
        self.search_var.set("")
        if self.search_entry.get() != "Search by name or phone":
            self.search_entry.delete(0, tk.END)
        self.search_entry.insert(0, "Search by name or phone")
        self.search_entry.config(fg=MUTED)
        self._refresh_list()

    def _show_add(self):
        self.listbox.selection_clear(0, tk.END)
        self.current_index = None
        self.selected_var.set("No contact selected")
        self._clear_main()

        card = tk.Frame(self.content_host, bg=CARD, padx=26, pady=24)
        card.place(relx=0.5, rely=0.46, anchor="center", relwidth=0.9)

        tk.Label(card, text="Create Contact", font=self.f_title,
                 bg=CARD, fg=FG).pack(anchor="w")
        tk.Label(
            card,
            text="Build a polished profile in a cleaner form with better spacing and flow.",
            font=self.f_normal,
            bg=CARD,
            fg=SECONDARY,
        ).pack(anchor="w", pady=(6, 18))

        self.entries = {}
        form = tk.Frame(card, bg=CARD)
        form.pack(fill="x")
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        self._make_field(form, 0, 0, "Name", "Enter full name...", colspan=2)
        self._make_field(form, 1, 0, "Phone",
                         "Enter phone number...", colspan=2)
        self._make_field(form, 2, 0, "Age", "Enter age...")
        self._make_field(form, 2, 1, "DOB", "DD-MM-YYYY")
        self._make_field(form, 3, 0, "Address", "Enter address...", colspan=2)

        actions = tk.Frame(card, bg=CARD)
        actions.pack(fill="x", pady=(18, 0))

        btn_save = tk.Button(
            actions,
            text="Save Contact",
            font=self.f_bold,
            bg=BTN_BG,
            fg=BTN_FG,
            bd=0,
            activebackground=BTN_HOVER,
            activeforeground=BTN_FG,
            cursor="hand2",
            command=self._save,
        )
        btn_save.pack(side="left", fill="x", expand=True, ipady=12)
        self._hover(btn_save, BTN_BG, BTN_HOVER)

        btn_reset = tk.Button(
            actions,
            text="Reset",
            font=self.f_bold,
            bg=BG_ALT,
            fg=FG,
            bd=0,
            activebackground=CARD_SOFT,
            activeforeground=FG,
            cursor="hand2",
            command=self._reset_form,
        )
        btn_reset.pack(side="left", padx=(12, 0),
                       fill="x", expand=True, ipady=12)
        self._hover(btn_reset, BG_ALT, CARD_SOFT)

    def _reset_form(self):
        for field, (entry, placeholder) in self.entries.items():
            entry.delete(0, tk.END)
            entry.insert(0, placeholder)
            entry.config(fg=MUTED)

    def _save(self):
        data = {}
        for field, (entry, placeholder) in self.entries.items():
            value = entry.get().strip()
            data[field] = "" if value == placeholder else value

        if not data["Name"] or not data["Phone"]:
            self._toast("Name and Phone are required.", err=True)
            return

        self.contacts.append(data)
        self.current_index = len(self.contacts) - 1
        self._refresh_list()
        self._toast("Contact saved successfully.")
        self._show_details(self.current_index)

    def _refresh_list(self):
        query = self.search_var.get().strip().lower()
        if query == "search by name or phone":
            query = ""

        self.filtered_indices = []
        self.listbox.delete(0, tk.END)

        for idx, contact in enumerate(self.contacts):
            name = contact.get("Name", "")
            phone = contact.get("Phone", "")
            searchable = f"{name} {phone}".lower()
            if query and query not in searchable:
                continue

            self.filtered_indices.append(idx)
            self.listbox.insert(tk.END, f"{name}  ·  {phone}")

        self.total_var.set(str(len(self.contacts)))
        self.visible_var.set(str(len(self.filtered_indices)))

        if not self.contacts:
            self.empty_title_var.set("Your phone book feels lighter now")
            self.empty_body_var.set(
                "Add a first contact or search through saved people from the sidebar.")
            self._show_empty_state()
            return

        if not self.filtered_indices:
            self.empty_title_var.set("No matching contacts")
            self.empty_body_var.set(
                "Try a different search term or clear the filter to see everything again.")
            self._show_empty_state(show_clear=True)
            return

        visible_index = None
        if self.current_index in self.filtered_indices:
            visible_index = self.filtered_indices.index(self.current_index)
        else:
            visible_index = 0
            self.current_index = self.filtered_indices[0]

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(visible_index)
        self.listbox.activate(visible_index)
        self.listbox.see(visible_index)
        self._show_details(self.current_index)

    def _on_select(self, event):
        selection = self.listbox.curselection()
        if not selection:
            return

        visible_index = selection[0]
        if visible_index >= len(self.filtered_indices):
            return

        self.current_index = self.filtered_indices[visible_index]
        self._show_details(self.current_index)

    def _show_details(self, idx):
        if idx is None or idx >= len(self.contacts):
            self._show_empty_state()
            return

        self.current_index = idx
        data = self.contacts[idx]
        self.selected_var.set(data.get("Name") or "Untitled contact")
        self._clear_main()

        card = tk.Frame(self.content_host, bg=CARD, padx=28, pady=26)
        card.pack(fill="both", expand=True)

        top = tk.Frame(card, bg=CARD)
        top.pack(fill="x")

        avatar = tk.Canvas(top, width=108, height=108,
                           bg=CARD, bd=0, highlightthickness=0)
        avatar.pack(side="left")
        avatar.create_oval(8, 8, 100, 100, fill=BG_ALT,
                           outline=ACCENT, width=3)
        initial = data["Name"][0].upper() if data.get("Name") else "?"
        avatar.create_text(54, 54, text=initial, font=(
            "Segoe UI", 40, "bold"), fill=ACCENT)

        header = tk.Frame(top, bg=CARD)
        header.pack(side="left", fill="both", expand=True, padx=(18, 0))

        tk.Label(
            header,
            text=data.get("Name", "Unnamed contact"),
            font=self.f_title,
            bg=CARD,
            fg=FG,
            anchor="w",
        ).pack(anchor="w")
        tk.Label(
            header,
            text=data.get("Phone", ""),
            font=("Segoe UI", 17, "bold"),
            bg=CARD,
            fg=BTN_BG,
            anchor="w",
        ).pack(anchor="w", pady=(6, 0))
        tk.Label(
            header,
            text="Profile snapshot",
            font=self.f_small,
            bg=CARD,
            fg=SECONDARY,
        ).pack(anchor="w", pady=(8, 0))

        details = tk.Frame(card, bg=CARD, pady=18)
        details.pack(fill="both", expand=True)

        detail_card = tk.Frame(details, bg=BG_ALT, padx=20, pady=18)
        detail_card.pack(fill="x")

        self._detail_row(detail_card, "Age", data.get("Age"))
        self._detail_row(detail_card, "DOB", data.get("DOB"))
        self._detail_row(detail_card, "Address", data.get("Address"))

        footer = tk.Frame(card, bg=CARD)
        footer.pack(fill="x", pady=(8, 0))

        btn_new = tk.Button(
            footer,
            text="Add Another",
            font=self.f_bold,
            bg=BG_ALT,
            fg=FG,
            bd=0,
            cursor="hand2",
            command=self._show_add,
        )
        btn_new.pack(side="left", ipady=10, ipadx=16)
        self._hover(btn_new, BG_ALT, CARD_SOFT)

    def _detail_row(self, parent, label, value):
        row = tk.Frame(parent, bg=BG_ALT)
        row.pack(fill="x", pady=8)
        tk.Label(row, text=label, font=self.f_small, fg=SECONDARY,
                 bg=BG_ALT, width=10, anchor="w").pack(side="left")
        tk.Label(row, text=value or "Not provided", font=self.f_bold, fg=FG, bg=BG_ALT,
                 anchor="w", wraplength=620, justify="left").pack(side="left", fill="x", expand=True)

    def _show_empty_state(self, show_clear=False):
        self._clear_main()

        panel = tk.Frame(self.content_host, bg=CARD, padx=30, pady=30)
        panel.place(relx=0.5, rely=0.45, anchor="center", relwidth=0.88)

        canvas = tk.Canvas(panel, width=160, height=160,
                           bg=CARD, bd=0, highlightthickness=0)
        canvas.pack(pady=(6, 20))
        canvas.create_oval(12, 12, 148, 148, fill=BG_ALT,
                           outline=ACCENT_2, width=3)
        canvas.create_oval(40, 40, 120, 120, fill=CARD_SOFT, outline="")
        canvas.create_text(80, 80, text="PB", font=(
            "Segoe UI", 34, "bold"), fill=ACCENT)

        tk.Label(panel, textvariable=self.empty_title_var,
                 font=self.f_title, bg=CARD, fg=FG).pack()
        tk.Label(
            panel,
            textvariable=self.empty_body_var,
            font=self.f_normal,
            bg=CARD,
            fg=SECONDARY,
            justify="center",
            wraplength=680,
        ).pack(pady=(10, 22))

        actions = tk.Frame(panel, bg=CARD)
        actions.pack()

        btn_add = tk.Button(
            actions,
            text="Create Contact",
            font=self.f_bold,
            bg=BTN_BG,
            fg=BTN_FG,
            bd=0,
            cursor="hand2",
            command=self._show_add,
        )
        btn_add.pack(side="left", ipady=12, ipadx=18)
        self._hover(btn_add, BTN_BG, BTN_HOVER)

        if show_clear:
            btn_clear = tk.Button(
                actions,
                text="Clear Search",
                font=self.f_bold,
                bg=BG_ALT,
                fg=FG,
                bd=0,
                cursor="hand2",
                command=self._clear_search,
            )
            btn_clear.pack(side="left", padx=(12, 0), ipady=12, ipadx=18)
            self._hover(btn_clear, BG_ALT, CARD_SOFT)

    def _toast(self, msg, err=False):
        color = ERROR_BG if err else SUCCESS_BG
        toast = tk.Label(
            self.content_host,
            text=msg,
            font=self.f_bold,
            bg=color,
            fg=BTN_FG,
            padx=20,
            pady=10,
        )
        toast.place(relx=0.5, rely=0.03, anchor="n")
        self.after(2500, toast.destroy)

    def _hover(self, widget, bg_norm, bg_hov):
        widget.bind("<Enter>", lambda e: widget.config(bg=bg_hov))
        widget.bind("<Leave>", lambda e: widget.config(bg=bg_norm))


if __name__ == "__main__":
    if os.name == "nt":
        from ctypes import windll

        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    app = ModernPhoneBook()
    app.mainloop()
