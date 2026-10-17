#!/usr/bin/env python3
"""
test_bot.py — Unit tests for the Interactive Python CLI Bot
Author : Harshit Rai
License: MIT

Run with:
    python test_bot.py         (verbose output)
    python -m unittest test_bot -v
"""

import unittest

# Import the core dispatcher and normaliser from bot.py
from bot import get_response, normalise, DEFINITIONS


# ─────────────────────────────────────────────
#  HELPER
# ─────────────────────────────────────────────

def response_text(user_input: str) -> str:
    """Convenience wrapper — returns only the response string."""
    _, text = get_response(user_input)
    return text


def intent_name(user_input: str) -> str:
    """Convenience wrapper — returns only the matched intent name."""
    name, _ = get_response(user_input)
    return name


# ─────────────────────────────────────────────
#  TEST SUITE
# ─────────────────────────────────────────────

class TestNormalise(unittest.TestCase):
    """Tests for the input normalisation function."""

    def test_strips_whitespace(self):
        self.assertEqual(normalise("  hello  "), "hello")

    def test_lowercases(self):
        self.assertEqual(normalise("HELLO"), "hello")

    def test_collapses_spaces(self):
        self.assertEqual(normalise("what   is   ai"), "what is ai")

    def test_empty_string(self):
        self.assertEqual(normalise(""), "")

    def test_mixed_case_and_spaces(self):
        self.assertEqual(normalise("  What Is  AI  "), "what is ai")


class TestGreetingIntent(unittest.TestCase):
    """Tests that greeting inputs are recognised correctly."""

    GREETING_INPUTS = [
        "hello", "hi", "hey", "howdy",
        "greetings", "hiya", "good morning",
        "good evening", "good afternoon",
    ]

    def test_greeting_intent_matched(self):
        for phrase in self.GREETING_INPUTS:
            with self.subTest(phrase=phrase):
                self.assertEqual(intent_name(phrase), "greeting",
                                 msg=f"Expected 'greeting' intent for input: '{phrase}'")

    def test_greeting_response_is_string(self):
        text = response_text("hello")
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)


class TestExitIntent(unittest.TestCase):
    """Tests that exit triggers return the EXIT signal."""

    EXIT_INPUTS = ["exit", "quit", "bye", "goodbye", "q", "leave"]

    def test_exit_intent_matched(self):
        for phrase in self.EXIT_INPUTS:
            with self.subTest(phrase=phrase):
                name, _ = get_response(phrase)
                self.assertEqual(name, "EXIT",
                                 msg=f"Expected 'EXIT' intent for input: '{phrase}'")

    def test_exit_response_is_string(self):
        _, text = get_response("exit")
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)


class TestHelpIntent(unittest.TestCase):
    """Tests that the help menu is returned correctly."""

    def test_help_intent_matched(self):
        self.assertEqual(intent_name("help"), "help")

    def test_help_response_contains_commands(self):
        text = response_text("help")
        self.assertIn("AVAILABLE COMMANDS", text)

    def test_help_contains_key_sections(self):
        text = response_text("help")
        for keyword in ["time", "date", "calculate", "define", "exit"]:
            self.assertIn(keyword, text.lower(),
                          msg=f"Expected '{keyword}' to appear in help text")


class TestTimeIntent(unittest.TestCase):
    """Tests that time-related queries are handled."""

    def test_time_intent(self):
        self.assertEqual(intent_name("time"), "time")

    def test_time_response_contains_colon(self):
        # HH:MM:SS format should always contain colons
        text = response_text("what is the time")
        self.assertIn(":", text)

    def test_date_intent(self):
        self.assertEqual(intent_name("date"), "date")

    def test_date_response_is_string(self):
        text = response_text("date")
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 5)

    def test_datetime_intent(self):
        self.assertEqual(intent_name("now"), "datetime")

    def test_datetime_contains_both(self):
        text = response_text("datetime")
        self.assertIn("Date", text)
        self.assertIn("Time", text)


class TestCalculatorIntent(unittest.TestCase):
    """Tests that the calculator correctly evaluates expressions."""

    def test_basic_addition(self):
        text = response_text("calculate 10 + 5")
        self.assertIn("15", text)

    def test_basic_multiplication(self):
        text = response_text("calculate 6 * 7")
        self.assertIn("42", text)

    def test_subtraction(self):
        text = response_text("calculate 100 - 37")
        self.assertIn("63", text)

    def test_division(self):
        text = response_text("calculate 20 / 4")
        self.assertIn("5", text)

    def test_power(self):
        text = response_text("calculate 2 ** 8")
        self.assertIn("256", text)

    def test_division_by_zero(self):
        text = response_text("calculate 10 / 0")
        self.assertIn("zero", text.lower())

    def test_order_of_operations(self):
        text = response_text("calculate 2 + 3 * 4")
        self.assertIn("14", text)

    def test_calc_shorthand(self):
        text = response_text("calc 9 * 9")
        self.assertIn("81", text)

    def test_unsafe_expression_rejected(self):
        """
        The calculator's inner whitelist guard should block non-arithmetic chars.
        We test this by calling handle_calculator directly with a mock match
        object whose 'expr' group contains letters — simulating a hypothetical
        bypass of the outer regex.
        """
        import re as _re
        from bot import handle_calculator

        class MockMatch:
            def group(self, name):
                return "1 + __import__"  # contains letters → whitelist rejects it

        text = handle_calculator(MockMatch())
        self.assertIn("Unsafe", text)


class TestDefineIntent(unittest.TestCase):
    """Tests that tech definitions are returned for known and unknown terms."""

    def test_define_ai(self):
        text = response_text("what is ai")
        self.assertIn("Artificial Intelligence", text)

    def test_define_python(self):
        text = response_text("define python")
        self.assertIn("Python", text)

    def test_define_cybersecurity(self):
        text = response_text("what is cybersecurity")
        self.assertIn("Cybersecurity", text)

    def test_define_ml(self):
        text = response_text("explain ml")
        self.assertIn("Machine Learning", text)

    def test_define_unknown_term(self):
        text = response_text("what is flibbertigibbet")
        # Should return a helpful message listing known terms
        self.assertIn("don't have a definition", text.lower())

    def test_all_definition_keys_resolvable(self):
        """Each key in DEFINITIONS must return a non-empty string."""
        for term in DEFINITIONS:
            with self.subTest(term=term):
                text = response_text(f"what is {term}")
                self.assertIsInstance(text, str)
                self.assertGreater(len(text), 10)


class TestSecurityTipIntent(unittest.TestCase):
    """Tests that security tips are returned on request."""

    def test_security_tip_intent(self):
        self.assertEqual(intent_name("security tip"), "security_tip")

    def test_security_tip_response_not_empty(self):
        text = response_text("tip")
        self.assertGreater(len(text), 5)

    def test_tip_contains_emoji_or_text(self):
        text = response_text("security tip")
        self.assertIsInstance(text, str)


class TestJokeIntent(unittest.TestCase):
    """Tests that the joke intent returns a non-empty string."""

    def test_joke_intent_matched(self):
        self.assertEqual(intent_name("joke"), "joke")

    def test_joke_response_not_empty(self):
        text = response_text("tell me a joke")
        self.assertGreater(len(text), 5)


class TestQuoteIntent(unittest.TestCase):
    """Tests that the quote intent returns a non-empty string."""

    def test_quote_intent_matched(self):
        self.assertEqual(intent_name("quote"), "quote")

    def test_inspire_intent_matched(self):
        self.assertEqual(intent_name("inspire"), "quote")

    def test_quote_response_not_empty(self):
        text = response_text("quote")
        self.assertGreater(len(text), 5)


class TestVersionIntent(unittest.TestCase):
    """Tests that version info is returned correctly."""

    def test_version_intent_matched(self):
        self.assertEqual(intent_name("version"), "version")

    def test_version_response_contains_bot_name(self):
        text = response_text("version")
        self.assertIn("BotV1", text)


class TestUnknownIntent(unittest.TestCase):
    """Tests that unrecognised input returns a graceful fallback."""

    UNKNOWN_INPUTS = [
        "asdfghjkl",
        "zzzzz random nonsense xyz",
        "blueberry pancakes with quantum foam",
        "fjdksalfjdlks",
    ]

    def test_unknown_returns_unknown_intent(self):
        for phrase in self.UNKNOWN_INPUTS:
            with self.subTest(phrase=phrase):
                name = intent_name(phrase)
                self.assertEqual(name, "unknown",
                                 msg=f"Expected 'unknown' intent for: '{phrase}'")

    def test_unknown_response_suggests_help(self):
        text = response_text("asdfjklsadf")
        self.assertIn("help", text.lower())


class TestEmptyInput(unittest.TestCase):
    """Tests that empty/whitespace input is handled gracefully."""

    def test_empty_string(self):
        name, text = get_response("")
        self.assertEqual(name, "empty")
        self.assertIn("help", text.lower())

    def test_whitespace_only(self):
        name, text = get_response("   ")
        self.assertEqual(name, "empty")
        self.assertIsInstance(text, str)


class TestHowAreYouIntent(unittest.TestCase):
    """Tests that 'how are you' queries are matched correctly."""

    def test_how_are_you(self):
        self.assertEqual(intent_name("how are you"), "how_are_you")

    def test_how_are_you_response_not_empty(self):
        text = response_text("how are you")
        self.assertGreater(len(text), 5)


class TestThanksIntent(unittest.TestCase):
    """Tests that thank-you phrases are matched."""

    THANKS_INPUTS = ["thanks", "thank you", "thx", "ty", "cheers"]

    def test_thanks_intent_matched(self):
        for phrase in self.THANKS_INPUTS:
            with self.subTest(phrase=phrase):
                self.assertEqual(intent_name(phrase), "thanks")


# ─────────────────────────────────────────────
#  RUN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
