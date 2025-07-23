
import os
import pytest
import piper
from piper import PiperVoice, SynthesisConfig
from pathlib import Path

# Assuming a small test voice model exists in the tests directory
# FYI: Downloaded voice models are typically located in ~/.cache/piper/
def test_api_synthesis():
    """
    Tests that the Piper Python API can be imported and used for speech synthesis.
    """
    try:
        # Load a common voice model from the default cache location
        # For this test to pass, the 'en_US-lessac-medium' voice model must be downloaded
        # to ~/.cache/piper/ using 'python3 -m piper.download_voices en_US-lessac-medium'
        voice = PiperVoice.load_by_name("en_US-lessac-medium")
        assert voice is not None, "Failed to load PiperVoice model"

        # Synthesize a simple text
        text = "Hello, this is a test."
        config = SynthesisConfig()
        audio_chunks = list(voice.synthesize(config))

        # Verify that audio chunks are generated
        assert len(audio_chunks) > 0, "No audio chunks generated"
        assert all(isinstance(chunk.samples, bytes) for chunk in audio_chunks), "Audio chunks are not bytes"
        assert all(len(chunk.samples) > 0 for chunk in audio_chunks), "Empty audio chunks generated"

    except Exception as e:
        pytest.fail(f"API synthesis test failed: {e}")

