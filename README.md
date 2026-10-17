# 🤖 Interactive Python CLI Bot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Dependencies](https://img.shields.io/badge/Dependencies-None-lightgrey)
![Tests](https://img.shields.io/badge/Tests-Passing-success)

> A lightweight, rule-based terminal assistant powered by regular expression intent matching — runs instantly with any Python 3.8+ installation, zero dependencies required.

---

## 📌 Description

**BotV1** is an interactive CLI bot that parses natural-language terminal input using Python's built-in `re` module, matching user messages to structured intents and returning dynamic responses. It is designed as a clean, beginner-friendly demonstration of regex-driven NLP, modular Python architecture, and standard-library-only development.

---

## ✨ Key Features

- **🔍 Regex Intent Engine** — 15+ intent patterns covering greetings, time/date, definitions, calculator, security tips, jokes, quotes, and more
- **🧮 Safe Calculator** — Evaluates basic arithmetic (`+ - * / ** %`) with a strict character whitelist — no code injection possible
- **📖 Tech Definitions** — Explains AI, ML, DL, NLP, Cybersecurity, Python, Regex, Git, GitHub, CTF, Kali Linux, API, and Penetration Testing
- **🔐 Security Tips** — 10 rotating cybersecurity tips drawn at random on request
- **🎭 Randomised Responses** — Multiple response variants per intent keep interactions fresh
- **🛡️ Graceful Fallback** — Unknown inputs receive helpful suggestions pointing to `help`
- **💀 ASCII Banner** — Cyber-styled startup banner with bot identity
- **🧪 Full Test Suite** — 40+ `unittest` cases covering every intent, edge case, and the calculator's safety guard
- **📦 Zero Dependencies** — Runs with vanilla Python; no `pip install` ever needed

---

## 🚀 How to Run

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/interactive-python-cli-bot.git
cd interactive-python-cli-bot
```

### 2. Verify Python version (3.8+ required)

```bash
python --version
# Python 3.x.x  ← must be 3.8 or higher
```

### 3. Run the bot

```bash
python bot.py
```

That's it — no virtual environment, no `pip install`, no setup.

### 4. Run the test suite

```bash
python test_bot.py
```

Or for verbose output:

```bash
python -m unittest test_bot -v
```

---

## 💻 Terminal Example

```
╔══════════════════════════════════════════════════════════════╗
║   [ Interactive CLI Bot  ·  Regex Intent Engine ]           ║
║   [ Author: Harshit Rai  ·  Python 3.8+         ]           ║
║   Type  'help'  for commands  ·  'exit' to quit             ║
╚══════════════════════════════════════════════════════════════╝

you  ❯  hello
bot  ❯  Hey there! I'm BotV1 — your terminal companion. How can I help?

you  ❯  what is AI
bot  ❯  🤖 Artificial Intelligence (AI)
         AI is the simulation of human intelligence processes by machines...

you  ❯  calculate 15 * 7 + 3
bot  ❯  🧮 15 * 7 + 3 = 108

you  ❯  what is the time
bot  ❯  🕐 Current time: 12:45:33  (local time)

you  ❯  security tip
bot  ❯  🔐 Tip: Use a password manager like Bitwarden — never reuse passwords.

you  ❯  define cybersecurity
bot  ❯  🔐 Cybersecurity
         The practice of protecting systems, networks, and programs from
         digital attacks...

you  ❯  joke
bot  ❯  😂 Debugging is like being the detective in a crime movie
         where you're also the murderer. 🔍

you  ❯  bye
bot  ❯  Goodbye! Stay curious and keep hacking (ethically). 👋
```

---

## 🗂️ Project Structure

```
interactive-python-cli-bot/
│
├── bot.py            # Main script — intent engine, handlers, REPL loop
├── test_bot.py       # Unit tests — 40+ cases using unittest
├── requirements.txt  # No dependencies (standard library only)
└── README.md         # This file
```

### Module Overview

| File | Purpose |
|---|---|
| `bot.py` | Defines the `INTENTS` table, all response handlers, `normalise()` input cleaner, `get_response()` dispatcher, and `main()` REPL |
| `test_bot.py` | Imports `get_response` and `normalise` to verify each intent, edge cases, calculator safety, and the unknown fallback |
| `requirements.txt` | Documents zero-dependency philosophy and lists standard library modules |

---

## 🧠 Architecture

```
User Input (raw string)
        │
        ▼
  normalise(input)          ← lowercase, strip, collapse spaces
        │
        ▼
  INTENTS table scan        ← iterate regex patterns in priority order
        │
   ┌────┴────┐
 match?     no match
   │            │
   ▼            ▼
 handler()   fallback      ← suggests 'help'
   │
   ▼
response string printed to terminal
```

---

## 🔐 Security Note (Calculator)

The calculator uses Python's `eval()` — but it is sandboxed by:
1. A **strict regex whitelist** (`[\d\s\+\-\*\/\.\(\)\%\*]+`) that rejects any non-arithmetic characters before evaluation.
2. Passing `{"__builtins__": {}}` to `eval()` to strip all built-in functions and prevent code injection.

This means inputs like `__import__('os')` or `open('/etc/passwd')` are blocked at the whitelist stage and never reach `eval()`.

---

## 📜 Supported Intent Commands

| Intent | Example Input |
|---|---|
| Greeting | `hello`, `hi`, `hey`, `good morning` |
| Farewell | `exit`, `quit`, `bye`, `goodbye` |
| Time | `time`, `what is the time` |
| Date | `date`, `today's date` |
| Date + Time | `now`, `datetime` |
| Calculator | `calculate 12 * 7 + 3`, `calc 2 ** 10` |
| Define / Explain | `what is AI`, `define python`, `explain regex` |
| Security Tip | `security tip`, `tip` |
| Joke | `joke`, `tell me a joke` |
| Quote | `quote`, `inspire me` |
| How are you | `how are you` |
| Thanks | `thanks`, `thank you`, `thx` |
| Version | `version`, `about` |
| Help | `help`, `commands` |
| Clear screen | `clear`, `cls` |

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

## 👤 Author

**Harshit Rai**
- LinkedIn: [harshit-rai-81b8ab42a](https://www.linkedin.com/in/harshit-rai-81b8ab42a/)
- TryHackMe: [DarkNex](https://tryhackme.com/p/DarkNex)
- Hack The Box: [Profile](https://profile.hackthebox.com/profile/019fbd92-3ca8-73d9-a543-965415155f57)
- GitHub: [github.com/HarshitRai](https://github.com/HarshitRai)

---

*Built with Python · Standard Library · Zero Dependencies · Hack the planet, ethically. 🐍🔐*
