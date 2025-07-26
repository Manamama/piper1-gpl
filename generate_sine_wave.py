
import numpy as np

sr = 22050
freq = 440
duration = 1
t = np.linspace(0, duration, int(sr * duration), False)
audio = np.sin(2 * np.pi * freq * t)
audio_int16 = (audio * 32767).astype(np.int16)

with open('/home/zezen/Downloads/GitHub/piper1-gpl/sine_wave.s16le', 'wb') as f:
    f.write(audio_int16.tobytes())
