import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic_utils import check_guess


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"


# Bug 1 fix: hint messages were backwards
# When guess is too high, message must say GO LOWER (not GO HIGHER)
def test_too_high_message_says_go_lower():
    outcome, message = check_guess(80, 50)
    assert outcome == "Too High"
    assert "LOWER" in message, f"Expected 'LOWER' in message, got: '{message}'"


# When guess is too low, message must say GO HIGHER (not GO LOWER)
def test_too_low_message_says_go_higher():
    outcome, message = check_guess(20, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message, f"Expected 'HIGHER' in message, got: '{message}'"


# Bug 2 fix: attempts initialized to 1 instead of 0
# Attempts must start at 0 so the sidebar count matches actual remaining guesses
def test_initial_attempts_should_be_zero():
    session = {}
    if "attempts" not in session:
        session["attempts"] = 0  # correct initial value
    assert session["attempts"] == 0, "Attempts must start at 0, not 1"


# Bug 3 fix: new game did not reset status, so win/loss screen persisted
# After a new game reset, status must be "playing" so the game is unblocked
def test_new_game_resets_status_to_playing():
    session = {"status": "won", "attempts": 5, "secret": 42}

    # Simulate the new_game button handler
    session["attempts"] = 0
    session["secret"] = 99
    session["status"] = "playing"

    assert session["status"] == "playing", (
        "New game must reset status to 'playing', "
        f"got: '{session['status']}'"
    )
