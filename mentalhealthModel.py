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

NOTE: Always ask whether the user would like to have a solution-oriented approach or a comfort-oriented

User Query:
{question}
"""
# REFINEMENT TEMPLATE
REFINEMENT_TEMPLATE = """
You are an expert in communication, specializing in refining responses to be concise, human-like, and natural. Please refine the following response to be free of bullet points, unnecessary advice, or repetitive language. Make sure the tone is conversational, empathetic, and direct without sounding robotic. Remove any irrelevant or generic suggestions, and keep the response clear and focused.

Do not repeat phrases that have been used previously in conversation.

Assistant's Initial Response:
{initial_response}
"""

CONTEXTUAL_TEMPLATE = """
Here is the chat history between the user and the assistant. Use this to generate the response. Make sure to not repeat any phrases already used by the assistant

"""

def refine_response(model, assistant_response):
    refinement_prompt = REFINEMENT_TEMPLATE.format(initial_response=assistant_response)
    
    refined_response = generate_response(model, refinement_prompt)
    refined_response = preprocess_response(refined_response)
    
    return refined_response

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
        "max_output_tokens": 128  # Shorter responses for ongoing chat
    }
    model = genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings
    )
    return model

import re

def preprocess_response(response):
    clean_response = re.sub(r'[\*\-\•]', '', response)
    clean_response = clean_response.replace('\n', ' ').strip()
    clean_response = re.sub(r'\s+', ' ', clean_response)
    clean_response = re.sub(r'(\?|!)+', '.', clean_response)
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
        context = "\n".join([f"User: {entry['user']}\nAssistant: {entry['assistant']}" for entry in chat_history if 'user' and 'assistant' in entry]) + f"\nUser: "
        prompt = CONTEXTUAL_TEMPLATE + context + user_input
        print("This is the prompt being sent to the model\n\n\n")
        print(prompt)
        

    assistant_response = generate_response(model, prompt)
    # Refine the assistant response for more natural and human-like tone
    refined_assistant_response = refine_response(model, assistant_response)
    refined_assistant_response = preprocess_response(refined_assistant_response)
    print(f"Assistant: {refined_assistant_response}")
    
    return refined_assistant_response

def save_chat_history(chat_history, jsonl_file_path):
    with open(jsonl_file_path, 'w') as jsonl_file:
        for entry in chat_history:
            jsonl_file.write(json.dumps(entry) + '\n')