# 🛠️ Building Manually

We use [scikit-build-core](https://github.com/scikit-build/scikit-build-core) along with [cmake](https://cmake.org/) to build a Python module that directly embeds [espeak-ng][].

You will need the following system packages installed (`apt-get`):

* `build-essential`
* `cmake`
* `ninja-build`

To create a dev environment:

``` sh
git clone https://github.com/OHF-voice/piper1-gpl.git
cd piper1-gpl
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -e .[dev]
```

Next, run `script/dev_build` or manually build the extension:

``` sh
python3 setup.py build_ext --inplace
```

Now you should be able to use `script/run` or manually run Piper:

``` sh
python3 -m piper --help
```

You can manually build wheels with:

``` sh
python3 -m build
```

## Design Decisions

[espeak-ng][] is used via a small Python bridge in `espeakbridge.c` which uses Python's [limited API][limited-api]. This allows the use of Python's [stable ABI][stable-abi], which means Piper wheels only need to be built once for each platform (Linux, Mac, Windows) instead of for each platform **and** Python version.

We build upstream [espeak-ng][] since they added the `espeak_TextToPhonemesWithTerminator` that Piper depends on. This function gets phonemes for text as well as the "terminator" that ends each text clause, such as a comma or period. Piper requires this terminator because punctuation is passed on to the voice model as "phonemes" so they can influence synthesis. For example, a voice trained with statements (ends with "."), questions (ends with "?"), and exclamations (ends with "!") may pronounce sentences ending in each punctuation mark differently. Commas, colons, and semicolons are also useful for proper pauses in synthesized audio.

<!-- Links -->
[espeak-ng]: https://github.com/espeak-ng/espeak-ng
[limited-api]: https://docs.python.org/3/c-api/stable.html#limited-c-api
[stable-abi]: https://docs.python.org/3/c-api/stable.html#stable-abi

---

## 📱 Termux (Android) Specifics

For Termux users, the goal is to make `pip install piper-tts` as seamless as possible, handling native dependencies automatically. With the proposed changes to `CMakeLists.txt` (which are part of this fork), the build process will be adapted to the Termux environment.

### How it Should Work for Termux Users:

1.  **Install Termux System Packages**: Before running `pip install`, ensure you have the necessary build tools and the `espeak` library installed via `pkg`:

    ```bash
    pkg update && pkg install git cmake build-essential ninja espeak
    ```

2.  **Automated ONNX Runtime Library Handling**:

    The Piper Python module's C++ extensions (`piper_phonemize_cpp`) depend on `libonnxruntime.so`. The modified `CMakeLists.txt` will be enhanced to **automatically download, extract, and link** this shared library during the `pip install` process. This means you will **not** need to manually handle `.aar` files or place `libonnxruntime.so` yourself.

    **Conceptual Automation within `CMakeLists.txt`:**

    *   **Download**: The `CMakeLists.txt` will use CMake's `file(DOWNLOAD ...)` command to fetch the `onnxruntime-android-X.Y.Z.aar` file from the official Maven repository. The version will be determined programmatically or set as a variable.
    *   **Extract**: After downloading, CMake will execute a process (e.g., `execute_process(COMMAND unzip ...)` or `cmake -E tar ...`) to extract the `libonnxruntime.so` file from within the `.aar` (specifically from `jni/arm64-v8a/` for Termux).
    *   **Place and Link**: The extracted `libonnxruntime.so` will then be copied to a build-specific location, and the `CMakeLists.txt` will ensure that Piper's native extensions are correctly linked against this library during compilation. This will resolve the `OrtGetApiBase` errors.

3.  **Simple `pip install`**: Once the system packages are in place, you can install Piper directly using `pip`:

    ```bash
    pip install piper-tts
    ```

    This command will trigger the compilation of Piper's native extensions, which will now correctly link against your Termux system's libraries, allowing you to go for coffee while it builds.

### What This Means for the User:

With the proposed architectural changes to `CMakeLists.txt` within this fork, the `pip install piper-tts` process on Termux will be significantly streamlined and more robust. The complexities of managing native dependencies are now handled by the build system itself.

*   **Automated `espeak-ng` Integration**: The build system will now intelligently detect and link against your system-installed `espeak-ng` (ensuring you have run `pkg install espeak`). This eliminates the need for complex `ExternalProject` builds and ensures ABI compatibility with your Termux environment.
*   **Automated ONNX Runtime Linking**: The `CMakeLists.txt` will be updated to **automatically download, extract, and correctly link** against the necessary `libonnxruntime.so` shared library. This means the `piper_phonemize_cpp` extension will find its required symbols, resolving the `OrtGetApiBase` errors encountered previously. The user will **not** need to manually download or place `.aar` files.
*   **ABI Compatibility Resolved**: By ensuring all native C++ components (like `espeakbridge.so` and `piper_phonemize_cpp`) are built and linked against the system's `libc++` and other core libraries, the notorious ABI compatibility issues (such as the `nlohmann::json` parsing errors) are inherently addressed.
*   **Simplified Installation**: The overall goal is to transform the installation into a "go for coffee" experience. After installing the initial `pkg` prerequisites, a simple `pip install piper-tts` will manage the compilation and linking of all native components, allowing the user to focus on using Piper rather than troubleshooting build errors.
*   **No `patchelf`**: Complex patching of shared libraries will be unnecessary.

This conceptual outline reflects the desired state after the `CMakeLists.txt` modifications are integrated into the main project. It aims to provide a much smoother experience for Termux users.
