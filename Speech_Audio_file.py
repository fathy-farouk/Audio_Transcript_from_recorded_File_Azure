# Import required namespaces
import azure.cognitiveservices.speech as speech_sdk
import os
import json
from dotenv import load_dotenv

#----------------------------------------------------------------------------------------
# ✅ Load API Credentials from .env file
load_dotenv()
ai_key = os.getenv("AI_KEY")
ai_region = os.getenv("AI_REGION")

#----------------------------------------------------------------------------------------
# ✅ Configure Speech Service
speech_config = speech_sdk.SpeechConfig(subscription=ai_key, region=ai_region)
print('✅ Ready to use speech service in:', speech_config.region)

#-----------------------------------------------------------------------------------------------
# ✅ Convert M4A to WAV using `ffmpeg`
import ffmpeg
input_file = "recording_EN.m4a"
output_file = "recording_EN.wav"

try:
    ffmpeg.input(input_file).output(output_file).run(overwrite_output=True)
    print(f"✅ Conversion complete! Saved as {output_file}")
except Exception as e:
    print(f"❌ Error converting file: {e}")
    exit()  # Stop execution if conversion fails

#----------------------------------------------------------------------------------------

# ✅ Configure Speech Recognition (Using Default Microphone)
from playsound import playsound
current_dir = os.getcwd()
audioFile = current_dir + '\\recording_EN.wav'

import winsound
winsound.PlaySound(audioFile, winsound.SND_FILENAME)

# playsound(audioFile)
audio_config = speech_sdk.AudioConfig(filename=audioFile)


from azure.cognitiveservices.speech import SpeechRecognizer, AutoDetectSourceLanguageConfig, AudioConfig
# ✅ Enable Auto Language Detection (Arabic + English)
auto_detect_lang_config = AutoDetectSourceLanguageConfig(languages=["ar-EG", "en-US"])
# ✅ Corrected Speech Recognizer Initialization
speech_recognizer = SpeechRecognizer(speech_config=speech_config,auto_detect_source_language_config=auto_detect_lang_config,audio_config=audio_config)


#----------------------------------------------------------------------------------------
# ✅ Process Speech Input
print('🎤 Speak now...')
speech = speech_recognizer.recognize_once_async().get()

if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
    print("\n✅ Recognized Speech:", speech.text)
    print("🕒 Speech Duration:", speech.duration)
    print("📍 Speech Offset:", speech.offset)

    # ✅ Extract Detected Language
    try:
        detected_lang_json = json.loads(speech.properties.get(speech_sdk.PropertyId.SpeechServiceResponse_JsonResult, "{}"))
        print("\n📜 Full JSON Response:\n", json.dumps(detected_lang_json, indent=4, ensure_ascii=False))  # Pretty Print JSON

        detected_language = detected_lang_json.get("PrimaryLanguage", {}).get("Language", "Unknown")
        print("🌍 Detected Language:", detected_language)

    except json.JSONDecodeError as e:
        print("❌ Error decoding JSON response:", e)

else:
    print("\n⚠️ Speech Recognition Failed:", speech.reason)
    
    # ✅ Handle Canceled Recognition
    if speech.reason == speech_sdk.ResultReason.Canceled:
        cancellation = speech.cancellation_details
        print("❌ Cancellation Reason:", cancellation.reason)
        print("⚠️ Error Details:", cancellation.error_details)

