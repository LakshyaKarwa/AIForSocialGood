import speechToTextHindi as stth
import textToSpeechHindi as ttsh
import mentalhealthModel as mhm
import speech2text_detection as s2t
import argparse
import time


def iterative_chat_loop(model):
    chat_history = []
    first_prompt = True
    while True:
        eng_input = s2t.translate_dynamic_to_english()
        
        assistant_response = mhm.chat_with_user(model, eng_input, chat_history, first_prompt)
        first_prompt = False

        if assistant_response == -1:
            ttsh.text_to_speech_hindi("You're welcome! If you need anything else, feel free to ask.")
            chat_history.append({'user': eng_input, 'assistant': "You're welcome! If you need anything else, feel free to ask."})
            break

        ttsh.text_to_speech_hindi(assistant_response)
        chat_history.append({'user': eng_input, 'assistant': assistant_response})

        # time.sleep(2)
    
    return chat_history

def main():
    parser = argparse.ArgumentParser(description="Generate appropriate response given prompt using Google Generative AI.")
    parser.add_argument('--api_key', type=str, required=True, help="API key for Google Generative AI.")
    parser.add_argument('--jsonl_file_path', type=str, required=True, help="Path to save chat history in JSONL format.")
    args = parser.parse_args()

    model = mhm.configure_genai(args.api_key)
    
    print("Configuring generative model...")
    model = mhm.configure_genai(args.api_key)
    
    print("Starting iterative chat loop...")
    chat_history = iterative_chat_loop(model)
    
    print(f"\nSaving chat history at: {args.jsonl_file_path}")
    mhm.save_chat_history(chat_history, args.jsonl_file_path)

if __name__ == "__main__":
    main()

# gemini API key: AIzaSyAwuW7ZvbYb7ygDqxWGDLjUSgfq8hbZ1x0
