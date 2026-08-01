"""Sintetizador de sonidos usando archivos WAV generados programáticamente.

Los WAV se generan al importar el módulo usando solo la librería estándar
(wave + struct + math). Se cachean en assets/sounds/ y se reproducen con
winsound en Windows.
"""

import math
import struct
import wave
import sys
from pathlib import Path

SOUNDS_DIR = Path("assets/sounds")
SOUNDS_DIR.mkdir(parents=True, exist_ok=True)

SAMPLE_RATE = 44100

SOUND_DEFS = {
    "start": {"type": "sine", "freq_start": 600, "freq_end": 1000, "duration": 0.12, "gain": 0.15},
    "pause": {"type": "sine", "freq_start": 800, "freq_end": 400, "duration": 0.12, "gain": 0.15},
    "reset": {"type": "triangle", "freq_start": 350, "freq_end": 200, "duration": 0.18, "gain": 0.2},
    "tick": {"type": "square", "freq_start": 1200, "freq_end": 1200, "duration": 0.03, "gain": 0.03},
}


def _generate_waveform(wave_type: str, freq: float, t: float) -> float:
    phase = 2.0 * math.pi * freq * t
    if wave_type == "sine":
        return math.sin(phase)
    elif wave_type == "triangle":
        return (2.0 / math.pi) * math.asin(math.sin(phase))
    elif wave_type == "square":
        return 1.0 if math.sin(phase) >= 0 else -1.0
    return math.sin(phase)


def _generate_wav(name: str) -> str:
    """Genera un archivo WAV y retorna la ruta."""
    defn = SOUND_DEFS[name]
    path = SOUNDS_DIR / f"{name}.wav"
    if path.exists():
        return str(path)

    num_samples = int(SAMPLE_RATE * defn["duration"])
    samples = []

    for i in range(num_samples):
        t = i / SAMPLE_RATE
        progress = t / defn["duration"]
        freq = defn["freq_start"] + (defn["freq_end"] - defn["freq_start"]) * progress
        env = 1.0 - progress
        sample = _generate_waveform(defn["type"], freq, t) * defn["gain"] * env
        samples.append(int(max(-32767, min(32767, sample * 32767))))

    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(struct.pack(f"<{len(samples)}h", *samples))

    return str(path)


_WAV_PATHS = {name: _generate_wav(name) for name in SOUND_DEFS}


def play_beep(beep_type: str) -> None:
    """Reproduce el sonido sintetizado para la acción indicada."""
    if beep_type not in _WAV_PATHS:
        return
    try:
        if sys.platform == "win32":
            import winsound
            winsound.PlaySound(_WAV_PATHS[beep_type], winsound.SND_FILENAME | winsound.SND_ASYNC)
    except Exception:
        pass
