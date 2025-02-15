import requests
import sounddevice as sd
import wave
import numpy as np


def convert_to_text():
    url = "https://api.sarvam.ai/speech-to-text"
    headers = {"api-subscription-key": "bc7fbc92-5b5a-494c-abc5-2f54b52dc91b"}

    files = {
        "file": ("audio.wav", open("audio.wav", "rb"), "audio/wav"),
    }
    data = {"model": "saarika:v2", "language_code": "en-IN", "with_timestamps": "false"}

    response = requests.post(url, headers=headers, files=files, data=data)

    print(response.text)


def recordVoice():
    sample_rate = 44100  # Sampling rate
    channels = 1  # Mono audio
    filename = "audio.wav"

    # Wait for user input to start recording
    input("Press Enter to start recording...")
    print("Recording... Press Enter again to stop.")

    recording = []
    stream = sd.InputStream(samplerate=sample_rate, channels=channels, dtype=np.int16)

    with stream:
        while True:
            # Read audio in small chunks
            audio_chunk, _ = stream.read(1024)
            recording.append(audio_chunk)

            # Check if Enter is pressed again
            if input() == "":
                break

    print("Recording stopped.")

    # Convert list of chunks to NumPy array
    audio_data = np.concatenate(recording, axis=0)

    # Save to WAV file
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit audio
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

    print(f"Audio saved as {filename}")


recordVoice()
convert_to_text()
