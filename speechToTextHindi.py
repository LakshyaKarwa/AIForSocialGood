import speech_recognition as sr

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
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")

speech_to_text_hindi()
