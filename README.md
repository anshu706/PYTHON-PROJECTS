<div align="center">
  <br>
  <h1>✨ SINTER — Python Projects Hub ✨</h1>
  <p><strong>A Premium, Animated Web Hub for Python Enthusiasts</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white" alt="Tailwind" />
    <img src="https://img.shields.io/badge/Alpine.js-8BC0D0?style=for-the-badge&logo=alpine.js&logoColor=white" alt="Alpine.js" />
  </p>
  <br>
</div>

SINTER (v4) is an elegantly designed, centralized hub to browse and launch your entire collection of Python projects. Built with a focus on **visual excellence**, SINTER provides a breathtaking UI filled with glassmorphism, fluid micro-animations, and dynamic particle effects.

We've recently upgraded SINTER to support a fully **web-based architecture**, allowing every single project (Games, Utilities, and Advanced visualizers) to run beautifully right in your browser.

---

## 🚀 Key Features

- **Stunning Aesthetics:** A meticulously crafted dark-mode interface powered by Tailwind CSS, featuring ambient glow effects, responsive 3D tilt cards, and a live particle canvas.
- **Lightning-Fast Navigation:** Instantly filter projects by category (Games, Utilities, Advanced) or use the omni-search bar.
- **Command Palette:** For power users, press `Cmd/Ctrl + K` to open the terminal-style command palette and launch apps via keyboard.
- **Fully Web-Migrated:** Native apps have been beautifully translated to web-native HTML/JS/CSS, ensuring a seamless browser experience without clunky desktop popups.
- **Modular Backend:** A lightweight, robust Flask server that handles configuration, templating, and routing with zero friction.

---

## 🛠️ Tech Stack

### Backend
- **Flask:** Serves the core hub structure and handles dynamic routing.
- **Python 3:** The backbone for logic and data structures.

### Frontend
- **Tailwind CSS:** For rapid, utility-first styling and gorgeous gradients.
- **Alpine.js:** Keeps interactions (like command palettes, filtering, and toasts) reactive and lightweight without the overhead of heavy frameworks.
- **Vanilla JavaScript & HTML5:** For the underlying web apps and 2D/3D canvas components.
- **Lucide Icons:** Clean, consistent iconography.

---

## 💻 Installation & Usage

Getting SINTER running locally takes just a few seconds.

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/sinter-hub.git
   cd sinter-hub
   ```

2. **Activate a virtual environment (Recommended)**
   ```bash
   python -m venv .venv
   
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Hub**
   ```bash
   python app.py
   ```
   > The terminal will output `http://127.0.0.1:5000`. Click or paste this URL into your favorite browser to enter the hub!

---

## 🏗️ Project Architecture

Adding a new project is effortless. The structure is intuitively categorized:

```
PYTHON-PROJECTS/
│
├── app.py                     # Main Flask application & project registry
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html             # The breathtaking SINTER Hub frontend
│
└── static/
    ├── web_apps/              # Fully translated web versions of projects
    │   ├── atm/               # ATM simulator
    │   ├── breakout/          # Breakout arcade game
    │   ├── casino/            # Slot machines & betting
    │   └── ... (and 20+ more!)
```

To register a new app, simply drop your web files into `/static/web_apps/my_new_app/` and add its metadata to the `PROJECT_META` dictionary in `app.py`!

---

<div align="center">
  <i>Crafted with passion for Python and modern web design.</i>
</div>
