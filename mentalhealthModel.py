import os
import glob
import json
import time
import argparse
from tqdm import tqdm
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# PROMPT TEMPLATE
TEMPLATE = """
You are a mental-health expert and assistant. Please respond to the user query in an empathetic manner. Always treat them with great care, using phrases like "I understand that..." or "It's okay to feel...". Reflect back on what the user shares with cues like "It sounds like you’re feeling...". Ask open-ended questions to encourage exploration, such as "Can you tell me more about that?" or "What do you think might help?". If the user seems distressed, gently suggest seeking professional help. Offer tailored coping strategies or resources based on their situation, ensuring a supportive and compassionate interaction.

User Query:
{question}
"""

def configure_genai(api_key):
    genai.configure(api_key=api_key)
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    generation_config = {
        "temperature": 0.7,  # Adjusted for more engaging conversation
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 128,  # Shorter responses for ongoing chat
    }
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return model

def generate_response(model, prompt):
    try:
        response = model.generate_content(prompt)
        return response.text if response else "I'm sorry, I didn't understand that."
    except ResourceExhausted:
        print("Resource exhausted, retrying...")
        time.sleep(30)
        return generate_response(model, prompt)
    except Exception as e:
        print(f"Error occurred: {e}")
        return "I'm sorry, I encountered an error."

def chat_with_user(model):
    chat_history = []
    print("Welcome to the mental health chat assistant! How can I help you today?")
    
    first_prompt = True

    while True:
        # add hindi to english input here
        user_input = input("You: ")
        chat_history.append({'user': user_input})

        if "end the conversation gemini" in user_input.lower():
            print("Assistant: You're welcome! If you need anything else, feel free to ask.")
            break
        
        # use template only for the first response
        if first_prompt:
            prompt = TEMPLATE.format(question=user_input)
            first_prompt = False
        else:
            # include previous user input for context
            context = "\n".join([f"User: {entry['user']}" for entry in chat_history if 'user' in entry]) + f"\nAssistant: "
            prompt = context + user_input
        
        # add the translator and speech tool here
        assistant_response = generate_response(model, prompt)
        print(f"Assistant: {assistant_response}")
        chat_history.append({'assistant': assistant_response})
    return chat_history


def save_chat_history(chat_history, jsonl_file_path):
    with open(jsonl_file_path, 'w') as jsonl_file:
        for entry in chat_history:
            jsonl_file.write(json.dumps(entry) + '\n')

def main():
    parser = argparse.ArgumentParser(description="Generate appropriate response given prompt using Google Generative AI.")
    parser.add_argument('--api_key', type=str, required=True, help="API key for Google Generative AI.")
    parser.add_argument('--jsonl_file_path', type=str, required=True, help="Path to save chat history in JSONL format.")
    args = parser.parse_args()

    print("Configuring generative model")
    model = configure_genai(args.api_key)

    print("Starting chat...")
    chat_history = chat_with_user(model)

    print(f"\nChat history saved at: {args.jsonl_file_path}")
    save_chat_history(chat_history, args.jsonl_file_path)

if __name__ == "__main__":
    main()
