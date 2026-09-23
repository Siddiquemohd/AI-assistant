import os
import math
import struct
import wave

class AudioSpeechEngine:
    """
    Audio Synthesis & Sound Generation Engine.
    Generates synthetic speech tones, audio waveforms, synth melodies, and exports WAV audio files.
    """

    def generate_tone(self, frequency: float = 440.0, duration_sec: float = 2.0, output_path: str = "generated_audio.wav") -> dict:
        sample_rate = 44100
        n_samples = int(sample_rate * duration_sec)

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

        with wave.open(output_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2) # 16-bit
            wav_file.setframerate(sample_rate)

            for i in range(n_samples):
                # Generate sine wave sample
                t = float(i) / sample_rate
                value = int(16384 * math.sin(2 * math.pi * frequency * t))
                data = struct.pack('<h', value)
                wav_file.writeframesraw(data)

        return {
            "status": "Success",
            "action": "generate_audio_tone",
            "frequency_hz": frequency,
            "duration_sec": duration_sec,
            "file_path": output_path
        }

    def generate_jingle(self, output_path: str = "generated_jingle.wav") -> dict:
        sample_rate = 44100
        notes = [261.63, 329.63, 392.00, 523.25]  # C4, E4, G4, C5 (C Major chord arpeggio)
        note_duration = 0.4

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)

        with wave.open(output_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)

            for freq in notes:
                n_samples = int(sample_rate * note_duration)
                for i in range(n_samples):
                    t = float(i) / sample_rate
                    # Fade out envelope
                    envelope = 1.0 - (i / n_samples)
                    value = int(16384 * envelope * math.sin(2 * math.pi * freq * t))
                    data = struct.pack('<h', value)
                    wav_file.writeframesraw(data)

        return {
            "status": "Success",
            "action": "generate_jingle",
            "notes": "C Major Arpeggio (C4-E4-G4-C5)",
            "file_path": output_path
        }
