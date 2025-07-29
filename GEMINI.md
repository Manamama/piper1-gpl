The Pull Request has been rejected. We are currently strategizing on how to proceed.

## Project Status (July 29, 2025)

This `GEMINI.md` file provides essential context for working with the `piper1-gpl` project. The primary development phase, focused on creating a robust and easily installable package for Termux (Android), was completed, but the associated Pull Request was rejected.

**Current Status:**
The Pull Request to merge the `feat/termux-build-pr` branch into the upstream `OHF-Voice/piper1-gpl` repository has been rejected. The developer's feedback was: "Thank you for the PR, but there are way too many things being done at once. Please split this PR into multiples with a single, focused change in each so that we can discuss them individually." We are now planning how to break down the changes into smaller, more focused Pull Requests, as per the following strategy:

**Proposed PR Splitting Strategy:**

**PR 1: Universal Build System Refinement & Termux Integration**
*   **Focus:** This PR will encompass all the core build system changes that make Piper's build more universal and specifically enable the Termux integration. This includes the unified `CMakeLists.txt` files, the `setup.py` modifications that tie into the build system, and the `pyproject.toml` changes. It also includes the `espeakbridge` and `phonemize_espeak.py` changes that are fundamental to the Termux build's dependency handling. The `Architecture_materials` would also fit here as they describe this new build system.
*   **Files:**
    *   `CMakeLists.txt` (root)
    *   `libpiper/CMakeLists.txt`
    *   `setup.py`
    *   `pyproject.toml`
    *   `src/piper/phonemize_espeak.py`
    *   `src/piper/include/piper.h` (if modified for build system, otherwise it's core API)
    *   `.gitignore`
    *   `Architecture_materials/Mermaid_02.md`
    *   `Architecture_materials/Mermaid_Piper_02.png`

**PR 2: Enhanced CLI Features & Text Processing**
*   **Focus:** This PR will contain the new user-facing features and improvements to the CLI, including the `say.cpp` and `clean_text.cpp` additions. These are distinct functional enhancements that build upon the underlying `libpiper` and `espeak-ng` integration.
*   **Files:**
    *   `libpiper/piper.cpp`
    *   `libpiper/say.cpp`
    *   `libpiper/clean_text.cpp`

**PR 3: Installation & CLI Tests**
*   **Focus:** This PR will introduce the new tests specifically designed to verify the successful installation and basic functionality of the API and CLI. These tests are crucial for validating the changes in PR1 and PR2.
*   **Files:**
    *   `pytest.ini`
    *   `tests/test_installation_api.py`
    *   `tests/test_installation_cli.py`

**PR 4: Documentation Updates**
*   **Focus:** This PR will update the `README.md`, `docs/BUILDING.md`, and `CHANGELOG.md` to reflect all the changes introduced in the previous PRs. This should be the last PR, as it summarizes everything.
*   **Files:**
    *   `README.md`
    *   `docs/BUILDING.md`
    *   `CHANGELOG.md`

**Rationale for this revised splitting:**

*   **Addresses "Too Many Things":** This breaks down the massive original PR into four distinct, yet logically connected, feature sets.
*   **Maintains Cohesion:** Each PR still represents a cohesive unit of work.
*   **Clear Dependencies:** PR1 is foundational. PR2 and PR3 can potentially be developed in parallel but depend on PR1 being merged. PR4 depends on all previous PRs.
*   **Easier Review:** Reviewers can focus on the build system, then the new features, then the tests, and finally the documentation.


**Pull Request Location:** [https://github.com/OHF-Voice/piper1-gpl/pull/21](https://github.com/OHF-Voice/piper1-gpl/pull/21)

### Key Accomplishments

*   **Unified Build System:** The `CMakeLists.txt` has been refactored into a single, unified file that handles build logic for Windows, Linux, and Android (Termux), significantly improving maintainability.
*   **Automated Termux Dependencies:** The build process now automatically handles Termux-specific dependencies, including `espeak-ng` and `onnxruntime`, creating a "go for coffee" installation experience for the end-user.
*   **ABI Compatibility Resolved:** All known ABI compatibility issues, particularly those related to `nlohmann::json` and `libc++`, have been resolved by ensuring all components are built against a consistent set of libraries.
*   **Comprehensive Documentation:** The `README.md` and `docs/BUILDING.md` files have been updated to reflect the new, simplified build process.

## PR Preparation Plan

The following plan was executed to prepare the `feat/termux-build-pr` branch for submission. These steps are retained for future reference and as a guide for similar PR processes.

**Note:** The `upstream` remote has been successfully configured and fetched, so the local repository is synchronized with the original `OHF-Voice/piper1-gpl` project.

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
4.  **Handle Deleted Files:** Ensure that files deleted in `termux-build-improvements` are also deleted in the PR branch. For example, `build_monotonic_align.sh` was deleted in `termux-build-improvements` and should not be present in the upstream PR.
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

## Repository Relationships (July 28, 2025)

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
    *   This is a distinct Git repository. Its primary online location is `https://github.com/gyroing/piper-tts-for-termux`.
*   **Its Fork Remote:** This repository also contains a remote named `fork` pointing to `https://github.com/Manamama/piper1-gpl.git`. This suggests an interaction or consumption of the user's `piper1-gpl` fork by this `piper-tts-for-termux` project.

## Core Operational Principle: The Strategic Sanity Check

Before executing any file modification or complex command, I must pause and perform a "Strategic Sanity Check." This involves asking:

1.  **What is the overall strategic goal?** (e.g., "To create a reliable build," "To fix a specific bug," "To refactor for clarity.")
2.  **Does my planned action directly and logically serve this goal?**
3.  **Does this action conflict with any "Lessons Learned" or historical failures documented in my memory files?**

If my planned action fails this check—if it is a tactical solution that undermines the strategic goal or repeats a past mistake—I must stop, report the conflict to the user, and propose a better course of action. I will not be a "bulldog" focused only on the immediate task if it compromises the larger objective.

**Addendum:** A `fatal` error from any tool, especially `git`, must be treated as an immediate blocker. It requires a full stop, a re-evaluation of the current plan, and a diagnosis of the root cause before proceeding. It is a signal to exit "execution mode" and enter "analysis mode."

**Termux Environment and Shebangs:** Its crucial to understand that Termux operates on top of the Android OS. When a scripts shebang (e.g., `#!/bin/sh`) is invoked, it typically resolves to the *native Android system shell* (`/bin/sh`), not the Termux shell, unless specific Termux virtualization commands are employed. This native shell is often minimal and may not be suitable for complex build scripts. To ensure scripts are run by the full-featured Termux shell, explicitly invoke them with `/data/data/com.termux/files/usr/bin/bash -c "..."` or ensure the `PATH` is correctly set for the sub-process. If unsure about the nature of a binary or script, use `file <path>` or `ldd <path>` to inspect it.

When testing the ready `piper` package do use the audio models which are located in `~/.cache/piper`. For the API synthesis test to pass, the `en_US-lessac-medium` voice model must be downloaded to `~/.cache/piper/` using `python3 -m piper.download_voices en_US-lessac-medium`. Do use piper's --help to learn how to