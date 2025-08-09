# Analysis of Android Build Failures and Remediation Plan

## 1. Overview

Based on a detailed analysis of the build logs, `CMakeLists.txt`, and user-submitted bug reports (GitHub Issue #2 in the `Manamama/piper1-gpl` fork), the current Android build process is unreliable due to two distinct, sequential failures. First, it creates a runtime dependency issue, which then masks a deeper compile-time failure. This document details both issues and proposes a remediation plan.

---

## 2. Failure Mode #1: Unwanted Runtime Dependency on PulseAudio

This is the first issue a user may encounter, manifesting as a runtime error.

### Symptom

The application fails to run after a seemingly successful installation. The error indicates that a shared library such as `libpulse-simple.so` or `libpulse.so` cannot be found.

### Evidence

This is confirmed by the initial bug report in `Manamama/piper1-gpl#2`, where the user was forced to manually create symbolic links to satisfy the linker:

```bash
# User-reported workaround
ln -s /data/data/com.termux/files/usr/lib/libpulse.so.0 /data/data/com.termux/files/usr/lib/libpulse-simple.so
ln -s /data/data/com.termux/files/usr/lib/libpulse.so.0 /data/data/com.termux/files/usr/lib/libpulse.so
```

### Root Cause Analysis

The `espeak-ng` `ExternalProject` build defined in `CMakeLists.txt` is configured to run `./configure` without specifying which audio backends to use. The `configure` script is "smart" and detects that `pulseaudio` is available in the Termux environment. It therefore automatically compiles `espeak-ng` with its PulseAudio output module enabled, creating an unwanted dynamic link dependency on the PulseAudio libraries.

---

## 3. Failure Mode #2: Incorrect Compile-Time Header Path

This is the more fundamental failure. It occurs during the `pip install .` process and prevents the wheel from being built successfully.

### Symptom

The build process fails with a C compiler error while compiling `src/piper/espeakbridge.c`.

### Evidence

This is confirmed by our own test and by the final comment in `Manamama/piper1-gpl#2`. The error log is identical in both cases:

```c
creating _skbuild/linux-aarch64-3.12/setuptools/temp.linux-aarch64-cpython-312/src/piper
clang -Wno-error=implicit-function-declaration -fPIC -I/data/data/com.termux/files/usr/include/espeak-ng -I/data/data/com.termux/files/usr/include/python3.12 -c src/piper/espeakbridge.c -o .../espeakbridge.o

src/piper/espeakbridge.c:63:32: warning: call to undeclared function 'espeak_TextToPhonemesWithTerminator'; ISO C99 and later do not support implicit function declarations [-Wimplicit-function-declaration]
   63 |         const char *phonemes = espeak_TextToPhonemesWithTerminator(
      |                                ^
src/piper/espeakbridge.c:63:21: error: incompatible integer to pointer conversion initializing 'const char *' with an expression of type 'int' [-Wint-conversion]
   63 |         const char *phonemes = espeak_TextToPhonemesWithTerminator(
      |                     ^          ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
...
1 warning and 1 error generated.
error: command '/data/data/com.termux/files/usr/bin/clang' failed with exit code 1
```

### Root Cause Analysis

The `clang` command's `-I` flag, which sets the include path for header files, is pointing to the wrong location: `-I/data/data/com.termux/files/usr/include/espeak-ng`. This is the path for the generic, system-wide `espeak-ng` installed by `pkg`.

This system version is older and its headers do not contain the required `espeak_TextToPhonemesWithTerminator` function. The build system **should** be using the headers from the private, up-to-date `espeak-ng` that was just built inside the `_skbuild` directory.

---

## 4. Proposed Remediation Plan

To fix the build, we must address both failures in the `CMakeLists.txt` file.

### Step 1: Disable Unwanted `espeak-ng` Audio Modules

We need to modify the `espeak-ng` `ExternalProject` build to ensure it is a pure phonemization engine with no audio output capabilities. This will remove the unwanted PulseAudio dependency.

**Action:** Add the `--without-speech-backends` flag to the `espeak-ng` configure command. This is the canonical way to disable all audio output modules.

*   **File:** `CMakeLists.txt`
*   **Current Line:** `CONFIGURE_COMMAND sh -c "cd ${ESPEAK_NG_SRC_DIR} && ./autogen.sh && ./configure --prefix=${ESPEAK_NG_INSTALL_DIR}"`
*   **Proposed Change:** `CONFIGURE_COMMAND sh -c "cd ${ESPEAK_NG_SRC_DIR} && ./autogen.sh && ./configure --prefix=${ESPEAK_NG_INSTALL_DIR} --without-speech-backends"`

### Step 2: Correct the `espeakbridge` Include Path

We must ensure that the `espeakbridge` C extension is compiled using the correct headers from our private `espeak-ng` build, not the system headers.

**Action:** The `target_include_directories` for `espeakbridge` already correctly lists `${ESPEAKNG_INCLUDE_DIR}`. The problem is that an implicit system path is likely taking precedence. We should explicitly remove any system `espeak-ng` path from the compiler's search.

*   **File:** `CMakeLists.txt`
*   **Action:** While the `target_include_directories` seems correct, we need to ensure no other part of the build process (like `setup.py` or environment variables) is injecting the incorrect system path. A definitive fix is to ensure our private include path is passed with `-I` and that no other `-I/data/data/com.termux/files/usr/include/espeak-ng` is present in the final `clang` command.

### Step 3: Verification

After applying these fixes, the following steps will verify the solution:

1.  **Clean Build:** Run `rm -rf _skbuild` and then `pip install . -v`.
2.  **Verify Compilation:** The build should complete successfully with no errors.
3.  **Verify Linkage (`ldd`):** Run `ldd` on the newly built `_skbuild/.../lib/libespeak-ng.so`. It should **not** list any dependencies on `libpulse.so` or `libpulse-simple.so`.
4.  **Verify Functionality:** Run the `piper` command to ensure it operates correctly.

### Step 4: Documentation and Release Workflow

Once the technical fixes in Steps 1 and 2 are verified, the following steps will ensure the project is properly documented and prepared for a new release.

**A. Update Documentation**

1.  **Update `docs/BUILDING.md`:** Revise the build guide to reflect the corrected build process and dependency handling on Android.
2.  **Update Architecture Diagram:** Regenerate the `Mermaid_02.md` diagram to accurately represent the new build logic.
3.  **Render PNG Diagram:** Convert the updated Mermaid diagram to a PNG image, as it is displayed in the main `README.md`.
4.  **Review `README.md`:** Ensure the main `README.md` is consistent with all changes.

**B. Versioning**

1.  **Increment Version:** Update the project version in `pyproject.toml` to a new development tag (e.g., `1.3.7-dev`) in accordance with semantic versioning.

**C. Commit and Push**

1.  **Stage Changes:** Add all modified files to the staging area (`git add .`).
2.  **Commit:** Create a single, comprehensive commit with a descriptive message summarizing the build fixes.
3.  **Push:** Push the commit to the `origin` remote repository.