## Voice Model Status

**Current Status:** The `en_US-lessac-medium` voice model (and its corresponding JSON configuration file) is confirmed to be present and ready in the `~/.cache/piper/` directory. This was verified by running `ls -F ~/.cache/piper/`.

## Failed Fix Attempts for `TypeError: argument should be a str or an os.PathLike object where __fspath__ returns a str, not 'NoneType'` in `test_installation_cli.py`

The `test_installation_cli.py` continues to fail with a `TypeError` related to `espeak_data_dir` being `None` when `PiperVoice.load_by_name` is called within the `piper` subprocess. The following attempts were made to resolve this issue, but were unsuccessful:

1.  **Modification in `src/piper/__main__.py` (Attempt 1):** Changed `espeak_data_dir=None` to `espeak_data_dir=args.data_dir[0]`.
    *   **Reasoning:** Initially, `args.data_dir` was an array due to `action="append"`, and `espeak_data_dir` was hardcoded to `None`. This change aimed to pass the first element of the `data_dir` list.
    *   **Outcome:** The `TypeError` persisted, indicating `args.data_dir[0]` was still `None` or not a valid path.

2.  **Modification in `src/piper/__main__.py` (Attempt 2):** Removed `action="append"` from the `--data-dir` argument definition.
    *   **Reasoning:** This was intended to make `args.data_dir` a single string, as `PiperVoice.load_by_name` expects a string or Path object, not a list.
    *   **Outcome:** The `TypeError` persisted.

3.  **Modification in `src/piper/__main__.py` (Attempt 3):** Reverted the change from Attempt 1, setting `espeak_data_dir=args.data_dir` directly.
    *   **Reasoning:** After removing `action="append"`, `args.data_dir` should have been a string, so direct assignment was appropriate.
    *   **Outcome:** The `TypeError` persisted.

4.  **Modification in `test_installation_cli.py` (Attempt 4):** Added `env={"HOME": str(Path.home())}` to the `subprocess.run` call.
    *   **Reasoning:** This was an attempt to ensure `Path.home()` resolved correctly within the isolated `subprocess` environment, as `NoneType` errors can sometimes stem from environment variable issues.
    *   **Outcome:** The `TypeError` persisted.

The root cause of `espeak_data_dir` being `None` within the `piper` subprocess remains elusive, despite these attempts to correctly pass the `--data-dir` argument and ensure `Path.home()` resolution. The traceback consistently points to `espeak_data_dir=Path(espeak_data_dir)` in `piper/voice.py`, line 134, where `espeak_data_dir` is `None`."