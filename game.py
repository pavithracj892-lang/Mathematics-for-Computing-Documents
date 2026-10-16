
import tkinter as tk
from tkinter import messagebox

# Knight & Knave: The Logic Quest
# Python-only desktop game using Tkinter.

BG = "#101820"
PANEL = "#1b2a35"
PANEL2 = "#243744"
GOLD = "#f2c66d"
CREAM = "#f5ead1"
MUTED = "#a9b8c4"
GREEN = "#78c091"
RED = "#ed7b75"
BLUE = "#8fc8ee"

LEVELS = [
    {
        "name": "EASY",
        "color": GREEN,
        "puzzles": [
            {
                "title": "The First Trial",
                "description": "A guard stands before the gate. Examine their statement.",
                "characters": [
                    {"name": "Arin", "statement": "2 + 2 = 4.", "answer": "knight"}
                ],
                "hint": "Check if the mathematical equation is true.",
                "explanation": "2 + 2 = 4 is true. Arin speaks truth, so Arin is a Knight."
            },
            {
                "title": "The Fallen Star",
                "description": "A guard speaks about astronomy.",
                "characters": [
                    {"name": "Borin", "statement": "The Sun is a planet.", "answer": "knave"}
                ],
                "hint": "The Sun is a star.",
                "explanation": "Borin's statement is false, making him a Knave."
            },
            {
                "title": "The Simple Claim",
                "description": "Determine the role of Guard Caren.",
                "characters": [
                    {"name": "Caren", "statement": "I am a Knave.", "answer": "knave"}
                ],
                "hint": "Can a Knight truthfully say 'I am a Knave'?",
                "explanation": (
                    "A Knight cannot truthfully claim to be a Knave. "
                    "This puzzle uses Knave as its intended answer."
                )
            }
        ]
    },
    {
        "name": "MEDIUM",
        "color": "#e8b86d",
        "puzzles": [
            {
                "title": "The Two Guardians",
                "description": "Two guardians make linked declarations.",
                "characters": [
                    {"name": "Arin", "statement": "Borin is a Knave.", "answer": "knave"},
                    {
                        "name": "Borin",
                        "statement": "Arin and I are different types.",
                        "answer": "knight"
                    }
                ],
                "hint": "If Borin is a Knight, check what his statement implies for Arin.",
                "explanation": "Arin is a Knave and Borin is a Knight."
            },
            {
                "title": "The Royal Oath",
                "description": "Two royal guards make a claim about each other.",
                "characters": [
                    {"name": "Celia", "statement": "Daren is a Knight.", "answer": "knight"},
                    {
                        "name": "Daren",
                        "statement": "Celia and I are the same type.",
                        "answer": "knight"
                    }
                ],
                "hint": "Check if both being Knights works logically.",
                "explanation": "Both Celia and Daren are Knights."
            },
            {
                "title": "The Spy Infiltration",
                "description": "A spy may tell either the truth or a lie.",
                "characters": [
                    {"name": "Elara", "statement": "Finn is a Knight.", "answer": "spy"},
                    {"name": "Finn", "statement": "Elara is a Spy.", "answer": "knight"}
                ],
                "hint": "Work backwards from Finn's statement.",
                "explanation": "Finn is a Knight, telling the truth that Elara is a Spy."
            }
        ]
    },
    {
        "name": "HARD",
        "color": "#e58a88",
        "puzzles": [
            {
                "title": "The Triple Conspiracy",
                "description": "Three characters make statements about each other.",
                "characters": [
                    {"name": "Arin", "statement": "Borin is a Knave.", "answer": "knave"},
                    {"name": "Borin", "statement": "Celia is a Knave.", "answer": "knight"},
                    {
                        "name": "Celia",
                        "statement": "Arin and Borin are the same type.",
                        "answer": "knave"
                    }
                ],
                "hint": "Arin and Borin must be opposite types.",
                "explanation": "Arin is a Knave, Borin is a Knight, and Celia is a Knave."
            },
            {
                "title": "The Spy Court",
                "description": "Find the spy among the court members.",
                "characters": [
                    {"name": "Daren", "statement": "I am a Spy.", "answer": "spy"},
                    {"name": "Elara", "statement": "Daren speaks the truth.", "answer": "knave"},
                    {"name": "Finn", "statement": "I am a Knight.", "answer": "knight"}
                ],
                "hint": "Neither a Knight nor a Knave can claim 'I am a Spy'.",
                "explanation": "Daren is the Spy, Elara is a Knave, and Finn is a Knight."
            },
            {
                "title": "The Ultimate Verdict",
                "description": "Three final statements stand between you and victory.",
                "characters": [
                    {"name": "Gideon", "statement": "Hala is a Knight.", "answer": "knave"},
                    {"name": "Hala", "statement": "Ivar is a Knight.", "answer": "knave"},
                    {
                        "name": "Ivar",
                        "statement": "Gideon and Hala are the same type.",
                        "answer": "knave"
                    }
                ],
                "hint": "Test if all three could be Knaves.",
                "explanation": "All three are Knaves."
            }
        ]
    }
]

ROLES = ["Knight", "Knave", "Spy"]

ROLE_COLORS = {
    "Knight": GREEN,
    "Knave": RED,
    "Spy": BLUE
}


class KnightKnaveGame:

    def __init__(self, root):
        self.root = root
        self.root.title("Knight & Knave: The Logic Quest")
        self.root.geometry("1000x720")
        self.root.minsize(760, 600)
        self.root.configure(bg=BG)

        self.player = "Player"
        self.score = 0
        self.current_level = 0
        self.puzzle_index = 0
        self.unlocked = 0
        self.completed = set()
        self.hints_used = 0
        self.answers = {}
        self.sound_on = True
        self.snow = []
        self.confetti = []
        self.canvas = None
        self.screen = None

        self.show_intro()

    # ---------------- GENERAL UI METHODS ----------------

    def clear(self):
        if self.screen:
            self.screen.destroy()

        self.screen = tk.Frame(self.root, bg=BG)
        self.screen.pack(fill="both", expand=True)

    def label(
        self, parent, text, size=12, color=CREAM,
        bold=False, **kwargs
    ):
        background = kwargs.pop("bg", parent.cget("bg"))
        wraplength = kwargs.pop("wraplength", 820)
        justify = kwargs.pop("justify", "center")

        return tk.Label(
            parent,
            text=text,
            bg=background,
            fg=color,
            font=(
                "TkDefaultFont",
                size,
                "bold" if bold else "normal"
            ),
            wraplength=wraplength,
            justify=justify,
            **kwargs
        )

    def button(
        self, parent, text, command,
        bg=PANEL2, fg=CREAM, width=20
    ):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=GOLD,
            activeforeground=BG,
            relief="flat",
            font=("TkDefaultFont", 11, "bold"),
            padx=12,
            pady=9,
            cursor="hand2",
            width=width
        )

    def header(self, parent=None, subtitle=""):
        # Supports header("Subtitle") and header(parent, "Subtitle").
        if isinstance(parent, str):
            subtitle = parent
            parent = self.screen
        elif parent is None:
            parent = self.screen

        self.label(
            parent, "♞  KNIGHT & KNAVE",
            22, GOLD, True
        ).pack(pady=(12, 2))

        self.label(
            parent, "THE LOGIC QUEST",
            11, MUTED, True
        ).pack()

        if subtitle:
            self.label(
                parent, subtitle, 11, MUTED
            ).pack(pady=(5, 8))

    def play_sound(self, kind="ok"):
        if self.sound_on:
            try:
                self.root.bell()
            except tk.TclError:
                pass

    # ---------------- INTRO SCREEN ----------------

    def show_intro(self):
        self.clear()
        self.header(self.screen, "A fantasy puzzle adventure")

        self.label(
            self.screen,
            "Truth has a price. Lies have consequences.",
            20, CREAM, True
        ).pack(pady=(35, 12))

        self.label(
            self.screen,
            "Can you discover who speaks the truth, "
            "who always lies, and who hides in the shadows?",
            12, MUTED
        ).pack(pady=8)

        card = tk.Frame(
            self.screen, bg=PANEL, padx=24, pady=18
        )
        card.pack(pady=20, padx=30)

        self.label(
            card, "♔  KNIGHT", 14, GREEN, True, bg=PANEL
        ).pack(pady=4)

        self.label(
            card, "Always tells the truth.",
            11, CREAM, bg=PANEL
        ).pack()

        self.label(
            card, "♟  KNAVE", 14, RED, True, bg=PANEL
        ).pack(pady=(12, 4))

        self.label(
            card, "Always lies.", 11, CREAM, bg=PANEL
        ).pack()

        self.label(
            card, "✦  SPY", 14, BLUE, True, bg=PANEL
        ).pack(pady=(12, 4))

        self.label(
            card, "May tell the truth or lie.",
            11, CREAM, bg=PANEL
        ).pack()

        self.button(
            self.screen,
            "PLAY GAME  ➜",
            self.show_profile,
            bg=GOLD,
            fg=BG,
            width=24
        ).pack(pady=15)

        self.label(
            self.screen,
            "3 difficulty levels  •  9 puzzles  •  Hints  •  Achievements",
            10, MUTED
        ).pack(pady=6)

        self.animate_snow()

    # ---------------- PLAYER PROFILE ----------------

    def show_profile(self):
        self.clear()
        self.header("Before your quest begins...")

        self.label(
            self.screen,
            "What shall we call you, seeker?",
            17, CREAM, True
        ).pack(pady=(60, 18))

        self.name_entry = tk.Entry(
            self.screen,
            font=("TkDefaultFont", 14),
            justify="center",
            bg=PANEL,
            fg=CREAM,
            insertbackground=CREAM,
            relief="flat"
        )

        self.name_entry.insert(
            0, self.player if self.player != "Player" else ""
        )
        self.name_entry.pack(ipady=10, ipadx=20)

        self.button(
            self.screen,
            "ENTER THE KINGDOM",
            self.save_profile,
            bg=GOLD,
            fg=BG,
            width=24
        ).pack(pady=22)

        self.name_entry.bind(
            "<Return>",
            lambda event: self.save_profile()
        )

    def save_profile(self):
        name = self.name_entry.get().strip()
        self.player = name[:24] if name else "Seeker"

        self.play_sound()
        self.show_map()

    # ---------------- LEVEL MAP ----------------

    def show_map(self):
        self.clear()

        self.header(
            self.screen,
            f"Welcome, {self.player}  •  Score: {self.score}"
        )

        self.label(
            self.screen, "CHOOSE YOUR TRIAL",
            18, CREAM, True
        ).pack(pady=20)

        wrap = tk.Frame(self.screen, bg=BG)
        wrap.pack(pady=4, padx=20, fill="x")

        descriptions = [
            ("I  •  EASY", "Learn the rules", "3 puzzles", GREEN),
            ("II  •  MEDIUM", "Think carefully", "3 puzzles", "#e8b86d"),
            ("III  •  HARD", "Master the logic", "3 puzzles", "#e58a88")
        ]

        for i, (title, desc, count, color) in enumerate(descriptions):
            unlocked = i <= self.unlocked
            card_bg = PANEL if unlocked else "#151e25"

            card = tk.Frame(
                wrap,
                bg=card_bg,
                padx=18,
                pady=20,
                highlightbackground=color if unlocked else "#35414a",
                highlightthickness=2
            )
            card.pack(
                side="left",
                expand=True,
                fill="both",
                padx=8
            )

            self.label(
                card,
                title if unlocked else "🔒  LOCKED",
                14,
                color if unlocked else MUTED,
                True,
                bg=card_bg
            ).pack(pady=6)

            self.label(
                card,
                desc if unlocked else "Complete previous level",
                10,
                CREAM if unlocked else MUTED,
                bg=card_bg
            ).pack(pady=4)

            self.label(
                card, count, 10, MUTED, bg=card_bg
            ).pack(pady=3)

            if unlocked:
                self.button(
                    card,
                    "START",
                    lambda idx=i: self.start_level(idx),
                    bg=color,
                    fg=BG,
                    width=12
                ).pack(pady=(12, 0))

        self.label(
            self.screen,
            f"Rank: {self.get_rank()}  •  "
            f"Completed puzzles: {len(self.completed)}/9",
            12, GOLD, True
        ).pack(pady=24)

        row = tk.Frame(self.screen, bg=BG)
        row.pack()

        self.button(
            row, "ACHIEVEMENTS",
            self.show_achievements, width=18
        ).pack(side="left", padx=6)

        self.button(
            row,
            "SOUND: " + ("ON" if self.sound_on else "OFF"),
            self.toggle_sound,
            width=14
        ).pack(side="left", padx=6)

        self.button(
            row, "HOW TO PLAY",
            self.show_help, width=14
        ).pack(side="left", padx=6)

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.show_map()

    def show_help(self):
        messagebox.showinfo(
            "How to Play",
            "1. Choose an unlocked difficulty level.\n"
            "2. Read each character's statement.\n"
            "3. Choose Knight, Knave, or Spy for each character.\n"
            "4. Press CHECK LOGIC.\n"
            "5. Use HINT if you need help.\n\n"
            "Knight = always tells the truth\n"
            "Knave = always lies\n"
            "Spy = may tell the truth or lie"
        )

    # ---------------- PUZZLE FLOW ----------------

    def start_level(self, idx):
        self.current_level = idx
        self.puzzle_index = 0
        self.load_puzzle()

    def load_puzzle(self):
        self.answers = {}
        self.hints_used = 0
        self.show_puzzle()

    def show_puzzle(self):
        self.clear()

        level = LEVELS[self.current_level]
        puzzle = level["puzzles"][self.puzzle_index]

        self.header(
            self.screen,
            f"{level['name']} TRIAL  •  "
            f"Puzzle {self.puzzle_index + 1}/3  •  "
            f"Score: {self.score}"
        )

        self.label(
            self.screen, puzzle["title"],
            21, GOLD, True
        ).pack(pady=(14, 5))

        self.label(
            self.screen, puzzle["description"],
            11, MUTED
        ).pack(pady=(0, 15))

        self.puzzle_vars = {}

        for char in puzzle["characters"]:
            card = tk.Frame(
                self.screen, bg=PANEL, padx=18, pady=12
            )
            card.pack(fill="x", padx=70, pady=7)

            self.label(
                card, char["name"],
                15, GOLD, True, bg=PANEL
            ).pack(anchor="w")

            self.label(
                card,
                f"“{char['statement']}”",
                12, CREAM,
                bg=PANEL,
                justify="left"
            ).pack(anchor="w", pady=(5, 9))

            var = tk.StringVar(value="Choose a role")
            self.puzzle_vars[char["name"]] = var

            role_row = tk.Frame(card, bg=PANEL)
            role_row.pack(anchor="w")

            for role in ROLES:
                rb = tk.Radiobutton(
                    role_row,
                    text=role,
                    variable=var,
                    value=role,
                    bg=PANEL,
                    fg=ROLE_COLORS[role],
                    selectcolor=BG,
                    activebackground=PANEL,
                    activeforeground=CREAM,
                    font=("TkDefaultFont", 10, "bold")
                )
                rb.pack(side="left", padx=(0, 18))

        bottom = tk.Frame(self.screen, bg=BG)
        bottom.pack(pady=18)

        self.button(
            bottom, "HINT  ?",
            self.show_hint, width=12
        ).pack(side="left", padx=5)

        self.button(
            bottom, "CHECK LOGIC  ✓",
            self.check_answer,
            bg=GOLD,
            fg=BG,
            width=17
        ).pack(side="left", padx=5)

        self.button(
            bottom, "EXIT TO MAP",
            self.show_map, width=13
        ).pack(side="left", padx=5)

        self.label(
            self.screen,
            f"Rank: {self.get_rank()}  •  "
            f"Hints used this puzzle: {self.hints_used}",
            10, MUTED
        ).pack()

    # ---------------- HINTS AND ANSWERS ----------------

    def show_hint(self):
        puzzle = LEVELS[self.current_level]["puzzles"][self.puzzle_index]

        self.hints_used += 1
        self.play_sound()

        messagebox.showinfo(
            "A Hint from the Oracle",
            puzzle["hint"]
        )

    def check_answer(self):
        puzzle = LEVELS[self.current_level]["puzzles"][self.puzzle_index]

        missing = [
            char["name"]
            for char in puzzle["characters"]
            if self.puzzle_vars[char["name"]].get() not in ROLES
        ]

        if missing:
            messagebox.showwarning(
                "Choose a role",
                "Please select a role for: " + ", ".join(missing)
            )
            return

        correct = all(
            self.puzzle_vars[char["name"]].get().lower()
            == char["answer"]
            for char in puzzle["characters"]
        )

        if correct:
            points = max(50, 100 - 20 * self.hints_used)
            self.score += points

            key = (self.current_level, self.puzzle_index)
            self.completed.add(key)

            if (
                self.puzzle_index == 2
                and self.current_level < 2
            ):
                self.unlocked = max(
                    self.unlocked,
                    self.current_level + 1
                )

            self.play_sound("ok")
            self.show_confetti()

            messagebox.showinfo(
                "Correct! ✨",
                f"Excellent reasoning, {self.player}!\n\n"
                f"+{points} points\n\n"
                f"{puzzle['explanation']}"
            )

            self.next_puzzle()

        else:
            self.play_sound("error")

            messagebox.showerror(
                "Not quite...",
                "One or more roles do not match the intended "
                "solution.\n\nTry again or use a hint."
            )

    # ---------------- LEVEL COMPLETION ----------------

    def next_puzzle(self):
        if self.puzzle_index < 2:
            self.puzzle_index += 1
            self.load_puzzle()
            return

        self.clear()
        self.header(self.screen, "Trial completed")

        self.label(
            self.screen, "✦  LEVEL CLEARED  ✦",
            24, GOLD, True
        ).pack(pady=(55, 12))

        self.label(
            self.screen,
            f"Well done, {self.player}!",
            18, CREAM, True
        ).pack(pady=8)

        self.label(
            self.screen,
            f"Your score: {self.score}   •   "
            f"Rank: {self.get_rank()}",
            13, MUTED
        ).pack(pady=8)

        if self.current_level < 2:
            self.label(
                self.screen,
                "A new path has opened on the kingdom map.",
                12, GREEN
            ).pack(pady=10)
        else:
            self.label(
                self.screen,
                "You have completed the entire Logic Quest!",
                13, GREEN, True
            ).pack(pady=10)

        self.button(
            self.screen, "RETURN TO MAP",
            self.show_map,
            bg=GOLD, fg=BG, width=22
        ).pack(pady=20)

        self.button(
            self.screen, "VIEW ACHIEVEMENTS",
            self.show_achievements, width=22
        ).pack()

    # ---------------- RANKING ----------------

    def get_rank(self):
        if self.score >= 1200:
            return "Grandmaster of Logic"
        if self.score >= 700:
            return "Royal Strategist"
        if self.score >= 300:
            return "Truth Seeker"
        if self.score >= 100:
            return "Apprentice"
        return "Newcomer"

    # ---------------- ACHIEVEMENTS ----------------

    def show_achievements(self):
        self.clear()
        self.header("Your deeds will be remembered")

        self.label(
            self.screen, "ACHIEVEMENTS",
            19, GOLD, True
        ).pack(pady=16)

        achievements = [
            (
                "First Steps",
                "Complete your first puzzle",
                len(self.completed) >= 1
            ),
            (
                "Sharp Mind",
                "Complete 3 puzzles",
                len(self.completed) >= 3
            ),
            (
                "Truth Seeker",
                "Complete 6 puzzles",
                len(self.completed) >= 6
            ),
            (
                "Master of Logic",
                "Complete all 9 puzzles",
                len(self.completed) >= 9
            ),
            (
                "No Hints Needed",
                "Earn 100 points on any puzzle",
                self.score >= 100
            ),
            (
                "Royal Strategist",
                "Reach 700 points",
                self.score >= 700
            )
        ]

        for name, desc, earned in achievements:
            row_bg = PANEL if earned else BG

            row = tk.Frame(
                self.screen,
                bg=row_bg,
                padx=14,
                pady=10,
                highlightbackground=GOLD if earned else PANEL2,
                highlightthickness=1
            )
            row.pack(fill="x", padx=120, pady=5)

            self.label(
                row,
                ("🏆 " if earned else "◇ ") + name,
                12,
                GOLD if earned else MUTED,
                True,
                bg=row_bg
            ).pack(anchor="w")

            self.label(
                row,
                desc,
                10,
                CREAM if earned else MUTED,
                bg=row_bg
            ).pack(anchor="w")

        self.button(
            self.screen, "BACK TO MAP",
            self.show_map,
            bg=GOLD, fg=BG, width=20
        ).pack(pady=20)

    # ---------------- EFFECTS ----------------

    def animate_snow(self):
        # Lightweight placeholder for the intro snow effect.
        # Keeps the game compatible with standard Tkinter.
        if not self.screen or not self.screen.winfo_exists():
            return

        self.root.after(900, lambda: None)

    def show_confetti(self):
        # Small native Tkinter victory popup.
        popup = tk.Toplevel(self.root)
        popup.title("Victory!")
        popup.configure(bg=BG)
        popup.geometry("380x150")
        popup.transient(self.root)

        self.label(
            popup, "✦  ✧  ✨  ✧  ✦",
            24, GOLD, True
        ).pack(pady=(18, 6))

        self.label(
            popup, "Logic triumphs!",
            15, GREEN, True
        ).pack()

        self.label(
            popup, "Your quest continues...",
            10, MUTED
        ).pack(pady=6)

        popup.after(900, popup.destroy)


if __name__ == "__main__":
    root = tk.Tk()
    app = KnightKnaveGame(root)
    root.mainloop()
