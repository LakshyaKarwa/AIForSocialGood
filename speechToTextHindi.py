import speech_recognition as sr
from deep_translator import GoogleTranslator

recognizer = sr.Recognizer()

def speech_to_text_hindi():
    with sr.Microphone() as source:
        print("Speak something in Hindi...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio = recognizer.listen(source)

        try:
            # Recognize speech using Google's API with Hindi language code
            text = recognizer.recognize_google(audio, language="hi-IN")
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError as e:
            print(f"RequestError: {str(e)}")


def translate_hindi_to_english():
    hin_input = speech_to_text_hindi()
    eng_input = GoogleTranslator(source = 'hi', target = 'en').translate(hin_input)
    print(f"Translated text: {eng_input}")
    return eng_input

# if __name__ == '__main__':
#     eng_input = translate_hindi_to_english()
