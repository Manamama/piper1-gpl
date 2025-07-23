
import os
import pytest
import piper
from piper import PiperVoice, SynthesisConfig
from pathlib import Path

# Assuming a small test voice model exists in the tests directory
TEST_VOICE_MODEL_PATH = Path(__file__).parent / "test_voice.onnx"
TEST_VOICE_CONFIG_PATH = Path(__file__).parent / "test_voice.onnx.json"

@pytest.mark.skipif(not TEST_VOICE_MODEL_PATH.exists() or not TEST_VOICE_CONFIG_PATH.exists(),
                    reason="Test voice model or config not found. Skipping API synthesis test.")
def test_api_synthesis():
    """
    Tests that the Piper Python API can be imported and used for speech synthesis.
    """
    try:
        # Load the voice model
        voice = PiperVoice.load(TEST_VOICE_MODEL_PATH, TEST_VOICE_CONFIG_PATH)
        assert voice is not None, "Failed to load PiperVoice model"

        # Synthesize a simple text
        text = "Hello, this is a test."
        config = SynthesisConfig(text=text)
        audio_chunks = list(voice.synthesize(config))

        # Verify that audio chunks are generated
        assert len(audio_chunks) > 0, "No audio chunks generated"
        assert all(isinstance(chunk.samples, bytes) for chunk in audio_chunks), "Audio chunks are not bytes"
        assert all(len(chunk.samples) > 0 for chunk in audio_chunks), "Empty audio chunks generated"

    except Exception as e:
        pytest.fail(f"API synthesis test failed: {e}")

