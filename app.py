# app.py
import os
import json
from flask import Flask, render_template, request, redirect, url_for
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

if not HUGGINGFACE_API_KEY:
    raise ValueError("HUGGINGFACE_API_KEY is not set in the environment variables.")

# Default model and parameters
DEFAULT_PARAMS = {
    'model': 'microsoft/DialoGPT-medium',  # Default model
    'temperature': 0.7,
    'top_p': 0.9,
    'max_length': 150,
    'repetition_penalty': 1.0,
    'top_k': 50,
    'do_sample': True
}

app = Flask(__name__)

# Cache for models and tokenizers
model_cache = {}
tokenizer_cache = {}

def get_model_and_tokenizer(model_name):
    if model_name not in model_cache:
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=HUGGINGFACE_API_KEY)
        model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=HUGGINGFACE_API_KEY)
        model_cache[model_name] = model
        tokenizer_cache[model_name] = tokenizer
    return model_cache[model_name], tokenizer_cache[model_name]

@app.route('/', methods=['GET', 'POST'])
def chat():
    params = DEFAULT_PARAMS.copy()
    bot_response = None
    user_input = None

    if request.method == 'POST':
        if 'reset' in request.form:
            return redirect(url_for('chat'))

        user_input = request.form.get('user_input', '').strip()
        params.update({
            'model': request.form.get('model', params['model']),
            'temperature': float(request.form.get('temperature', params['temperature'])),
            'top_p': float(request.form.get('top_p', params['top_p'])),
            'max_length': int(request.form.get('max_length', params['max_length'])),
            'repetition_penalty': float(request.form.get('repetition_penalty', params['repetition_penalty'])),
            'top_k': int(request.form.get('top_k', params['top_k'])),
            'do_sample': request.form.get('do_sample', 'true').lower() == 'true'
        })

        try:
            # Get model and tokenizer
            model, tokenizer = get_model_and_tokenizer(params['model'])

            # Encode the input
            input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

            # Generate response
            with torch.no_grad():
                output = model.generate(
                    input_ids,
                    max_length=params['max_length'],
                    temperature=params['temperature'],
                    top_p=params['top_p'],
                    top_k=params['top_k'],
                    repetition_penalty=params['repetition_penalty'],
                    do_sample=params['do_sample'],
                    pad_token_id=tokenizer.eos_token_id
                )

            # Decode the response
            bot_response = tokenizer.decode(output[0], skip_special_tokens=True)
            
            # Remove the input text from the response
            bot_response = bot_response[len(user_input):].strip()

        except Exception as e:
            bot_response = f"Error: {str(e)}"

    return render_template('chat.html', user_input=user_input, bot_response=bot_response, **params)

if __name__ == '__main__':
    app.run(debug=True)
