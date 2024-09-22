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
You are a mental-health expert and assistant. Please respond to the user query with empathy, tailoring your response based on the specifics of what the user shares. Vary your language to avoid sounding repetitive or formulaic. Ensure the conversation feels natural by reflecting back on what the user says and encouraging deeper exploration with thoughtful open-ended questions only when necessary. Avoid generic or surface-level advice. Be concise, direct, and empathetic, focusing on a single idea or solution where possible, and provide meaningful, practical suggestions.

If the user seems distressed, calmly suggest they reach out to a professional without being forceful. 

Your goal is to make the user feel heard, understood, and gently guided toward coping strategies, but without overwhelming them with too many suggestions or options.
 
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
        "max_output_tokens": 72  # Shorter responses for ongoing chat
    }
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return model

import re

def preprocess_response(response):
    # Remove asterisks, bullet points, and newlines
    clean_response = re.sub(r'[\*\-\•]', '', response)  # Remove bullet points or asterisks
    clean_response = clean_response.replace('\n', ' ').strip()  # Remove newlines, extra spaces
    clean_response = re.sub(r'\s+', ' ', clean_response)  # Collapse multiple spaces into one
    # Ensure proper punctuation (only full stops and commas)
    clean_response = re.sub(r'(\?|!)+', '.', clean_response)  # Replace multiple exclamation marks or question marks with full stops
    return clean_response

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

def chat_with_user(model, user_inp, chat_history, first_prompt):
    user_input = user_inp
    bye = ["okay thank you", "ok thanks", "okay thanks", "ok thank you"]
    if user_input.lower() in bye:
        print("Assistant: You're welcome! If you need anything else, feel free to ask.")
        return "end the conversation gemini"

    if first_prompt:
        prompt = TEMPLATE.format(question = user_input)
        first_prompt = False
    else:
        context = "\n".join([f"User: {entry['user']}" for entry in chat_history if 'user' in entry]) + f"\nAssistant: "
        prompt = context + user_input

    assistant_response = generate_response(model, prompt)
    assistant_response = preprocess_response(assistant_response)
    print(f"Assistant: {assistant_response}")
    
    return assistant_response



def save_chat_history(chat_history, jsonl_file_path):
    with open(jsonl_file_path, 'w') as jsonl_file:
        for entry in chat_history:
            jsonl_file.write(json.dumps(entry) + '\n')
