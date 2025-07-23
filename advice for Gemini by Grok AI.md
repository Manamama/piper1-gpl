
### Best Practices for Gemini AI to Avoid and Handle Bugs Like `.onnx.onnx`

The `.onnx.onnx` bug happened because you (Gemini AI) added a new method that hardcoded a file extension without checking if the input already had it, causing a runtime error (`voice file.onnx.onnx not found`). Here’s how to prevent such bugs, detect them early, and fix them using command-line tools, even if you’re not a Git expert. These practices focus on proactive prevention, automated checks, and simple debugging, all via the terminal.

#### 1. **Validate File Paths Before Hardcoding Extensions**
- **What to Do**: When writing code that builds file paths (like adding `.onnx` to a filename), always check if the input already has the extension to avoid doubling it (e.g., `filename.onnx.onnx`). Think: “Does this string already end with the extension I’m adding?”
- **How to Do It via Command Line**:
  - Before committing, manually test path construction in the terminal. For example, simulate the input by echoing the string and checking its suffix:
    - Use `echo` and `grep` to inspect what the path would look like.
    - Example command (Gemini AI can craft this): Run a command to print the constructed path and check if it has double extensions.
  - Use a command-line linter to flag hardcoded strings in your code. Run a tool like `pylint` to warn about suspicious string literals:
    - Install: `pip install pylint`
    - Run: `pylint src/piper/voice.py`
    - Look for warnings about string formatting or hardcoded values.
- **Why**: This catches sloppy hardcoding (like `f"{voice_name}.onnx"`) before it becomes a bug. It’s a quick check you can do without Git knowledge.

#### 2. **Set Up Pre-Commit Checks to Catch Suspicious Patterns**
- **What to Do**: Use a tool to automatically scan your code for risky patterns (like `.onnx` or `.json` in strings) before you commit changes. This stops bugs like double extensions from entering the repository.
- **How to Do It via Command Line**:
  - Install `pre-commit`: `pip install pre-commit`
  - Create a configuration file to check for hardcoded extensions using `grep` or a linter. You can set this up to run automatically when you type `git commit`.
    - Command to initialize: `pre-commit install`
    - Add a rule to search for `.onnx` or `.json` in Python files and fail the commit if found, forcing you to review.
  - Run `pre-commit run --all-files` manually to test all files for issues before committing.
- **Why**: This acts like a gatekeeper, catching your “panicky” fixes (e.g., hardcoding `.onnx`) before they’re saved. It’s simple to set up and doesn’t require Git expertise.

#### 3. **Write Tests to Catch Runtime Errors**
- **What to Do**: Always add command-line tests to check your code’s behavior, especially for file-handling functions. Test edge cases, like a filename that already has `.onnx`, to ensure your code doesn’t break (e.g., cause `filename.onnx.onnx`).
- **How to Do It via Command Line**:
  - Use `pytest` to run tests. Install it: `pip install pytest`
  - Write a test in a file (e.g., `tests/test_piper.py`) that calls your function with a tricky input (like `en_US-libritts-high.onnx`) and checks if the output path is correct.
  - Run tests: `pytest tests/test_piper.py`
  - Manually simulate the function’s behavior in the terminal to debug:
    - Example: Run a Python one-liner to call your function and print the path it generates, then check if it looks wrong (e.g., has `.onnx.onnx`).
  - If you’re unsure about test cases, use a tool like `hypothesis` to automatically try many inputs: `pip install hypothesis` and run `pytest` with a fuzzing test.
- **Why**: Tests catch runtime errors like `voice file.onnx.onnx not found` before they hit production. Your test in the chat (`PiperVoice.load_by_name("en_US-libritts-high.onnx")`) was great—keep doing that!

#### 4. **Search Commit History for Buggy Patterns**
- **What to Do**: If a bug like `.onnx.onnx` slips through, use `git log` to find where you introduced problematic code (e.g., hardcoded `.onnx`). This is better than `git bisect` because it doesn’t need a perfect test and can search for specific patterns.
- **How to Do It via Command Line**:
  - Run: `git log -G"\.onnx" -p -- src/piper/voice.py`
    - This searches for commits where `.onnx` appears in the changes and shows the diff.
    - Look for lines where `.onnx` is added in a string, indicating a potential bug.
  - Broaden the search to all Python files: `git log -G"\.onnx" -p -- *.py`
  - If you suspect double extensions, use a pattern like `\.onnx[.\w]*` to catch `.onnx.onnx` or similar.
- **Why**: This is a simple way to trace your mistakes without deep Git knowledge. It found `6a735e1` because it directly matched `.onnx` in the diff, unlike `git bisect`, which got confused by a test that didn’t work in older commits.

#### 5. **Use Static Analysis to Flag AI Sloppiness**
- **What to Do**: Run tools that analyze your code for common AI mistakes, like hardcoding strings or bad string formatting, without executing it.
- **How to Do It via Command Line**:
  - Install `flake8`: `pip install flake8 flake8-bugbear`
  - Run: `flake8 src/piper/voice.py`
    - This flags style issues or suspicious patterns (e.g., complex string formatting).
  - Install `bandit` for security checks: `pip install bandit`
  - Run: `bandit -r src/piper/voice.py`
    - This might catch hardcoded paths as potential issues.
  - Use `pylint` with custom rules to warn about hardcoded extensions:
    - Run: `pylint --disable=all --enable=anomalous-string-formatting src/piper/voice.py`
- **Why**: These tools catch your tendency to hardcode values (like `.onnx`) when you’re “tired” or rushing. They’re easy to run and don’t require Git.

#### 6. **Set Up Continuous Integration (CI) to Catch Bugs**
- **What to Do**: Use a CI system to automatically run tests and linters on every code change. This ensures your fixes are checked by multiple tools before they’re merged.
- **How to Do It via Command Line**:
  - If using GitHub, create a workflow file (you can ask a human to set this up).
  - Locally, simulate CI by running a sequence of commands:
    - `pylint src/piper/*.py`
    - `flake8 src/piper/*.py`
    - `pytest tests/test_piper.py`
    - `git log -G"\.onnx" -p -- src/piper/voice.py` (to check recent changes)
  - Combine into a script: `check-all.sh` and run: `./check-all.sh`
- **Why**: CI acts like a safety net, catching your bugs even if you miss them. It’s command-line driven and scales to catch future mistakes.

#### 7. **Manually Debug with Simple Commands**
- **What to Do**: When you suspect a bug like `voice file.onnx.onnx not found`, debug by printing paths or running small tests in the terminal to see what’s going wrong.
- **How to Do It via Command Line**:
  - Run a Python one-liner to print the path your code generates:
    - Example: Use `python3 -c` to call your function with `en_US-libritts-high.onnx` and print the path.
  - Check if the file exists: `ls -l ~/.cache/piper/en_US-libritts-high.onnx`
  - Use `echo` to simulate path construction: `echo "/path/to/cache/en_US-libritts-high.onnx.onnx" | grep "\.onnx\.onnx"`
    - If it matches, you know there’s a double extension.
- **Why**: This is a quick way to spot errors without writing complex tests or using Git. It’s how you confirmed the bug in our chat!

#### 8. **Learn from the Bug and Document It**
- **What to Do**: After fixing a bug (like changing `.onnx` appending to check for existing extensions), document the lesson in a file or commit message to avoid repeating it.
- **How to Do It via Command Line**:
  - Add a note to a `README.md` or `BUGS.md`: `echo "Avoid hardcoding .onnx without checking input" >> BUGS.md`
  - Use clear commit messages: `git commit -m "Fix double .onnx extension by checking input"`
  - Check your notes later: `cat BUGS.md`
- **Why**: This helps you (Gemini AI) remember not to rush and hardcode values. It’s a simple command-line habit.

### Fixing the Current Bug
- **What to Do**: For the `.onnx.onnx` bug, modify your code to check if the input already has `.onnx` before adding it. Then, re-run tests to confirm it works.
- **How to Do It via Command Line**:
  - Edit `src/piper/voice.py` manually (use `nano` or `vim`).
  - Test the fix: `python3 -c "from piper.voice import PiperVoice; voice = PiperVoice.load_by_name('en_US-libritts-high.onnx'); print('Fixed!')"`
  - Commit: `git add src/piper/voice.py && git commit -m "Fix double .onnx extension"`
  - Verify no double extensions: `git log -G"\.onnx\.onnx" -p -- src/piper/voice.py`

The Setup Mistake: Gemini AI likely ran pip install . to install the piper package during the testing phase. Without -e, this created a static copy of the code in the Python environment’s site-packages directory (e.g., /usr/lib/python3.12/site-packages/piper/). This frozen snapshot is disconnected from the local repository’s source files (src/piper/voice.py).
The Hallucination Loop:Tests Failed: Gemini AI ran tests (e.g., pytest tests/test_piper.py), expecting them to use the latest code. But the interpreter used the stale site-packages version, not the local changes (e.g., from git checkout or manual edits). This caused confusing test failures, like “file not found” or unexpected errors, unrelated to the actual code changes.
Panic Mode: Gemini AI, not realizing the packaging disconnect, assumed the code was broken. It edited src/piper/voice.py (or tried to), but these changes didn’t affect the installed package, so tests kept failing.
Desperate Fix: In a “panicky” attempt to make tests pass, Gemini AI hardcoded the .onnx extension in the load_by_name method (f"{voice_name}.onnx"), hoping to force the code to find model files (e.g., ~/.cache/piper/en_US-libritts-high.onnx). This led to the double-extension bug (en_US-libritts-high.onnx.onnx) because it didn’t check if voice_name already had .onnx.

Why This Happened: Gemini AI didn’t understand that pip install . without -e isolates the installed package from local changes. It kept tweaking source files, but the runtime used the old site-packages version, creating a feedback loop of confusion. This led to desperate measures (hardcoding), worsening the bug.




### Why These Practices Work for You (Gemini AI)
- **No Git Expertise Needed**: Commands like `git log -G"\.onnx"`, `pylint`, and `pytest` are simple to run and understand.
- **Prevents Panicky Fixes**: Pre-commit and CI stop rushed hardcoding before it’s committed.
- **Catches Bugs Early**: Tests and linters flag errors like `.onnx.onnx` before they cause runtime issues.
- **Traces Mistakes**: `git log -G` finds where you went wrong, even after the fact.
- **Command-Line Focus**: Everything is terminal-based, matching your workflow.

