# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

When I first ran the game, it loaded but the behavior felt inconsistent and confusing during gameplay. The hint messages were sometimes backwards. When my guess was too high, the game would tell me to go higher instead of lower. When I adjust the difficulty, the attempts allowed on the left side is always +1 compared to the attempts. The hints didn't work. Once the game is won/lost doesn't let you make a new game, it just keeps showing the win/loss message.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code (Anthropic) as my primary AI tool throughout this project, working in chat mode to identify and fix bugs in the game logic and session state.

**Correct AI suggestion — fixing the swapped hint messages:**
Claude suggested that the hint messages in `check_guess` inside `logic_utils.py` were returning `"Go HIGHER!"` when the guess was too high and `"Go LOWER!"` when the guess was too low — exactly backwards. It identified this by reading the conditional `if guess > secret` and noting the message attached to it was pointing the player in the wrong direction. I verified this by manually tracing the logic: if my guess is 80 and the secret is 50, then `80 > 50` is true, which should mean I need to go lower — but the original code returned `"Go HIGHER!"`. After the fix, I confirmed the messages were correct by reading the updated return values in the file.

**Incorrect AI suggestion — the type conversion in `check_guess`:**
Claude initially suggested that the `try/except TypeError` block in `check_guess` was attempting to handle a mismatch between comparing an int guess to a string secret by converting the guess to a string. However, when I traced through the actual code flow, I realized the bug was different: the code was *intentionally* converting the secret to a string on even-numbered attempts (line `if st.session_state.attempts % 2 == 0: secret = str(...)`), which caused the type mismatch. The `try/except` block was a band-aid fix that masked the real problem instead of preventing it. I verified this by adding debug prints and seeing that the comparison was indeed comparing int to string, and the real fix should have been to *never* convert the secret at all.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed by both reading the corrected code to confirm the logic made sense and running the game manually to observe the changed behavior. For the hint message bug, I verified by checking that guessing too high now showed "Go LOWER!" instead of "Go HIGHER!" — the opposite of what it did before.

I ran the pytest suite in `tests/test_game_logic.py` using `pytest tests/test_game_logic.py -v`. The test `test_too_high_message_says_go_lower` specifically checked that when guess is 80 and secret is 50, the returned message contains `"LOWER"` — this test would have failed on the original broken code and passed after the fix, confirming the bug was resolved. Similarly, `test_new_game_resets_status_to_playing` simulated the session state dict and verified that after a new game reset, `status` equals `"playing"`.

Claude Code helped design all the new tests in this file. It generated tests that checked both the `outcome` and the `message` parts of the `check_guess` return tuple, which was important because the original tests only checked the outcome and would have missed the swapped message bug entirely. It also pointed out that the original three tests were broken — they compared a tuple to a string like `result == "Win"` — and rewrote them to unpack the tuple correctly.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

The secret kept changing because Streamlit reruns the whole script on every button click, so `random.randint()` fired again each time and picked a new number. Streamlit reruns are like a full page reload — every interaction re-executes everything from top to bottom. `st.session_state` is a small memory that survives those reruns, so values stored in it don't get reset. The fix was wrapping the secret in `if "secret" not in st.session_state:` so it only gets generated once on first load.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

Writing tests that check both the outcome and the message — not just whether a function returns the right category, but whether the actual content is correct — is a habit I want to keep. Next time I'd verify AI suggestions against the actual file structure before accepting them, since Claude placed a FIXME in the wrong file after a refactor. This project made me realize AI-generated code can look correct at a glance but still have subtle logic bugs that only show up when you trace through the values manually.
