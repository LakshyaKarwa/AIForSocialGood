import torchaudio
from speechbrain.inference.classifiers import EncoderClassifier
import speech_recognition as sr
from deep_translator import GoogleTranslator

# Load the SpeechBrain language identifier model
language_id = EncoderClassifier.from_hparams(source="speechbrain/lang-id-voxlingua107-ecapa", savedir="tmp")
recognizer = sr.Recognizer()

def detect_language_from_speech():
    # Capture audio from the microphone
    with sr.Microphone() as source:
        print("Speak now ...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = recognizer.listen(source)

        # Save the captured audio to a temporary file
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data.get_wav_data())

    # Load the audio with torchaudio
    signal = language_id.load_audio("temp_audio.wav")
    print("Detecting Language ...")

    # Classify the language using the SpeechBrain model
    prediction = language_id.classify_batch(signal)

    # Extract the detected language ISO code
    detected_language = prediction[3][0]  # Extract the detected language code (like 'hi' for Hindi)
    print(f"Detected language: {detected_language}")

    return detected_language.split(":")[0]  # return just the language code (e.g., 'hi')

def speech_to_text_dynamic(lang_code):
    with sr.Microphone() as source:
        print(f"Speak something in the detected language ({lang_code})...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's API, with dynamically detected language
            text = recognizer.recognize_google(audio, language=lang_code)
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"RequestError: {str(e)}")

def translate_dynamic_to_english(detected_lang_code):
    input_text = speech_to_text_dynamic(detected_lang_code)

    if input_text:
        # Translate the recognized text into English
        translated_text = GoogleTranslator(source=detected_lang_code, target='en').translate(input_text)
        print(f"Translated text: {translated_text}")
        return translated_text

# Main workflow
if __name__ == '__main__':
    detected_lang_code = detect_language_from_speech()
    translate_dynamic_to_english(detected_lang_code)
