import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory

# Ensuring consistent results by setting seed
DetectorFactory.seed = 0

recognizer = sr.Recognizer()

def speech_to_text():
    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's API
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"RequestError: {str(e)}")


def detect_language(text):
    try:
        lang = detect(text)
        print(f"Detected language: {lang}")
        return lang
    except Exception as e:
        print(f"Language detection error: {str(e)}")
        return None


def translate_text(text, target_lang='en'):
    detected_lang = detect_language(text)
    
    if detected_lang:
        try:
            translated_text = GoogleTranslator(source=detected_lang, target=target_lang).translate(text)
            print(f"Translated text ({detected_lang} -> {target_lang}): {translated_text}")
            return translated_text
        except Exception as e:
            print(f"Translation error: {str(e)}")
    else:
        print("Could not detect language. Translation skipped.")


def speech_to_translation(target_lang='en'):
    spoken_text = speech_to_text()
    if spoken_text:
        translate_text(spoken_text, target_lang=target_lang)


# Example call
speech_to_translation(target_lang='en')  # You can change the target language as needed
