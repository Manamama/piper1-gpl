## Project Context and Current Task

This `GEMINI.md` file provides essential context for working with the `piper1-gpl` project, especially within a Termux (Android) environment.

**Current Task:**
The project is currently in a maintenance status. Our primary focus is to address any issues that may arise and ensure the continued stability and functionality of the `piper1-gpl` project. New features or major refactoring will only be undertaken if specifically requested or deemed critical for the project's health.

## Repository Relationships (July 19, 2025)

This section clarifies the relationships between the various Git repositories encountered during this session to prevent future confusion.

### 1. Current Working Directory Repository (`/data/data/com.termux/files/home/downloads/GitHub/piper1-gpl`)
    *   **Local Path:** `/data/data/com.termux/files/home/downloads/GitHub/piper1-gpl`

*   **Your Fork (`origin` remote):** `https://github.com/Manamama/piper1-gpl`
    *   This is the user's personal fork of the `piper1-gpl` project. Local changes are pushed to this remote.
*   **Original/Upstream (`upstream` remote):** `https://github.com/OHF-Voice/piper1-gpl`
    *   This is the repository from which the user's `Manamama/piper1-gpl` fork was created. Updates are pulled from here to synchronize the user's fork with the original project.

### 2. Separate temp `piper-tts-for-termux` Repository
    *   **Local Path:** `/data/data/com.termux/files/home/downloads/GitHub/piper1-gpl/piper-tts-for-termux`

*   **Its Origin:** `https://github.com/gyroing/piper-tts-for-termux`
    *   This is a distinct Git repository. Its primary online location is `gyroing/piper-tts-for-termux`.
*   **Its Fork Remote:** This repository also contains a remote named `fork` pointing to `https://github.com/Manamama/piper1-gpl.git`. This suggests an interaction or consumption of the user's `piper1-gpl` fork by this `piper-tts-for-termux` project.

## Termux (Android) Build Status and Improvements

This section summarizes the current state of building Piper TTS on Termux, highlighting the successful compilation and the automated improvements implemented.

The project now compiles successfully on Termux. The following key improvements have been made to streamline the build process:

*   **Hybrid `espeak-ng` Strategy**: The build system employs a two-stage strategy for maximum reliability. It first ensures the system's `espeak-ng` package is installed via `pkg` to satisfy any underlying dependencies. It then proceeds to clone and compile a fresh version of `espeak-ng` from source. This guarantees that the project links against a known, consistent version of the library, eliminating potential ABI conflicts and ensuring a self-contained, robust build.
*   **Automated ONNX Runtime Handling**: The `CMakeLists.txt` now automatically detects and links against the system's `libonnxruntime.so` provided by the `python-onnxruntime` Termux package. This eliminates the need for manual downloading, extraction, or linking against pre-compiled `.aar` files, ensuring better ABI compatibility and a more streamlined build process.
*   **ABI Compatibility Resolved**: By ensuring all native C++ components (like `espeakbridge.so` and `piper_phonemize_cpp`) are built and linked against the system's `libc++` and other core libraries, the notorious ABI compatibility issues (such as the `nlohmann::json` parsing errors) are inherently addressed.
*   **Simplified Installation**: The overall goal is to transform the installation into a "go for coffee" experience. After installing the initial `pkg` prerequisites, a simple `pip install piper-tts` will manage the compilation and linking of all native components, allowing the user to focus on using Piper rather than troubleshooting build errors.
*   **Reduced Manual Intervention**: The need for manual extraction of `libonnxruntime.so` from `.aar` files or using `patchelf` for library path adjustments is significantly reduced or provided as clear fallback steps.

## Core Operational Principle: The Strategic Sanity Check

Before executing any file modification or complex command, I must pause and perform a "Strategic Sanity Check." This involves asking:

1.  **What is the overall strategic goal?** (e.g., "To create a reliable build," "To fix a specific bug," "To refactor for clarity.")
2.  **Does my planned action directly and logically serve this goal?**
3.  **Does this action conflict with any "Lessons Learned" or historical failures documented in my memory files?**

If my planned action fails this check—if it is a tactical solution that undermines the strategic goal or repeats a past mistake—I must stop, report the conflict to the user, and propose a better course of action. I will not be a "bulldog" focused only on the immediate task if it compromises the larger objective.

**Termux Environment and Shebangs:** Its crucial to understand that Termux operates on top of the Android OS. When a scripts shebang (e.g., `#!/bin/sh`) is invoked, it typically resolves to the *native Android system shell* (`/bin/sh`), not the Termux shell, unless specific Termux virtualization commands are employed. This native shell is often minimal and may not be suitable for complex build scripts. To ensure scripts are run by the full-featured Termux shell, explicitly invoke them with `/data/data/com.termux/files/usr/bin/bash -c "..."` or ensure the `PATH` is correctly set for the sub-process. If unsure about the nature of a binary or script, use `file <path>` or `ldd <path>` to inspect it.

When testing the ready `piper` package do use the audio models which are located in `~/.cache/piper`. For the API synthesis test to pass, the `en_US-lessac-medium` voice model must be downloaded to `~/.cache/piper/` using `python3 -m piper.download_voices en_US-lessac-medium`. Do use piper's --help to learn how to

## Known Issues

### ImportError: espeakbridge

When attempting to run the `piper` command, an `ImportError` occurs, indicating that the `espeakbridge` module cannot be imported:

```
ImportError: cannot import name 'espeakbridge' from 'piper' (/data/data/com.termux/files/usr/lib/python3.12/site-packages/piper/__init__.py)
```

This suggests that the native `espeakbridge` component, crucial for phonemization, is is not being correctly built or installed during the `pip install .` process. This is the primary blocker for the `piper` package's functionality.

## Build Fixes and Progress

### espeakbridge ImportError Resolved (Manual Build)

The persistent `ImportError: cannot import name 'espeakbridge'` has been addressed. The root cause was the `espeakbridge.c` C extension not being properly compiled and integrated into the Python package.

**Solution:**

`setup.py` was modified to explicitly define `espeakbridge` as a `setuptools.Extension`. This involved:

*   Adding `import sys` and `from setuptools import Extension`.
*   Defining an `espeakbridge_extension` object, specifying `src/piper/espeakbridge.c` as its source.
*   Using `sys.prefix` to dynamically determine the `espeak-ng` include and library paths for portability (e.g., `Path(sys.prefix) / "include" / "espeak-ng"`).
*   Adding `espeakbridge_extension` to the `ext_modules` list in the `setup()` call.

**Verification (Manual Build):**

Running `python3 setup.py build_ext --inplace` successfully compiled `espeakbridge.c` into `espeakbridge.cpython-312.so` and placed it in the `src/piper` directory, resolving the compilation aspect of the `ImportError`.

**Next Steps:**

While the C extension now compiles, the `piper` package itself is not yet fully discoverable by the Python interpreter in a standard way (e.g., `python3 -m piper` still fails). This indicates that a proper installation (e.g., via `pip install .` or `pip install -e .`) is still required to make the package and its entry points accessible in the Python environment.


## Build Fixes and Progress

### espeakbridge ImportError Resolved (Final Solution)

The persistent `ImportError: cannot import name 'espeakbridge'` has been fully addressed, and the `piper` package now installs and functions correctly with `pip install .` (including build isolation).

**Root Cause:**

The primary issue was the `espeakbridge.c` C extension not being properly compiled and integrated into the Python package, specifically due to `setuptools` misinterpreting relative paths as absolute within `pip`'s isolated build environment.

**Solution:**

`setup.py` was modified to explicitly define `espeakbridge` as a `setuptools.Extension` with a robust relative path construction. This involved:

*   Adding `import os` and ensuring `import sys` and `from setuptools import Extension` are present.
*   Defining an `espeakbridge_extension` object.
*   Crucially, setting the `sources` argument for `espeakbridge_extension` to use `os.path.relpath(os.path.join(os.path.dirname(__file__), "src", "piper", "espeakbridge.c"))`. This ensures the path is always correctly interpreted as relative to `setup.py`, even in isolated build environments.
*   Using `sys.prefix` to dynamically determine the `espeak-ng` include and library paths for portability (e.g., `str(Path(sys.prefix) / "include" / "espeak-ng")`).
*   Adding `espeakbridge_extension` to the `ext_modules` list in the `setup()` call.

**Verification:**

Running `pip install . -v` now successfully builds and installs the `piper` package, including the `espeakbridge` C extension. The `piper` command is accessible in the PATH, and speech generation functions as expected.

## README.md Cleanup and Simplification

The `README.md` file has been significantly updated and simplified to reflect the successful build process and provide a clearer user experience. Key changes include:

*   **Introduction of a "Quick Start (Recommended Method)" section**: This new section highlights the streamlined `pip install .` process, making it the primary and easiest way for users to get started.
*   **Removal of obsolete manual build instructions**: All detailed, step-by-step guides for manual compilation, ONNX Runtime handling, and `patchelf` usage have been removed as they are no longer necessary with the automated build.
*   **Consolidation and update of usage examples**: The various usage examples have been combined into a single, comprehensive "Usage" section. All examples now correctly demonstrate how to use the installed Python package via `python3 -m piper`.
*   **Refined "Environment Variables" section**: This section has been updated to reflect the relevant environment variables for the Python API and CLI, removing outdated information.
*   **Removal of the Debian package section**: The section detailing the `piper-tts-cli` deb package has been removed as it is no longer the primary or recommended installation method.
*   **Retention of "Building from Source & Development"**: This section remains and now explicitly points to `docs/BUILDING.md` for advanced users who need detailed build information or wish to contribute to development.

## CMakeLists.txt Merge and Simplification

The project's `CMakeLists.txt` has been refactored to merge platform-specific build logic into a single, unified file. This improves maintainability and simplifies the build process across different operating systems. Key changes include:

*   **Consolidated Build Logic**: The separate build configurations for Windows, Android (Termux), and generic Unix (Linux/macOS) have been merged into one `CMakeLists.txt` using conditional `if(WIN32)`, `elseif(ANDROID)`, and `elseif(UNIX)` blocks.
*   **Platform-Specific External Project Handling**: The `espeak-ng` external project is now built with parameters tailored to each platform (e.g., static libraries for Windows/Unix, shared libraries for Android).
*   **Unified `espeakbridge` Definition**: The `espeakbridge` Python C extension is defined once, with its linking and properties adjusted based on the target platform.
*   **Automated Dependency Management for Android**: The Android-specific section retains the `pkg` calls for automatic installation of Termux prerequisites and the discovery of the system's `onnxruntime` library.
*   **Renamed Original CMakeLists**: The original `CMakeLists.txt` (version 1.3.0) has been renamed to `CMakeLists.txt.bak` for historical reference.

## Lessons Learned from Recent Development Session

This section summarizes key insights and practical takeaways from the recent development session focused on improving the `piper1-gpl` build process and documentation.

### Challenges Encountered:

*   **`replace` tool limitations**: The `replace` tool proved challenging for complex, multi-line text manipulations due to its strict exact-match requirement (including whitespace and indentation). This led to repeated failures and inefficient iterations.
*   **Over-aggressive content removal**: Initial attempts to simplify `README.md` resulted in the accidental removal of valuable end-user information, highlighting the need for a more nuanced approach to documentation updates.
*   **Complexity of `CMakeLists.txt` merge**: While conceptually straightforward, the practical implementation of merging platform-specific CMake logic required meticulous attention to detail regarding variable scoping, external project configurations, and dependency management across Windows, Android, and generic Unix.

### Successes and Facilitating Factors:

*   **Effective problem understanding**: The existing `GEMINI.md` and clear error messages from the `espeakbridge` `ImportError` facilitated a quick grasp of the core build challenges.
*   **Conceptual clarity of CMake merge**: The strategy of using conditional `if(PLATFORM)` blocks for unifying the build system was a clear and effective path forward.

### Key Tools and Strategies:

*   **`run_shell_command` with `sed`**: This proved to be an invaluable tool for robust text manipulation, especially for multi-line replacements and deletions where the `replace` tool struggled. Its flexibility and power were critical in overcoming previous roadblocks.
*   **`GEMINI.md` as a knowledge base**: The detailed historical context and ongoing documentation within `GEMINI.md` provided a strong foundation for understanding project specifics and past solutions.


## Voice Model Status

**Current Status:** The `en_US-lessac-medium` voice model (and its corresponding JSON configuration file) is confirmed to be present and ready in the `~/.cache/piper/` directory. This was verified by running `ls -F ~/.cache/piper/`




## ONNX Model Path Bug Resolved

The runtime error related to the `.onnx.onnx` file path has been resolved. The issue stemmed from a semantic mismatch between `src/piper/__main__.py` and `src/piper/voice.py` regarding how voice model paths were handled. `__main__.py` was passing a full file path to `voice.py`'s `load_by_name` method, which expected a simple voice name and then re-appended the `.onnx` extension, leading to the duplication.

**Resolution:** The bug was resolved by reverting both `src/piper/__main__.py` and `src/piper/voice.py` to their respective `upstream/main` versions. This removed the problematic `load_by_name` method from `voice.py` and restored `__main__.py`'s original logic for handling model paths directly.

**Lessons Learned:** This particular bug proved challenging and time-consuming to diagnose and fix due to several factors, including initial misinterpretations of the problem's scope and the impact of local development environment nuances (e.g., `pip install -e`). A more strategic approach, focusing on understanding the intended API contracts and the propagation of changes, would have led to a quicker resolution. Further lessons learned regarding debugging strategies and AI-human collaboration will be documented soon.

## Plan for `feat/termux-build-pr` Branch Preparation

This section outlines the detailed steps for preparing the `feat/termux-build-pr` branch for the upstream Pull Request, ensuring only relevant changes are included.

1.  **Switch to `feat/termux-build-pr`:** Ensure we are on the correct branch.
    `git checkout feat/termux-build-pr`
2.  **Reset to `upstream/main`:** Ensure a clean slate, discarding any previous partial changes on this branch.
    `git reset --hard upstream/main`
3.  **Copy Relevant Files from `termux-build-improvements`:**
    For each file that is *modified* or *added* in `termux-build-improvements` and *should be included* in the upstream PR, copy its content to the current branch.
    *   **Added Files (from `termux-build-improvements`):**
        *   `Architecture_materials/Mermaid_02.md`
        *   `Architecture_materials/Mermaid_Piper_02.png`
        *   `libpiper/clean_text.cpp`
        *   `libpiper/piper.cpp`
        *   `libpiper/say.cpp`
        *   `pytest.ini`
        *   `src/piper/include/piper.h`
        *   `tests/test_installation_api.py`
        *   `tests/test_installation_cli.py`
    *   **Modified Files (from `termux-build-improvements`):**
        *   `.gitignore`
        *   `CHANGELOG.md`
        *   `CMakeLists.txt`
        *   `README.md`
        *   `docs/BUILDING.md`
        *   `libpiper/CMakeLists.txt`
        *   `pyproject.toml`
        *   `setup.py`
        *   `src/piper/phonemize_espeak.py`
4.  **Handle Deleted Files:** Remove `build_monotonic_align.sh` as it was deleted in `termux-build-improvements` and should be deleted in the upstream PR.
    `rm build_monotonic_align.sh`
5.  **Stage All Changes:** Stage all the copied and deleted files.
    `git add .`
6.  **Commit Changes:** Create a single, comprehensive commit with the agreed-upon message.
    `git commit -m "feat: Termux build improvements and unified CMakeLists.txt

..."`
7.  **Verify Diff:** Confirm that the staged changes accurately reflect only the intended PR content.
    `git diff upstream/main --name-status`
8.  **Run Tests:** Install the package and run the full test suite to ensure everything works as expected on this PR branch.
    `pip install .`
    `pytest`
9.  **Push to Fork:** Push the `feat/termux-build-pr` branch to the user's fork.
    `git push origin feat/termux-build-pr`
10. **Create Pull Request:** Use `gh pr create` to open the PR to `OHF-Voice/piper1-gpl:main`.