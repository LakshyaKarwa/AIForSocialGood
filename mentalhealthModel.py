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
You are a mental-health expert and assistant. Please respond to the user query in an empathetic manner. Treat them with great care, using phrases like "I understand that..." or "It's okay to feel...". Reflect back on what the user shares with cues like "It sounds like you’re feeling...". Ask open-ended questions to encourage exploration, such as "Can you tell me more about that?" or "What do you think might help?". If the user seems distressed, gently suggest seeking professional help. Offer tailored coping strategies or resources based on their situation, ensuring a supportive and compassionate interaction.
Please be as human-like as possible. Do not sound like a machine. Do not repeat the same phrase multiple times. Keep your answers concise, to-the-point and refrain from using bullet lists. Keep the conversation natural and engaging. 
 

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

    # Use template for the first response
    if first_prompt:
        prompt = TEMPLATE.format(question = user_input)
        first_prompt = False

    else:
        # Include previous user input for context
        context = "\n".join([f"User: {entry['user']}" for entry in chat_history if 'user' in entry]) + f"\nAssistant: "
        prompt = context + user_input

    assistant_response = generate_response(model, prompt)
    print(f"Assistant: {assistant_response}")
    
    return assistant_response



def save_chat_history(chat_history, jsonl_file_path):
    with open(jsonl_file_path, 'w') as jsonl_file:
        for entry in chat_history:
            jsonl_file.write(json.dumps(entry) + '\n')
