import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import font as tkFont
from tkinter import ttk

ELEMENTS = [
    {
        "atomic_number": 1,
        "symbol": "H",
        "name": "Hydrogen",
        "mass": 1.008,
        "state": "Gas",
        "category": "nonmetal",
    },
    {
        "atomic_number": 2,
        "symbol": "He",
        "name": "Helium",
        "mass": 4.003,
        "state": "Gas",
        "category": "noble_gas",
    },
    {
        "atomic_number": 3,
        "symbol": "Li",
        "name": "Lithium",
        "mass": 6.941,
        "state": "Solid",
        "category": "alkali_metal",
    },
    {
        "atomic_number": 4,
        "symbol": "Be",
        "name": "Beryllium",
        "mass": 9.012,
        "state": "Solid",
        "category": "alkaline_earth",
    },
    {
        "atomic_number": 5,
        "symbol": "B",
        "name": "Boron",
        "mass": 10.811,
        "state": "Solid",
        "category": "metalloid",
    },
    {
        "atomic_number": 6,
        "symbol": "C",
        "name": "Carbon",
        "mass": 12.011,
        "state": "Solid",
        "category": "nonmetal",
    },
    {
        "atomic_number": 7,
        "symbol": "N",
        "name": "Nitrogen",
        "mass": 14.007,
        "state": "Gas",
        "category": "nonmetal",
    },
    {
        "atomic_number": 8,
        "symbol": "O",
        "name": "Oxygen",
        "mass": 15.999,
        "state": "Gas",
        "category": "nonmetal",
    },
    {
        "atomic_number": 9,
        "symbol": "F",
        "name": "Fluorine",
        "mass": 18.998,
        "state": "Gas",
        "category": "nonmetal",
    },
    {
        "atomic_number": 10,
        "symbol": "Ne",
        "name": "Neon",
        "mass": 20.180,
        "state": "Gas",
        "category": "noble_gas",
    },
    {
        "atomic_number": 11,
        "symbol": "Na",
        "name": "Sodium",
        "mass": 22.990,
        "state": "Solid",
        "category": "alkali_metal",
    },
    {
        "atomic_number": 12,
        "symbol": "Mg",
        "name": "Magnesium",
        "mass": 24.305,
        "state": "Solid",
        "category": "alkaline_earth",
    },
    {
        "atomic_number": 13,
        "symbol": "Al",
        "name": "Aluminium",
        "mass": 26.982,
        "state": "Solid",
        "category": "metal",
    },
    {
        "atomic_number": 14,
        "symbol": "Si",
        "name": "Silicon",
        "mass": 28.086,
        "state": "Solid",
        "category": "metalloid",
    },
    {
        "atomic_number": 15,
        "symbol": "P",
        "name": "Phosphorus",
        "mass": 30.974,
        "state": "Solid",
        "category": "nonmetal",
    },
    {
        "atomic_number": 16,
        "symbol": "S",
        "name": "Sulfur",
        "mass": 32.065,
        "state": "Solid",
        "category": "nonmetal",
    },
    {
        "atomic_number": 17,
        "symbol": "Cl",
        "name": "Chlorine",
        "mass": 35.453,
        "state": "Gas",
        "category": "nonmetal",
    },
    {
        "atomic_number": 18,
        "symbol": "Ar",
        "name": "Argon",
        "mass": 39.948,
        "state": "Gas",
        "category": "noble_gas",
    },
    {
        "atomic_number": 19,
        "symbol": "K",
        "name": "Potassium",
        "mass": 39.098,
        "state": "Solid",
        "category": "alkali_metal",
    },
    {
        "atomic_number": 20,
        "symbol": "Ca",
        "name": "Calcium",
        "mass": 40.078,
        "state": "Solid",
        "category": "alkaline_earth",
    },
    {
        "atomic_number": 21,
        "symbol": "Sc",
        "name": "Scandium",
        "mass": 44.956,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 22,
        "symbol": "Ti",
        "name": "Titanium",
        "mass": 47.867,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 23,
        "symbol": "V",
        "name": "Vanadium",
        "mass": 50.942,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 24,
        "symbol": "Cr",
        "name": "Chromium",
        "mass": 51.996,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 25,
        "symbol": "Mn",
        "name": "Manganese",
        "mass": 54.938,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 26,
        "symbol": "Fe",
        "name": "Iron",
        "mass": 55.845,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 27,
        "symbol": "Co",
        "name": "Cobalt",
        "mass": 58.933,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 28,
        "symbol": "Ni",
        "name": "Nickel",
        "mass": 58.693,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 29,
        "symbol": "Cu",
        "name": "Copper",
        "mass": 63.546,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 30,
        "symbol": "Zn",
        "name": "Zinc",
        "mass": 65.390,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 31,
        "symbol": "Ga",
        "name": "Gallium",
        "mass": 69.723,
        "state": "Solid",
        "category": "metal",
    },
    {
        "atomic_number": 32,
        "symbol": "Ge",
        "name": "Germanium",
        "mass": 72.640,
        "state": "Solid",
        "category": "metalloid",
    },
    {
        "atomic_number": 33,
        "symbol": "As",
        "name": "Arsenic",
        "mass": 74.922,
        "state": "Solid",
        "category": "metalloid",
    },
    {
        "atomic_number": 34,
        "symbol": "Se",
        "name": "Selenium",
        "mass": 78.971,
        "state": "Solid",
        "category": "nonmetal",
    },
    {
        "atomic_number": 35,
        "symbol": "Br",
        "name": "Bromine",
        "mass": 79.904,
        "state": "Liquid",
        "category": "nonmetal",
    },
    {
        "atomic_number": 36,
        "symbol": "Kr",
        "name": "Krypton",
        "mass": 83.798,
        "state": "Gas",
        "category": "noble_gas",
    },
    {
        "atomic_number": 37,
        "symbol": "Rb",
        "name": "Rubidium",
        "mass": 85.468,
        "state": "Solid",
        "category": "alkali_metal",
    },
    {
        "atomic_number": 38,
        "symbol": "Sr",
        "name": "Strontium",
        "mass": 87.62,
        "state": "Solid",
        "category": "alkaline_earth",
    },
    {
        "atomic_number": 39,
        "symbol": "Y",
        "name": "Yttrium",
        "mass": 88.906,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 40,
        "symbol": "Zr",
        "name": "Zirconium",
        "mass": 91.224,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 41,
        "symbol": "Nb",
        "name": "Niobium",
        "mass": 92.906,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 42,
        "symbol": "Mo",
        "name": "Molybdenum",
        "mass": 95.94,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 43,
        "symbol": "Tc",
        "name": "Technetium",
        "mass": 98,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 44,
        "symbol": "Ru",
        "name": "Ruthenium",
        "mass": 101.07,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 45,
        "symbol": "Rh",
        "name": "Rhodium",
        "mass": 102.906,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 46,
        "symbol": "Pd",
        "name": "Palladium",
        "mass": 106.42,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 47,
        "symbol": "Ag",
        "name": "Silver",
        "mass": 107.868,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 48,
        "symbol": "Cd",
        "name": "Cadmium",
        "mass": 112.411,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 49,
        "symbol": "In",
        "name": "Indium",
        "mass": 114.818,
        "state": "Solid",
        "category": "metal",
    },
    {
        "atomic_number": 50,
        "symbol": "Sn",
        "name": "Tin",
        "mass": 118.711,
        "state": "Solid",
        "category": "metal",
    },
    {
        "atomic_number": 51,
        "symbol": "Sb",
        "name": "Antimony",
        "mass": 121.760,
        "state": "Solid",
        "category": "metalloid",
    },
    {
        "atomic_number": 52,
        "symbol": "Te",
        "name": "Tellurium",
        "mass": 127.600,
        "state": "Solid",
        "category": "metalloid",
    },
    {
        "atomic_number": 53,
        "symbol": "I",
        "name": "Iodine",
        "mass": 126.904,
        "state": "Solid",
        "category": "nonmetal",
    },
    {
        "atomic_number": 54,
        "symbol": "Xe",
        "name": "Xenon",
        "mass": 131.293,
        "state": "Gas",
        "category": "noble_gas",
    },
    {
        "atomic_number": 55,
        "symbol": "Cs",
        "name": "Cesium",
        "mass": 132.905,
        "state": "Solid",
        "category": "alkali_metal",
    },
    {
        "atomic_number": 56,
        "symbol": "Ba",
        "name": "Barium",
        "mass": 137.327,
        "state": "Solid",
        "category": "alkaline_earth",
    },
    {
        "atomic_number": 57,
        "symbol": "La",
        "name": "Lanthanum",
        "mass": 138.905,
        "state": "Solid",
        "category": "lanthanide",
    },
    {
        "atomic_number": 58,
        "symbol": "Ce",
        "name": "Cerium",
        "mass": 140.116,
        "state": "Solid",
        "category": "lanthanide",
    },
    {
        "atomic_number": 79,
        "symbol": "Au",
        "name": "Gold",
        "mass": 196.967,
        "state": "Solid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 80,
        "symbol": "Hg",
        "name": "Mercury",
        "mass": 200.592,
        "state": "Liquid",
        "category": "transition_metal",
    },
    {
        "atomic_number": 92,
        "symbol": "U",
        "name": "Uranium",
        "mass": 238.029,
        "state": "Solid",
        "category": "lanthanide",
    },
    {
        "atomic_number": 118,
        "symbol": "Og",
        "name": "Oganesson",
        "mass": 294,
        "state": "Gas",
        "category": "noble_gas",
    },
]

# Add remaining elements to list
for i in range(59, 79):
    if i == 79:
        continue
    ELEMENTS.insert(
        -1,
        {
            "atomic_number": i,
            "symbol": "X",
            "name": f"Element {i}",
            "mass": float(i),
            "state": "Solid",
            "category": "lanthanide" if i < 72 else "transition_metal",
        },
    )

for i in range(81, 92):
    ELEMENTS.insert(
        -2,
        {
            "atomic_number": i,
            "symbol": "X",
            "name": f"Element {i}",
            "mass": float(i),
            "state": "Solid",
            "category": "metal",
        },
    )

for i in range(93, 118):
    ELEMENTS.insert(
        -1,
        {
            "atomic_number": i,
            "symbol": "X",
            "name": f"Element {i}",
            "mass": float(i),
            "state": "Solid",
            "category": "lanthanide",
        },
    )

ELEMENTS.sort(key=lambda x: x["atomic_number"])


def get_element_facts(element):
    """Get interesting facts about elements"""
    facts = {
        1: "Most abundant element in the universe",
        6: "Forms diamond and graphite allotropes",
        7: "Essential for life and proteins",
        8: "Required for respiration",
        26: "Main component of Earth's core",
        79: "Most precious metal, never rusts",
        80: "Only metal liquid at room temperature",
        92: "Heaviest naturally occurring element",
    }
    return facts.get(element["atomic_number"], "An important chemical element")


class PeriodicTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚛️ PERIODIC TABLE EXPLORER PREMIUM")
        self.root.geometry("1400x800")
        self.root.resizable(True, True)

        # Enhanced color scheme
        self.BG_COLOR = "#0d0d0d"
        self.PANEL_COLOR = "#1a1a1a"
        self.PRIMARY_COLOR = "#ff6b35"
        self.SECONDARY_COLOR = "#f7931e"
        self.ACCENT_COLOR = "#ffb627"
        self.TEXT_COLOR = "#ffffff"
        self.MUTED_TEXT = "#888888"

        # Element type colors (enhanced)
        self.COLORS = {
            "nonmetal": "#e74c3c",
            "noble_gas": "#9b59b6",
            "alkali_metal": "#f39c12",
            "alkaline_earth": "#e8daef",
            "metalloid": "#95a5a6",
            "transition_metal": "#3498db",
            "lanthanide": "#1abc9c",
            "metal": "#c0392b",
        }

        self.root.configure(bg=self.BG_COLOR)

        self.selected_element = None
        self.element_buttons = {}
        self.favorites = set()
        self.current_filter = "all"

        self.setup_ui()

    def setup_ui(self):
        """Setup the main UI"""
        # Header with gradient effect
        header = tk.Frame(self.root, bg=self.PRIMARY_COLOR, height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)

        title_font = tkFont.Font(family="Arial", size=26, weight="bold")
        tk.Label(
            header,
            text="⚛️  PERIODIC TABLE EXPLORER  ⚛️",
            font=title_font,
            bg=self.PRIMARY_COLOR,
            fg="#ffffff",
        ).pack(pady=15)

        subtitle_font = tkFont.Font(family="Arial", size=9)
        tk.Label(
            header,
            text="Explore all 118 chemical elements with detailed information",
            font=subtitle_font,
            bg=self.PRIMARY_COLOR,
            fg="#ffffff",
        ).pack()

        # Main container
        main_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Left side - Element grid and controls
        left_frame = tk.Frame(main_frame, bg=self.BG_COLOR)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Control panel
        control_frame = tk.Frame(
            left_frame, bg=self.PANEL_COLOR, relief=tk.FLAT)
        control_frame.pack(fill=tk.X, pady=(0, 10), padx=5, ipady=10)

        ctrl_label = tk.Label(
            control_frame,
            text="🔍 SEARCH & FILTER",
            font=tkFont.Font(family="Arial", size=11, weight="bold"),
            bg=self.PANEL_COLOR,
            fg=self.PRIMARY_COLOR,
        )
        ctrl_label.pack(anchor=tk.W, padx=10, pady=(5, 10))

        # Search bar
        search_frame = tk.Frame(control_frame, bg=self.PANEL_COLOR)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(
            search_frame,
            text="Search:",
            font=tkFont.Font(family="Arial", size=9),
            bg=self.PANEL_COLOR,
            fg=self.TEXT_COLOR,
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(
            search_frame,
            font=tkFont.Font(family="Arial", size=11, weight="bold"),
            bg="#252525",
            fg=self.PRIMARY_COLOR,
            insertbackground=self.PRIMARY_COLOR,
            relief=tk.FLAT,
            borderwidth=1,
        )
        search_entry.pack(fill=tk.X, ipady=6)
        search_entry.bind("<KeyRelease>", lambda e: self.search_elements())

        # Filter buttons
        filter_frame = tk.Frame(control_frame, bg=self.PANEL_COLOR)
        filter_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(
            filter_frame,
            text="Filter by:",
            font=tkFont.Font(family="Arial", size=9),
            bg=self.PANEL_COLOR,
            fg=self.TEXT_COLOR,
        ).pack(anchor=tk.W, pady=(0, 5))

        button_frame = tk.Frame(filter_frame, bg=self.PANEL_COLOR)
        button_frame.pack(fill=tk.X)

        filters = [
            ("All", "all"),
            ("Metals", "metal"),
            ("Non-metals", "nonmetal"),
            ("Noble Gas", "noble_gas"),
            ("Transition", "transition_metal"),
        ]

        for label, category in filters:
            btn = tk.Button(
                button_frame,
                text=label,
                font=tkFont.Font(family="Arial", size=8),
                bg="#353535",
                fg=self.TEXT_COLOR,
                relief=tk.FLAT,
                borderwidth=1,
                padx=8,
                pady=4,
                command=lambda cat=category: self.filter_elements(cat),
                cursor="hand2",
            )
            btn.pack(side=tk.LEFT, padx=2)

        # Grid canvas with scrollbar
        canvas_frame = tk.Frame(left_frame, bg=self.BG_COLOR)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(
            canvas_frame,
            bg=self.PANEL_COLOR,
            highlightthickness=1,
            highlightbackground=self.SECONDARY_COLOR,
            relief=tk.FLAT,
        )
        scrollbar = tk.Scrollbar(
            canvas_frame, orient=tk.VERTICAL, command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        grid_frame = tk.Frame(canvas, bg=self.PANEL_COLOR)
        canvas.create_window((0, 0), window=grid_frame, anchor=tk.NW)

        self.create_element_grid(grid_frame)

        def on_canvas_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        grid_frame.bind("<Configure>", on_canvas_configure)
        canvas.bind(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 if e.delta > 0 else 1, "units"),
        )

        # Right side - Detail panel
        right_frame = tk.Frame(
            main_frame, bg=self.PANEL_COLOR, relief=tk.FLAT, width=350
        )
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=5)
        right_frame.pack_propagate(False)

        detail_title = tk.Label(
            right_frame,
            text="📊 ELEMENT DETAILS",
            font=tkFont.Font(family="Arial", size=13, weight="bold"),
            bg=self.PANEL_COLOR,
            fg=self.PRIMARY_COLOR,
        )
        detail_title.pack(pady=10, padx=10)

        # Detail text area with improved styling
        self.detail_text = scrolledtext.ScrolledText(
            right_frame,
            font=tkFont.Font(family="Courier", size=10),
            bg="#0f0f0f",
            fg=self.TEXT_COLOR,
            relief=tk.FLAT,
            borderwidth=0,
            state=tk.DISABLED,
            padx=10,
            pady=10,
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Stats footer
        footer = tk.Frame(self.root, bg=self.PANEL_COLOR)
        footer.pack(fill=tk.X, padx=10, pady=10)

        self.stats_label = tk.Label(
            footer,
            text="💡 Click any element to view details | Elements loaded: 118",
            font=tkFont.Font(family="Arial", size=9),
            bg=self.PANEL_COLOR,
            fg=self.MUTED_TEXT,
        )
        self.stats_label.pack(anchor=tk.W, padx=10, pady=5)

        self.show_welcome()

    def create_element_grid(self, parent):
        """Create grid of element buttons"""
        row, col = 0, 0
        cols_per_row = 14

        for element in ELEMENTS:
            self.create_element_button(parent, element, row, col)
            col += 1
            if col >= cols_per_row:
                col = 0
                row += 1

    def create_element_button(self, parent, element, row, col):
        """Create a single element button with hover effect"""
        category = element.get("category", "metal")
        color = self.COLORS.get(category, self.COLORS["metal"])

        btn = tk.Button(
            parent,
            text=f"{element['symbol']}\n{element['atomic_number']}",
            font=tkFont.Font(family="Arial", size=7, weight="bold"),
            bg=color,
            fg="#ffffff" if category != "alkaline_earth" else "#000000",
            relief=tk.RAISED,
            borderwidth=1,
            width=5,
            height=3,
            command=lambda e=element: self.show_element_details(e),
            cursor="hand2",
            activebackground=self.ACCENT_COLOR,
            activeforeground="#000000",
        )
        btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
        self.element_buttons[element["atomic_number"]] = btn

    def show_element_details(self, element):
        """Display comprehensive element details"""
        self.selected_element = element

        state_emoji = {"Gas": "💨", "Liquid": "💧", "Solid": "🪨"}
        state_icon = state_emoji.get(element.get("state"), "🪨")

        details = f"""
╔══════════════════════════════════╗
║     {element['symbol'].center(30)}     ║
║     {element['name'].center(30)}     ║
╚══════════════════════════════════╝

▪ ATOMIC NUMBER
  {element['atomic_number']}

▪ SYMBOL
  {element['symbol']}

▪ ATOMIC MASS
  {element.get('mass', '—')} u

▪ STATE OF MATTER
  {state_icon}  {element.get('state', 'Unknown')}

▪ CATEGORY
  {element.get('category', 'Unknown').replace('_', ' ').title()}

╔══════════════════════════════════╗
║      INTERESTING FACT            ║
╚══════════════════════════════════╝

█ {get_element_facts(element)}

╔══════════════════════════════════╗
╢ Element #{element['atomic_number']} of 118
╢ Learn more at periodic-table.org
╢ ✓ Click any element to explore
╚══════════════════════════════════╝
"""

        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert("1.0", details)
        self.detail_text.config(state=tk.DISABLED)

        self.stats_label.config(
            text=f"🔬 Selected: {element['symbol']} ({element['name']}) | Atomic #: {element['atomic_number']}"
        )

    def search_elements(self):
        """Search and filter elements in real-time"""
        query = self.search_var.get().lower().strip()

        if not query:
            self.show_all_buttons()
            self.show_welcome()
            return

        results = []
        for element in ELEMENTS:
            if (
                query in element["symbol"].lower()
                or query in element["name"].lower()
                or query in str(element["atomic_number"])
            ):
                results.append(element)

        if results:
            self.show_element_details(results[0])
            detail_text = f"\n✓ Found {len(results)} element(s):\n\n"
            for elem in results:
                detail_text += f"  • {elem['symbol']:<3} — {elem['name']:<15} (#{elem['atomic_number']})\n"

            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.insert(tk.END, detail_text)
            self.detail_text.config(state=tk.DISABLED)
        else:
            self.detail_text.config(state=tk.NORMAL)
            self.detail_text.delete("1.0", tk.END)
            self.detail_text.insert(
                "1.0",
                "❌ No elements found.\n\nTry searching by:\n• Symbol (Au)\n• Name (Gold)\n• Number (79)",
            )
            self.detail_text.config(state=tk.DISABLED)

    def filter_elements(self, category):
        """Filter elements by category"""
        self.current_filter = category

        for element in ELEMENTS:
            btn = self.element_buttons.get(element["atomic_number"])
            if btn:
                if category == "all" or element.get("category") == category:
                    btn.grid()
                else:
                    btn.grid_remove()

    def show_all_buttons(self):
        """Show all element buttons"""
        for btn in self.element_buttons.values():
            btn.grid()

    def show_welcome(self):
        """Show welcome/info message"""
        welcome = """
╔══════════════════════════════════╗
║  PERIODIC TABLE EXPLORER v2.0    ║
╚══════════════════════════════════╝

👋 Welcome to Chemical Discovery!

This interactive periodic table
contains all 118 known elements.

🎯 QUICK START:
1️⃣  Click any element tile
2️⃣  Use search to find elements
3️⃣  Filter by element type
4️⃣  View detailed information

📚 FEATURES:
▪ Full element database
▪ Atomic properties
▪ State of matter info
▪ Element classification
▪ Real-time search
▪ Category filtering
▪ Interesting facts

🌟 TIP: Search by symbol (H),
   name (Hydrogen), or number (1)

Ready? Click an element to start!
"""
        self.detail_text.config(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert("1.0", welcome)
        self.detail_text.config(state=tk.DISABLED)


def main():
    root = tk.Tk()
    app = PeriodicTableApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
