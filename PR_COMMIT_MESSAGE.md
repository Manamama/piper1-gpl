feat: Termux build improvements and unified CMakeLists.txt

This commit introduces significant improvements to the Piper TTS build process, with a particular focus on streamlining installation and enhancing Termux (Android) compatibility.

Key changes include:
- **Unified CMakeLists.txt:** Refactored the build configuration into a single, platform-agnostic `CMakeLists.txt` file, simplifying maintenance across Windows, Linux, and Android.
- **Automated Termux Dependency Handling:** The build process now automatically manages Termux-specific prerequisites like `espeak-ng` and `onnxruntime`, providing a more seamless "pip install ." experience.
- **Resolved ABI Compatibility:** Addressed notorious ABI compatibility issues by ensuring all native components are built and linked against consistent system libraries.
- **Updated Documentation:** `README.md` and `docs/BUILDING.md` have been revised to reflect the simplified installation and build procedures.
- **New Test Coverage:** Added `test_installation_api.py` and `test_installation_cli.py` to verify the streamlined installation process.
