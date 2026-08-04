"""
SINTER — Python Projects Hub (Flask Backend)
Serves a premium web UI and launches Python scripts from categorized folders.
"""

from flask import Flask, jsonify, request, render_template, send_from_directory
import subprocess
import os
import sys
import threading

app = Flask(__name__, static_folder="static", template_folder="templates")

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# ── Project metadata (descriptions, icons, tags) ────────────────────────────
PROJECT_META = {
    # ── Games ──────────────────────────────────────────────────────────────
    "casino.py":              {"icon": "🎰", "desc": "Lucky Casino — bet and guess to win 10× your stake.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/casino/index.html"},
    "guess_game.py":          {"icon": "🔮", "desc": "Number guessing game with multiple difficulty modes.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/guess_game/index.html"},
    "quiz_game.py":           {"icon": "🧠", "desc": "Trivia quiz with categories, timer, and scoring.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/quiz_game/index.html"},
    "rock_paper_scissors.py": {"icon": "✊", "desc": "Classic Rock-Paper-Scissors with animated GUI.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/rock_paper_scissors/index.html"},
    "tic_tac_toe.py":         {"icon": "❌", "desc": "Two-player Tic-Tac-Toe on a 3×3 grid.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/tic_tac_toe/index.html"},
    "aim_trainer.py":         {"icon": "🎯", "desc": "Test your reflexes — click targets before time runs out.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/aim_trainer/index.html"},
    "guess_number.py":        {"icon": "🔢", "desc": "Guess the hidden number with hints and lives.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/guess_number/index.html"},
    "mastermind_game.py":     {"icon": "🧩", "desc": "Crack the secret code with logic and deduction.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/mastermind_game/index.html"},
    "minesweeper.py":         {"icon": "💣", "desc": "Classic Minesweeper — sweep the grid without hitting a mine.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/minesweeper/index.html"},
    "slot_machine.py":        {"icon": "🍒", "desc": "Spin the reels and try your luck at the slot machine.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/slot_machine/index.html"},
    "sudoku_solver.py":       {"icon": "🔲", "desc": "Interactive Sudoku board with auto-solve.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/sudoku_solver/index.html"},
    "breakout.py":            {"icon": "🧱", "desc": "Breakout arcade game — smash bricks with a bouncing ball.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/breakout/index.html"},
    "pathfinding_maze.py":    {"icon": "🗺️", "desc": "A* pathfinding visualizer on an interactive grid.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/pathfinding_maze/index.html"},
    # ── Utilities ─────────────────────────────────────────────────────────
    "atm.py":                 {"icon": "🏧", "desc": "ATM simulator with deposits, withdrawals, and PIN auth.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/atm/index.html"},
    "billing.py":             {"icon": "🧾", "desc": "Generate itemised bills with tax calculation.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/billing/index.html"},
    "clock.py":               {"icon": "⏰", "desc": "Live digital clock widget for your desktop.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/clock/index.html"},
    "hotelmenu.py":           {"icon": "🍽️", "desc": "Hotel menu ordering system with cart and receipt.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/hotelmenu/index.html"},
    "lib_manage.py":          {"icon": "📚", "desc": "Library management — add, search, borrow, and return books.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/lib_manage/index.html"},
    "mod_periodic_table.py":  {"icon": "⚗️", "desc": "Interactive periodic table with element details.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/mod_periodic_table/index.html"},
    "phone_book.py":          {"icon": "📞", "desc": "Contact manager — add, search, edit, and delete contacts.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/phone_book/index.html"},
    "rent.py":                {"icon": "🏠", "desc": "Rental billing calculator with customisable rates.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/rent/index.html"},
    "to_do.py":               {"icon": "✅", "desc": "To-do list manager with add/remove/complete actions.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/to_do/index.html"},
    # ── Advanced ──────────────────────────────────────────────────────────
    "particle_fireworks.py":  {"icon": "🎆", "desc": "Click to launch colourful particle fireworks.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/particle_fireworks/index.html"},
    "3d_object_viewer.py":    {"icon": "🧊", "desc": "Rotate and zoom a 3-D wireframe cube with OpenGL.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/3d_object_viewer/index.html"},
    "music_visualizer.py":    {"icon": "🎵", "desc": "Real-time FFT audio visualizer using your microphone.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/music_visualizer/index.html"},
    "text_morph_animation.py":{"icon": "✨", "desc": "Animated text that morphs and fades through words.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/text_morph_animation/index.html"},
    "color_explosion.py":     {"icon": "🌈", "desc": "Mesmerising real-time colour gradient animation.", "tags": ["web"], "type": "web", "web_url": "/static/web_apps/color_explosion/index.html"},
}

CATEGORIES = {
    "games":     {"label": "Games",     "icon": "🎮", "color": "#ff006e"},
    "utilities": {"label": "Utilities", "icon": "🛠️", "color": "#3a86ff"},
    "advanced":  {"label": "Advanced",  "icon": "🚀", "color": "#8338ec"},
}


def scan_projects():
    """Walk category folders and return a list of project dicts."""
    projects = []
    for cat_key, cat_info in CATEGORIES.items():
        cat_dir = os.path.join(PROJECT_ROOT, cat_key)
        if not os.path.isdir(cat_dir):
            continue
        for fname in sorted(os.listdir(cat_dir)):
            if not fname.endswith(".py") or fname.startswith("__"):
                continue
            meta = PROJECT_META.get(fname, {})
            title = os.path.splitext(fname)[0].replace("_", " ").title()
            projects.append({
                "title":    title,
                "filename": fname,
                "path":     f"{cat_key}/{fname}",
                "category": cat_key,
                "catLabel": cat_info["label"],
                "catIcon":  cat_info["icon"],
                "catColor": cat_info["color"],
                "icon":     meta.get("icon", "📄"),
                "desc":     meta.get("desc", "A Python project."),
                "tags":     meta.get("tags", []),
                "type":     meta.get("type", "native"),
                "web_url":  meta.get("web_url", ""),
            })
    return projects


# ── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/projects", methods=["GET"])
def get_projects():
    return jsonify(scan_projects())


@app.route("/api/launch", methods=["POST"])
def launch():
    data = request.get_json(force=True)
    rel_path = data.get("path", "")
    if not rel_path or ".." in rel_path:
        return jsonify({"status": "error", "message": "Invalid path"}), 400

    abs_path = os.path.join(PROJECT_ROOT, rel_path)
    if not os.path.isfile(abs_path):
        return jsonify({"status": "error", "message": "File not found"}), 404

    def _run():
        try:
            python = sys.executable
            subprocess.Popen(
                [python, abs_path],
                cwd=os.path.dirname(abs_path),
                creationflags=subprocess.CREATE_NO_WINDOW,  # no terminal pop-up
            )
        except Exception as exc:
            print(f"[launcher] Error starting {rel_path}: {exc}")

    threading.Thread(target=_run, daemon=True).start()
    return jsonify({"status": "ok", "message": f"Launched {rel_path}"})


if __name__ == "__main__":
    port = 5000
    print("\n  **  SINTER -- Python Projects Hub  **")
    print(f"  ->  Open http://127.0.0.1:{port} in your browser\n")
    app.run(host="127.0.0.1", port=port, debug=True)
