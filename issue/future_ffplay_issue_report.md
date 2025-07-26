# ffplay Audio Playback Issue Report

## 1. Issue Description

When attempting to use `piper` for direct audio playback, a `BrokenPipeError` occurs. This prevents the user from hearing the synthesized speech, although saving the output to a WAV file works correctly. The issue is caused by an incompatibility between the arguments `piper` passes to `ffplay` and the version of `ffplay` installed on the user's system.

## 2. System Information

- **Operating System:** Ubuntu 22.04.5 LTS x86_64
- **Kernel:** 6.8.0-60-generic
- **ffplay Version:** 7.1.1 (from `ffplay` command output)
- **Python Version:** 3.10.12
- **Host:** HP Pavilion Laptop 14-ce2xxx

## 3. Diagnosis and Steps to Reproduce

The root cause was identified by isolating `ffplay` from `piper` and testing its behavior with known-good raw audio data (`s16le`, 22050 Hz, mono).

**Test 1: Replicating the Failure Condition (with `-ac 1`)**

- **Command:** `ffplay -f s16le -ar 22050 -ac 1 -i sine_wave.s16le -autoexit -nodisp`
- **Result:** The command failed with the error: `Failed to set value '1' for option 'ac': Option not found`. This confirms that this version of `ffplay` does not support the `-ac` argument in this context.

**Test 2: Verifying the Fix (without `-ac 1`)**

- **Command:** `ffplay -f s16le -ar 22050 -i sine_wave.s16le -autoexit -nodisp`
- **Result:** The command executed successfully, and the audio was played correctly.

This demonstrates that the `-ac 1` argument, while likely intended to ensure `ffplay` correctly interprets the mono audio stream, is the direct cause of the failure on the tested system.

## 4. Deeper Analysis: The `BrokenPipeError`

Even after removing the `-ac 1` argument, the `BrokenPipeError` persisted when running the main `piper` script. This indicated a second, more subtle issue.

**Test 3: Simulating the Python Script's Pipe**

- **Command:** `cat sine_wave.s16le | ffplay -f s16le -ar 22050 -i - -autoexit -nodisp`
- **Result:** This command worked perfectly. `ffplay` successfully played the audio piped from `cat`.

This crucial result proved that `ffplay` can handle piped data correctly, and the issue lies within the Python script's subprocess management.

The `BrokenPipeError` occurs because the `ffplay` process terminates before the Python script has finished writing all the audio data to its `stdin`. This is likely because `ffplay`, when receiving data via a pipe, expects the pipe to be closed to signal the end of the stream. The original Python code only closes the pipe in the `__exit__` method of its `AudioPlayer` context manager, which is too late.

## 5. Proposed Solution

The solution requires two changes:

1.  **Remove the `-ac 1` argument:** This is necessary to prevent the initial `Option not found` error.
2.  **Close `stdin` immediately after writing:** This signals the end of the audio stream to `ffplay`, preventing it from exiting prematurely.

- **File to Modify:** `src/piper/audio_playback.py`

**Combined Code Change:**

```python
# In __enter__ method:
self._proc = subprocess.Popen(
    [
        "ffplay",
        "-nodisp",
        "-autoexit",
        "-f",
        "s16le",
        "-ar",
        str(self.sample_rate),
        "-", # Read from stdin
    ],
    stdin=subprocess.PIPE,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.DEVNULL,
)

# In play method:
self._proc.stdin.write(audio_bytes)
self._proc.stdin.close() # Close stdin immediately after writing
```

This revised approach ensures the `ffplay` command is valid for the user's system and that the pipe handling correctly signals the end of the audio data, resolving the `BrokenPipeError`.