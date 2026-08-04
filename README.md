# SINTER — Python Projects Hub

SINTER is a premium, animated web-based launcher for your Python projects. It serves a sleek, modern UI built with Flask, Tailwind CSS, and Alpine.js, allowing you to seamlessly launch native Python GUI applications (like PyGame or Tkinter apps) and web apps directly from your browser.

## Features

- **Beautiful UI:** Premium dark-mode interface with particle canvas, ambient orbs, and glassmorphism.
- **Categorization:** Projects are neatly grouped into Games, Utilities, and Advanced categories.
- **Silent Launch:** Native applications launch directly without popping up annoying terminal windows.
- **Instant Search & Command Palette:** Use `Cmd/Ctrl + K` to bring up the command palette for lightning-fast project launching.

## Installation & Setup

1. **Clone the repository.**
2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the hub:**
   ```bash
   python app.py
   ```
   The terminal will output the local URL (e.g., `http://127.0.0.1:5000`). Open it in your browser to start exploring your projects!

## Technologies Used

- **Backend:** Python, Flask
- **Frontend:** HTML, Tailwind CSS, Vanilla JavaScript, Alpine.js, Lucide Icons
- **Project GUIs:** Tkinter, PyGame, OpenGL, and embedded web views.

## Adding Projects

To add a new project, simply place your Python script into one of the designated category folders (`games/`, `utilities/`, `advanced/`). Then, update the `PROJECT_META` dictionary in `app.py` with its icon, description, and tags so it appears beautifully on the SINTER hub!
