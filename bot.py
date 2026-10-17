#!/usr/bin/env python3
"""
bot.py — Interactive Python CLI Bot
Author : Harshit Rai
License: MIT
Python : 3.8+

A rule-based terminal assistant that uses regular expressions to match
user intents and respond intelligently — zero external dependencies.
"""

import re
import sys
import random
from datetime import datetime

# ─────────────────────────────────────────────
#  ASCII BANNER
# ─────────────────────────────────────────────

BANNER = r"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ██████╗  ██████╗ ████████╗   ██╗   ██╗ ██╗              ║
║    ██╔══██╗██╔═══██╗╚══██╔══╝   ██║   ██║ ██║              ║
║    ██████╔╝██║   ██║   ██║      ██║   ██║ ██║              ║
║    ██╔══██╗██║   ██║   ██║      ╚██╗ ██╔╝ ╚═╝              ║
║    ██████╔╝╚██████╔╝   ██║       ╚████╔╝  ██╗              ║
║    ╚═════╝  ╚═════╝    ╚═╝        ╚═══╝   ╚═╝              ║
║                                                              ║
║    [ Interactive CLI Bot  ·  Regex Intent Engine ]          ║
║    [ Author: Harshit Rai  ·  Python 3.8+         ]          ║
║                                                              ║
║    Type  'help'  for commands  ·  'exit' to quit            ║
╚══════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────
#  RESPONSE POOLS  (randomised for variety)
# ─────────────────────────────────────────────

GREET_RESPONSES = [
    "Hey there! I'm BotV1 — your terminal companion. How can I help?",
    "Hello, operator! Ready to assist. Type 'help' to see what I can do.",
    "Hi! Good to see you in the terminal. What are we exploring today?",
    "Greetings! BotV1 online and fully operational.",
]

FAREWELL_RESPONSES = [
    "Goodbye! Stay curious and keep hacking (ethically). 👋",
    "Session terminated. See you in the next terminal. 🔐",
    "Bye! Remember — knowledge is the best firewall. ✌️",
    "Logging out… Stay safe out there, operator.",
]

THANKS_RESPONSES = [
    "Happy to help! Anything else?",
    "You're welcome! Type 'help' if you need more commands.",
    "Anytime! That's what I'm here for.",
    "No problem at all. What else can I do for you?",
]

HOW_ARE_YOU_RESPONSES = [
    "I'm running at 100% — no segfaults today! How about you?",
    "All processes nominal. Feeling very Pythonic today! 🐍",
    "Fully operational and regex-powered. Thanks for asking!",
    "Great! No memory leaks detected. 😄 How are you?",
]

UNKNOWN_RESPONSES = [
    "Hmm, I didn't catch that. Try typing 'help' to see available commands.",
    "Unknown command. Type 'help' for a list of things I understand.",
    "I'm not sure what you mean. Try 'help' — I promise it's useful!",
    "Command not recognised. Hint: type 'help' to see my capabilities.",
]

SECURITY_TIPS = [
    "🔐 Tip: Use a password manager like Bitwarden — never reuse passwords.",
    "🛡️  Tip: Enable 2FA (Two-Factor Authentication) on every important account.",
    "🌐 Tip: Always verify HTTPS in the URL before entering sensitive data.",
    "🧅 Tip: Use a VPN on public Wi-Fi to encrypt your traffic.",
    "📧 Tip: Be wary of phishing emails — verify sender domains carefully.",
    "💻 Tip: Keep your OS and software updated — patches fix known exploits.",
    "🔑 Tip: Use long, random passphrases (4+ words) — they're hard to crack.",
    "🧪 Tip: Run penetration tests on your own systems using Kali Linux.",
    "🚫 Tip: Disable unused services and close unneeded open ports.",
    "📁 Tip: Encrypt sensitive files at rest using tools like VeraCrypt.",
]

MOTIVATIONAL_QUOTES = [
    '"The quieter you become, the more you can hear." — Ram Dass',
    '"In the middle of difficulty lies opportunity." — Einstein',
    '"Security is not a product, but a process." — Bruce Schneier',
    '"Hack the planet — ethically." — Anonymous',
    '"Programs must be written for people to read." — SICP',
    '"First, solve the problem. Then, write the code." — John Johnson',
    '"Learning never exhausts the mind." — Leonardo da Vinci',
]

# ─────────────────────────────────────────────
#  INTENT DEFINITIONS
#  Each intent is a dict with:
#    pattern  : compiled regex
#    handler  : callable() -> str response
# ─────────────────────────────────────────────

def _pick(pool: list) -> str:
    """Return a random item from a response pool."""
    return random.choice(pool)


# ── Time & Date ──────────────────────────────

def handle_time(_match) -> str:
    now = datetime.now()
    return f"🕐 Current time: {now.strftime('%H:%M:%S')}  ({now.strftime('%Z') or 'local time'})"


def handle_date(_match) -> str:
    now = datetime.now()
    return f"📅 Today's date: {now.strftime('%A, %d %B %Y')}"


def handle_datetime(_match) -> str:
    now = datetime.now()
    return (
        f"📅 Date : {now.strftime('%A, %d %B %Y')}\n"
        f"🕐 Time : {now.strftime('%H:%M:%S')}"
    )


# ── Basic Calculator ─────────────────────────

def handle_calculator(match) -> str:
    """
    Safely evaluate a basic arithmetic expression.
    Supports: +  -  *  /  **  %  (  )  integers and floats.
    Rejects any non-arithmetic characters for safety.
    """
    raw_expr = match.group("expr").strip()

    # Whitelist: digits, operators, spaces, dots, parentheses only
    if not re.fullmatch(r"[\d\s\+\-\*\/\.\(\)\%\*]+", raw_expr):
        return f"⚠️  Unsafe expression detected. Only use: numbers and + - * / ** % ( )"

    try:
        # Restrict eval to pure math — no builtins
        result = eval(raw_expr, {"__builtins__": {}})  # noqa: S307
        return f"🧮 {raw_expr} = {result}"
    except ZeroDivisionError:
        return "⚠️  Division by zero is undefined."
    except Exception:
        return "⚠️  I couldn't parse that expression. Example: 'calculate 12 * 7 + 3'"


# ── Tech Definitions ─────────────────────────

DEFINITIONS = {
    "ai": (
        "🤖 Artificial Intelligence (AI)\n"
        "   AI is the simulation of human intelligence processes by machines,\n"
        "   especially computer systems. It includes learning, reasoning, and\n"
        "   self-correction. Key branches: Machine Learning, Deep Learning, NLP."
    ),
    "ml": (
        "📊 Machine Learning (ML)\n"
        "   ML is a subset of AI where systems learn from data and improve\n"
        "   automatically without being explicitly programmed. Core types:\n"
        "   Supervised, Unsupervised, and Reinforcement Learning."
    ),
    "dl": (
        "🧠 Deep Learning (DL)\n"
        "   A subset of ML using multi-layered neural networks to model complex\n"
        "   patterns. Powers image recognition, NLP, and voice assistants.\n"
        "   Key frameworks: TensorFlow, PyTorch."
    ),
    "nlp": (
        "💬 Natural Language Processing (NLP)\n"
        "   A field of AI focused on the interaction between computers and\n"
        "   human language. Enables translation, sentiment analysis, chatbots,\n"
        "   and speech recognition."
    ),
    "cybersecurity": (
        "🔐 Cybersecurity\n"
        "   The practice of protecting systems, networks, and programs from\n"
        "   digital attacks. Key domains: Network Security, Application Security,\n"
        "   Ethical Hacking, Incident Response, and Cryptography."
    ),
    "penetration testing": (
        "🛡️  Penetration Testing (Pen Testing)\n"
        "   An authorised simulated cyberattack on a system to evaluate\n"
        "   security. Phases: Reconnaissance → Scanning → Exploitation →\n"
        "   Post-Exploitation → Reporting."
    ),
    "python": (
        "🐍 Python\n"
        "   A high-level, interpreted, general-purpose programming language\n"
        "   known for its clean syntax. Widely used in AI/ML, web dev,\n"
        "   automation, and security scripting. Created by Guido van Rossum."
    ),
    "regex": (
        "🔍 Regular Expressions (Regex)\n"
        "   A sequence of characters forming a search pattern. Used for\n"
        "   string searching, validation, and parsing. Powered by the `re`\n"
        "   module in Python. Example: r'\\d+' matches one or more digits."
    ),
    "git": (
        "🗂️  Git\n"
        "   A distributed version control system for tracking changes in\n"
        "   source code. Created by Linus Torvalds in 2005. Key commands:\n"
        "   git init, add, commit, push, pull, clone, branch."
    ),
    "github": (
        "🐙 GitHub\n"
        "   A cloud-based platform for hosting Git repositories. Enables\n"
        "   collaboration, version control, CI/CD, and open-source contribution.\n"
        "   Owned by Microsoft since 2018."
    ),
    "kali": (
        "💀 Kali Linux\n"
        "   A Debian-based Linux distribution designed for penetration testing\n"
        "   and ethical hacking. Maintained by Offensive Security. Comes\n"
        "   pre-installed with 600+ security tools (Nmap, Metasploit, etc.)."
    ),
    "api": (
        "🔌 API (Application Programming Interface)\n"
        "   A set of rules allowing different software applications to\n"
        "   communicate. REST APIs use HTTP methods (GET, POST, PUT, DELETE)\n"
        "   and are the backbone of modern web services."
    ),
    "ctf": (
        "🚩 CTF (Capture The Flag)\n"
        "   Cybersecurity competitions where participants solve challenges\n"
        "   to find hidden 'flags'. Types: Jeopardy (independent challenges)\n"
        "   and Attack-Defence. Great platforms: TryHackMe, Hack The Box, CTFtime."
    ),
}


def handle_define(match) -> str:
    """Look up a tech definition by keyword."""
    keyword = match.group("term").strip().lower()

    # Direct lookup
    if keyword in DEFINITIONS:
        return DEFINITIONS[keyword]

    # Fuzzy partial match
    for key, definition in DEFINITIONS.items():
        if keyword in key or key in keyword:
            return definition

    available = ", ".join(sorted(DEFINITIONS.keys()))
    return (
        f"📖 I don't have a definition for '{keyword}'.\n"
        f"   Known terms: {available}"
    )


# ── Help Menu ────────────────────────────────

HELP_TEXT = """
╔══════════════════════════════════════════════════════════╗
║                    AVAILABLE COMMANDS                    ║
╠══════════════════════════════════════════════════════════╣
║  GREETINGS                                               ║
║    hello / hi / hey / greetings                          ║
║                                                          ║
║  TIME & DATE                                             ║
║    time             → current time                       ║
║    date             → today's date                       ║
║    datetime / now   → date and time together             ║
║                                                          ║
║  MATH CALCULATOR                                         ║
║    calculate <expr> → e.g. "calculate 15 * 7 + 3"       ║
║    calc <expr>      → shorthand for calculate            ║
║                                                          ║
║  TECH DEFINITIONS                                        ║
║    what is <term>   → e.g. "what is AI"                  ║
║    define <term>    → e.g. "define cybersecurity"        ║
║    explain <term>   → e.g. "explain regex"               ║
║    Terms: ai, ml, dl, nlp, python, regex, git, github,  ║
║           cybersecurity, penetration testing, kali,      ║
║           api, ctf                                       ║
║                                                          ║
║  SECURITY                                                ║
║    security tip     → random cybersecurity tip           ║
║    tip              → same as above                      ║
║                                                          ║
║  EXTRAS                                                  ║
║    how are you      → bot status check                   ║
║    joke             → a nerdy tech joke                  ║
║    quote / inspire  → motivational quote                 ║
║    version          → bot version info                   ║
║    clear            → clear the terminal screen          ║
║                                                          ║
║  EXIT                                                    ║
║    exit / quit / bye / q                                 ║
╚══════════════════════════════════════════════════════════╝
"""

TECH_JOKES = [
    "Why do programmers prefer dark mode?\nBecause light attracts bugs! 🐛",
    "A SQL query walks into a bar, walks up to two tables and asks...\n'Can I join you?' 😄",
    "Why did the developer go broke?\nBecause they used up all their cache. 💸",
    "There are 10 types of people in the world:\nThose who understand binary, and those who don't.",
    "Debugging is like being the detective in a crime movie\nwhere you're also the murderer. 🔍",
    "A hacker walks into a bar.\nThe bartender says: 'We don't serve your type here.'\nThe hacker says: 'That's fine, I'll just use SQL injection.' 💉",
    "Why do Java developers wear glasses?\nBecause they don't C#! 👓",
    "A programmer's partner says: 'Go to the store, get a litre of milk,\nif they have eggs get a dozen.'\nThey come back with 12 litres of milk.",
]


def handle_joke(_match) -> str:
    return f"😂 {random.choice(TECH_JOKES)}"


def handle_quote(_match) -> str:
    return f"💡 {_pick(MOTIVATIONAL_QUOTES)}"


def handle_version(_match) -> str:
    return (
        "📦 BotV1 — Interactive Python CLI Bot\n"
        "   Version    : 1.0.0\n"
        "   Author     : Harshit Rai\n"
        "   License    : MIT\n"
        "   Python     : 3.8+\n"
        "   Dependencies: None (standard library only)"
    )


def handle_clear(_match) -> str:
    """Print ANSI escape code to clear the screen, then re-show banner."""
    print("\033[2J\033[H", end="")
    print(BANNER)
    return "Screen cleared."


# ─────────────────────────────────────────────
#  INTENT TABLE
#  Order matters — more specific patterns first.
# ─────────────────────────────────────────────

INTENTS = [
    # ── Exit ──────────────────────────────────────────────────────────────────
    {
        "name": "exit",
        "pattern": re.compile(
            r"^(exit|quit|bye|goodbye|good\s*bye|q|logout|leave|stop)[\.\!\?]?$"
        ),
        "handler": lambda m: ("EXIT", _pick(FAREWELL_RESPONSES)),
    },
    # ── Help ──────────────────────────────────────────────────────────────────
    {
        "name": "help",
        "pattern": re.compile(r"\b(help|commands|usage|what can you do|options)\b"),
        "handler": lambda m: HELP_TEXT,
    },
    # ── Greeting ──────────────────────────────────────────────────────────────
    {
        "name": "greeting",
        "pattern": re.compile(
            r"^(hello|hi|hey|howdy|greetings|sup|what'?s up|yo|hiya|good\s*(morning|afternoon|evening|day))[\.\!\?]?$"
        ),
        "handler": lambda m: _pick(GREET_RESPONSES),
    },
    # ── Farewell (in-sentence) ─────────────────────────────────────────────
    {
        "name": "farewell",
        "pattern": re.compile(r"\b(see\s+you|take\s+care|farewell|later|cya|ttyl)\b"),
        "handler": lambda m: _pick(FAREWELL_RESPONSES),
    },
    # ── Thanks ────────────────────────────────────────────────────────────────
    {
        "name": "thanks",
        "pattern": re.compile(r"\b(thanks|thank\s+you|thank\s+u|thx|ty|cheers|appreciate)\b"),
        "handler": lambda m: _pick(THANKS_RESPONSES),
    },
    # ── How are you ───────────────────────────────────────────────────────────
    {
        "name": "how_are_you",
        "pattern": re.compile(
            r"\b(how\s+are\s+you|how('?re| are)\s+you|are\s+you\s+ok|you\s+okay|how\s+do\s+you\s+do)\b"
        ),
        "handler": lambda m: _pick(HOW_ARE_YOU_RESPONSES),
    },
    # ── Date + Time combined (must be before individual date/time) ────────────
    {
        "name": "datetime",
        "pattern": re.compile(
            r"\b(date\s+and\s+time|time\s+and\s+date|datetime|current\s+date\s+and\s+time|now)\b"
        ),
        "handler": handle_datetime,
    },
    # ── Time ──────────────────────────────────────────────────────────────────
    {
        "name": "time",
        "pattern": re.compile(
            r"\b(what('?s|\s+is)\s+the\s+time|current\s+time|tell\s+me\s+the\s+time|time\s+now|show\s+time|time)\b"
        ),
        "handler": handle_time,
    },
    # ── Date ──────────────────────────────────────────────────────────────────
    {
        "name": "date",
        "pattern": re.compile(
            r"\b(what('?s|\s+is)\s+(the\s+)?date|today('?s)?\s+date|current\s+date|show\s+date|date\s+today|date)\b"
        ),
        "handler": handle_date,
    },
    # ── Calculator ────────────────────────────────────────────────────────────
    {
        "name": "calculator",
        "pattern": re.compile(
            r"^(calculate|calc|compute|solve|evaluate|what\s+is)\s+(?P<expr>[\d\s\+\-\*\/\.\(\)\%\*]+)$"
        ),
        "handler": handle_calculator,
    },
    # ── Define / Explain / What is ────────────────────────────────────────────
    # Term is limited to 1–4 words so long philosophical sentences don't match.
    {
        "name": "define",
        "pattern": re.compile(
            r"^(what\s+is|define|explain|tell\s+me\s+about|describe|what\s+does)"
            r"\s+(?P<term>[a-z][a-z0-9\s\-]{0,39})$"
        ),
        "handler": handle_define,
    },
    # ── Security tip ──────────────────────────────────────────────────────────
    {
        "name": "security_tip",
        "pattern": re.compile(
            r"\b(security\s+tip|tip|cyber\s+tip|give\s+me\s+a\s+tip|security\s+advice)\b"
        ),
        "handler": lambda m: _pick(SECURITY_TIPS),
    },
    # ── Joke ──────────────────────────────────────────────────────────────────
    {
        "name": "joke",
        "pattern": re.compile(r"\b(joke|funny|make\s+me\s+laugh|tell\s+me\s+a\s+joke|humor|humour)\b"),
        "handler": handle_joke,
    },
    # ── Quote / Motivation ────────────────────────────────────────────────────
    {
        "name": "quote",
        "pattern": re.compile(r"\b(quote|inspire|motivation|motivate|inspire\s+me|wisdom)\b"),
        "handler": handle_quote,
    },
    # ── Version ───────────────────────────────────────────────────────────────
    {
        "name": "version",
        "pattern": re.compile(r"\b(version|about|info|bot\s+info|about\s+bot)\b"),
        "handler": handle_version,
    },
    # ── Clear screen ──────────────────────────────────────────────────────────
    {
        "name": "clear",
        "pattern": re.compile(r"^(clear|cls|clr)$"),
        "handler": handle_clear,
    },
]

# ─────────────────────────────────────────────
#  INPUT NORMALISATION
# ─────────────────────────────────────────────

def normalise(text: str) -> str:
    """
    Clean raw user input:
      1. Strip leading/trailing whitespace.
      2. Lowercase everything.
      3. Collapse multiple internal spaces into one.
      4. Remove trailing punctuation (. ! ?) for easier matching.
    """
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


# ─────────────────────────────────────────────
#  INTENT DISPATCHER
# ─────────────────────────────────────────────

def get_response(raw_input: str) -> tuple[str, str]:
    """
    Match normalised input against the INTENTS table.

    Returns
    -------
    (intent_name, response_text)
        intent_name  : str  — matched intent name, or 'unknown'
        response_text: str  — the bot's reply
    """
    cleaned = normalise(raw_input)

    if not cleaned:
        return ("empty", "Please type something. Try 'help' to see available commands.")

    for intent in INTENTS:
        match = intent["pattern"].search(cleaned)
        if match:
            result = intent["handler"](match)
            # Exit intent returns a tuple ("EXIT", message)
            if isinstance(result, tuple):
                return result
            return (intent["name"], result)

    # Fallback
    return ("unknown", _pick(UNKNOWN_RESPONSES))


# ─────────────────────────────────────────────
#  MAIN INTERACTIVE LOOP
# ─────────────────────────────────────────────

def main() -> None:
    """Entry point — print banner and start the REPL."""
    print(BANNER)

    while True:
        try:
            raw = input("you  ❯  ")
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+D / Ctrl+C gracefully
            print(f"\nbot  ❯  {_pick(FAREWELL_RESPONSES)}\n")
            sys.exit(0)

        intent_name, response = get_response(raw)

        # Handle exit intent
        if intent_name == "EXIT":
            print(f"\nbot  ❯  {response}\n")
            sys.exit(0)

        # Print response (handles multi-line cleanly)
        print(f"\nbot  ❯  {response}\n")


if __name__ == "__main__":
    main()
