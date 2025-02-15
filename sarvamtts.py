import requests
import base64

url = "https://api.sarvam.ai/text-to-speech"

payload = {
    "inputs": ["what is your name?"],
    "target_language_code": "en-IN",
    "speaker": "maya",
    "pitch": -0.5,
    "pace": 1,
    "loudness": 1.5,
    "speech_sample_rate": 16000,
    "enable_preprocessing": False,
    "model": "bulbul:v1",
    "eng_interpolation_wt": 123,
    "override_triplets": {},
}
headers = {
    "api-subscription-key": "bc7fbc92-5b5a-494c-abc5-2f54b52dc91b",
    "Content-Type": "application/json",
}

response = requests.post(url, json=payload, headers=headers)

if response.status_code == 200:
    try:
        data = response.json()
        if "audios" in data and data["audios"]:
            audio_base64 = data["audios"][0]  # Assuming it's base64 encoded
            audio_binary = base64.b64decode(audio_base64)

            out_file = "audio.wav"
            with open(out_file, "wb") as fout:
                fout.write(audio_binary)
            print(f"Audio file saved as {out_file}")
        else:
            print("No audio data found in response.")
    except Exception as e:
        print(f"Error processing response: {e}")
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")
