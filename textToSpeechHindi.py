from gtts import gTTS
# from pydub import AudioSegment
# from pydub.playback import play
from deep_translator import GoogleTranslator
import os
from playsound import playsound

def text_to_speech_hindi(eng_output):
    hin_output = GoogleTranslator(source = 'en', target = 'hi').translate(eng_output)
    print(f"Translated text: {hin_output}")

    tts = gTTS(text = hin_output, lang = 'hi')
    
    audio_file = "output.mp3"
    tts.save(audio_file)
    play_audio(audio_file)

def play_audio(audio_file):
    if(os.path.exists(audio_file)):
        playsound(audio_file)
        os.remove(audio_file)
    else:
        print("Audio file not found.")


# if __name__ == "__main__":
#     eng_output = "Hello my name is Manav"           # Dummy Input
#     audio_file = text_to_speech_hindi(eng_output)
#     play_audio(audio_file)
#     os.remove(audio_file)
