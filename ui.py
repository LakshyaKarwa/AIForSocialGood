import tkinter as tk
from tkinter import scrolledtext, messagebox
import speechToTextHindi as stth
import textToSpeechHindi as ttsh
import mentalhealthModel as mhm
import argparse
from deep_translator import GoogleTranslator
import speech2text_detection as s2t
import textToSpeechDyn as t2s

class MentalHealthAssistantUI:
    def __init__(self, master, model, jsonl_file_path):
        self.master = master
        self.master.title("Mental Health AI Assistant")
        self.master.geometry("600x500")
        self.master.configure(bg="#f0f8ff")

        # Chat history display
        self.chat_display = scrolledtext.ScrolledText(master, wrap=tk.WORD, state='disabled', width=70, height=20, bg="#ffffff", fg="#333333", font=("Arial", 12))
        self.chat_display.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input text box
        self.user_input = tk.Entry(master, width=50, bg="#ffffff", fg="#000000", font=("Arial", 12))
        self.user_input.grid(row=1, column=0, padx=10, pady=10)
        self.user_input.bind("<Return>", self.send_message)

        # Speak button
        self.speak_button = tk.Button(master, text="Speak", command=self.speak_input, bg="#000000", fg="black", font=("Arial", 12, "bold"), relief=tk.RAISED)
        self.speak_button.grid(row=1, column=1, padx=10, pady=10)

        # Language selection dropdown
        self.language_var = tk.StringVar(value="English")  # Default language
        self.language_menu = tk.OptionMenu(master, self.language_var, "English", "Native")
        self.language_menu.config(bg="#ffffff", fg="#000000", font=("Arial", 12))
        self.language_menu.grid(row=2, column=0, padx=10, pady=(10, 0), sticky=tk.W)
        self.language_code = 'en'
        self.detect = True

        self.model = model
        self.chat_history = []
        self.first_prompt = True
        self.jsonl_file_path = jsonl_file_path

        # Add a title label
        self.title_label = tk.Label(master, text="Mental Health AI Assistant", bg="#f0f8ff", fg="#4CAF50", font=("Arial", 16, "bold"))
        self.title_label.grid(row=3, column=0, columnspan=2, pady=(10, 0))


    def send_message(self, event=None):
        user_message = self.user_input.get()
        if not user_message.strip():
            return

        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"You: {user_message}\n")
        self.chat_display.config(state='disabled')
        self.user_input.delete(0, tk.END)

        assistant_response = mhm.chat_with_user(self.model, user_message, self.chat_history, self.first_prompt, self.language_code)
        self.first_prompt = False
        self.chat_history.append({'user': self.user_input.get(), 'assistant': assistant_response})
        if assistant_response == -1:
            response = "You're welcome! If you need anything else, feel free to ask."
            self.chat_history.append({'user': self.user_input.get(), 'assistant': response})
            self._display_response(1, response)
            self.master.destroy()
            return

        self._display_response(1, assistant_response)

    def speak_input(self):
        translated_input, self.language_code = s2t.translate_dynamic_to_english(self.detect, self.language_code)
        self.detect = False
        self._display_response(0, translated_input)
        assistant_response = mhm.chat_with_user(self.model, translated_input, self.chat_history, self.first_prompt, self.language_code)
        self.first_prompt = False
        
        if assistant_response == -1:
            response = "You're welcome! If you need anything else, feel free to ask."
            self.chat_history.append({'user': translated_input, 'assistant': response})
            self._display_response(1, response)
            self.master.destroy()
            return
        
        self.chat_history.append({'user': translated_input, 'assistant': assistant_response})
        self._display_response(1, assistant_response)

    def _display_response(self, id, response):
        self.chat_display.config(state='normal')
        if id == 0:
            if self.language_var.get() == 'Native':
                self.chat_display.insert(tk.END, f"You: {GoogleTranslator(source='auto', target=self.language_code).translate(response)}\n")
            else:
                self.chat_display.insert(tk.END, f"You: {response}\n")
        elif id == 1:
            if self.language_var.get() == 'Native':
                self.chat_display.insert(tk.END, f"Assistant: {GoogleTranslator(source='auto', target=self.language_code).translate(response)}\n")
            else:
                self.chat_display.insert(tk.END, f"Assistant: {response}\n")
            t2s.text_to_speech_dyn(response, self.language_code)
        self.chat_display.config(state='disabled')
        self.save_chat_history()

    def save_chat_history(self):
        mhm.save_chat_history(self.chat_history, self.jsonl_file_path)

def main(api_key, jsonl_file_path):
    model = mhm.configure_genai(api_key)
    root = tk.Tk()
    app = MentalHealthAssistantUI(root, model, jsonl_file_path)
    root.mainloop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the Mental Health AI Assistant.")
    parser.add_argument('--api_key', type=str, required=True, help="API key for Google Generative AI.")
    parser.add_argument('--jsonl_file_path', type=str, required=True, help="Path to save chat history in JSONL format.")
    args = parser.parse_args()
    
    main(args.api_key, args.jsonl_file_path)
