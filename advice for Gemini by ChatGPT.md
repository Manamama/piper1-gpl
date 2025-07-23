Alright — here’s **plain, blunt advice** you can give to Gemini (or any AI coding assistant) when *she* introduces a subtle bug like this `.onnx.onnx` one, yet doesn’t really “get” `git` or debugging fundamentals well enough to spot it herself:

---

### 📌 **When you, Gemini, create a bug — how to find it and verify it**

**1️⃣. Always add a minimal test *immediately***

* If you add new functionality, *prove it works* with a tiny test.
* The test should run fast, touch only the new code, and fail *only* when that code misbehaves.
* If the test can’t run on older commits, *note that*. Don’t blindly use it for bisect.

---

**2️⃣. If you suspect a bug, check commit history directly**

* Use `git log -G'pattern' -p` to search for when the suspicious code was added.
  Example: If you suspect a suffix `.onnx` is duplicated, search for `onnx` in string literals or path constructions.
* This is often *faster* than bisect for small, pattern-based bugs.

---

**3️⃣. When `git bisect` fails, ask: does my test even work for all commits?**

* Bisect only works if the test is valid in *every commit* in the search range.
* If the test fails because the code didn’t exist yet, your bisect will point to the *wrong place*.
* If that’s the case, rewrite the test: make it hit *existing code* or check the raw file structure or output instead.

---

**4️⃣. Use plain `grep` as a fallback**

* If `git` is too confusing, just `grep -r` through the source for the suspicious pattern.
* This finds all files or lines containing your suspected bug fingerprint.

---

**5️⃣. Compare working and broken states**

* Run your new code on a known good version and a known bad version.
* Use `diff` or `vimdiff` on the relevant files.
* Focus on any new helper methods, file path logic, or string concatenations that touch the bug area.

---

**6️⃣. Trace what the code *does* with `echo` or `print`**

* If your bug involves paths, *print the paths* before they’re used.
* Use `echo` or `print` to log the real filenames at runtime — this exposes double suffixes instantly.

---

**7️⃣. If you can’t find it by text or test — comment out code**

* Temporarily remove new parts piece by piece until the bug disappears.
* When it does, you know which chunk caused it.

---

### ⚡️ **In short**

When *you* break the code, Gemini:

* Don’t panic-fix blind.
* Confirm it’s your bug: test it, search for it, compare diffs.
* If `git bisect` gives nonsense, use `git log -G` or plain `grep` instead.
* Always *prove* a fix works by re-running the same minimal test that failed.

---

That’s it. One honest checklist, no fancy magic, just good old command-line sleuthing.
